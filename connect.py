from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# container
# docker run --name homework_06 -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

url_to_db = "postgresql+psycopg2://postgres:567234@localhost:5432/postgres"

engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
