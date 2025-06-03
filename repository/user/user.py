import structlog

from sqlalchemy import (
    Engine,
    select
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

from .schemas import (
    UserInfo,
    _USER_BASE_REPO
)

from ..exceptions import (
    BadRequest,
    RepoInternalError
)

from utils.hash import hash_password

class userRepo:

    def __init__(self, 
                 logger: structlog.stdlib.BoundLogger,
                 engine: Engine):
        
        # register log handler
        self.logger = logger

        # register database session
        self.session_maker = sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine)
        
    def get_user(self, email: str) -> UserInfo:

        with self.session_maker() as session:

            try:

                query_stmt = (
                    select(UserInfo)
                    .where(UserInfo.email == email)
                    .cte("user_query_stmt")
                )

                return session.query(query_stmt).one()
            
            except Exception as err:
                self.logger.error(f"[userRepo][get_user] Failed to get {email} user info: {err}")
                session.rollback()
                raise RepoInternalError(f"Failed to get {email} user info")

    def register_user(self, email: str, username: str, password: str):

        with self.session_maker() as session:

            try:

                # Check if the user already exists
                existing_user = session.query(UserInfo).filter_by(email=email).first()
                if existing_user:
                    raise BadRequest(f"User with email {email} already exists")
                
                insert_stmt = (
                    insert(UserInfo)
                    .values({
                        "email": email,
                        "username": username,
                        "role": "guest",
                        "password": hash_password(password)
                    })
                )

                session.execute(insert_stmt)
                session.commit()

            except BadRequest as err:
                session.rollback()
                raise err

            except Exception as err:
                self.logger.error(f"[userRepo][register_user] Failed to register a user: {err}")
                session.rollback()
                raise RepoInternalError(f"Failed to register a user")

def setup_user_repo(logger: structlog.stdlib.BoundLogger, engine: Engine) -> userRepo:

    _USER_BASE_REPO.metadata.create_all(engine)

    user_repo = userRepo(logger=logger, engine=engine)
    
    return user_repo