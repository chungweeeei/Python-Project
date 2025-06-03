import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.postgres import connect_to_postgres

from logger import context_logger

from repository.user.user import setup_user_repo
from repository.files.files import setup_files_repo

from routes.auth import init_auth_router
from routes.files import init_files_router

if __name__ == "__main__":

    pg_engine = connect_to_postgres()

    swagger_ui_desc = """
    API Server
    """
    app = FastAPI(title="Python API Project", description=swagger_ui_desc, version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTION"],
        allow_headers=["*"],
    )

    # register repo
    user_repo = setup_user_repo(logger=context_logger, engine=pg_engine)
    file_repo = setup_files_repo(logger=context_logger)

    app.include_router(init_auth_router(user_repo))
    app.include_router(init_files_router(file_repo))

    try:
        context_logger.info("Running API Server")
        uvicorn.run(app, host="0.0.0.0", port=3001)
    except KeyboardInterrupt as err:
        context_logger.error("[RUN] Uvicorn fun fastapi server failed: {}".format(err))
        exit()
    