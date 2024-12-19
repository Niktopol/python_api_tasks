from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = 'postgresql://user:a9QtBSozWH4S8Gjrz5LgzXNGidHH1XcD@dpg-csh6nmhu0jms739sl7p0-a.frankfurt-postgres.render.com/fastapi_database_rmyd'
DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/fastapi_database'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
Base = declarative_base()
