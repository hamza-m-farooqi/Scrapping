from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_models import Base

engine = create_engine("sqlite:///DataBase/night_cafe_images.db", echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.commit()

session.close()
