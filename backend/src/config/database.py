from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

db_username = 'postgres'
db_password = '1234'
db_url = '127.0.0.1'
db_port = '5432'
db_name = 'Inventory_control'

connectionString = f'postgresql://{db_username}:{db_password}@{db_url}:{db_port}/{db_name}'

engine = create_engine(connectionString, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

try:
    # Подключаемся к базе данных
    with engine.connect() as connection:
        result = connection.exec_driver_sql("SHOW port")
        print(result.scalar())
except OperationalError as e:
    print(f"Connection failed: {e}")