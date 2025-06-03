import io
import structlog

from ..exceptions import RepoInternalError

class filesRepo:

    def __init__(self, logger: structlog.stdlib.BoundLogger):
        
        # register log handler
        self.logger = logger

        self._received_content = io.BytesIO()

    def upload(self, filename: str, content: bytes):

        try:
            self._received_content.write(content)
        except Exception as err:
            self.logger.error(f"[fileRepo][upload] Failed to upload file {filename}: {err}")
            raise RepoInternalError(f"Failed to upload file {filename}")

    def deploy(self, filename: str):
        
        try:
            # chunk_size = 1024 * 1024
            file_content = self._received_content.getvalue()
            with open(f"./{filename}", "wb") as file:
                # for i in range(0, len(file_content), chunk_size):
                    # file.write(file_content[i:i + chunk_size])
                file.write(file_content)
        except Exception as err:
            self.logger.error(f"[fileRepo][deploy] Failed to deploy file {filename}: {err}")
            raise RepoInternalError(f"Failed to deploy file {filename}")

def setup_files_repo(logger: structlog.stdlib.BoundLogger) -> filesRepo:
    return filesRepo(logger=logger)