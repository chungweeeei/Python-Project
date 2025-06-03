from sqlalchemy import (
    Engine,
    create_engine
)

from sqlalchemy_utils import (
    create_database,
    database_exists
)

def connect_to_postgres(
    host: str = "localhost",
    port: str = "5432",
    db_name: str = "python_db",
    user: str = "root",
    password: str = "root"
) -> Engine:
    
    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{db_name}",
        pool_size=10
    )

    if not database_exists(engine.url):
        create_database(engine.url)

    return engine

