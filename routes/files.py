from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)

from repository.files.files import filesRepo
from repository.exceptions import RepoInternalError

def init_files_router(file_repo: filesRepo) -> APIRouter:

    files_router = APIRouter(prefix="", tags=["files"])

    @files_router.post("/v1/files/upload")
    async def upload_file(request: Request):

        file_id = request.headers.get("X-fileId")
        filename = request.headers.get("X-filename")
        start_byte = request.headers.get("X-startByte")
        total_bytes = request.headers.get("Content-Length")

        if file_id is None or filename is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Missing required headers")
        
        try:
            async for chunk in request.stream():
                """
                    The chunk size of 262144 bytes (256KB) is a default value used by Starlette
                    for streaming request bodies. This size is chosen as a balance between memory usage and performance, 
                    allowing efficient handling of large request bodies without consuming too much memory.
                """
                file_repo.upload(filename=filename, content=chunk)
            
            file_repo.deploy(filename=filename)
        except RepoInternalError as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=str(err))

        return status.HTTP_200_OK

    return files_router