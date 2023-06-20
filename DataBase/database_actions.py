from sqlalchemy import create_engine, desc,not_,select
from sqlalchemy.orm import sessionmaker
from DataBase.database_models import (
    AI_Generated_Images_Search_Words,
    AI_Generated_Images_Search_Words_Track,
    AI_Generated_Images_Platforms_Info,
)


class Database_Actions:
    def __init__(self, connection_string):
        engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=engine)

    def add(self, entity):
        session = self.Session()
        try:
            session.add(entity)
            session.commit()
            session.close()
        except Exception as ex:
            return f"An Error Occured while Adding : {str(ex)}"

    def update(self, entity):
        session = self.Session()
        try:
            session.merge(entity)
            session.commit()
            session.close()
        except Exception as ex:
            return f"An Error Occured while Updating : {str(ex)}"

    def delete(self, entity):
        session = self.Session()
        try:
            session.delete(entity)
            session.commit()
            session.close()
        except Exception as ex:
            return f"An Error Occured while Deleting : {str(ex)}"

    def bulk_add(self, entities):
        session = self.Session()
        try:
            session.bulk_save_objects(entities)
            session.commit()
            session.close()
        except Exception as ex:
            return f"An Error Occured while Bulk Adding : {str(ex)}"

    def get(self, model, **kwargs):
        session = self.Session()
        try:
            query = session.query(model).filter_by(**kwargs)
            result = query.all()
            session.close()
            return result
        except Exception as ex:
            return f"An Error Occured while Getting : {str(ex)}"

    def get_limited(self, model, limit, **kwargs):
        session = self.Session()
        try:
            query = session.query(model).filter_by(**kwargs)
            result = query.limit(limit).all()
            session.close()
            return result
        except Exception as ex:
            return f"An Error Occured while Getting : {str(ex)}"

    def get_latest(self, model, latest_by_column, **kwargs):
        session = self.Session()
        try:
            if kwargs is not None:
                query = (
                    session.query(model)
                    .filter_by(**kwargs)
                    .order_by(desc(latest_by_column))
                    .first()
                )
            else:
                query = session.query(model).order_by(desc(latest_by_column)).first()
            session.close()
            return query
        except Exception as ex:
            return f"An Error Occured while Getting Latest : {str(ex)}"

    def check_if_value_exists(self, model, **kwargs):
        session = self.Session()
        try:
            query = session.query(model).filter_by(**kwargs)
            exists = session.query(query.exists()).scalar()
            session.close()
            return exists
        except Exception as ex:
            session.close()
            return f"An Error Occurred: {str(ex)}"

    def get_search_words_untracked_by_platform(self, platform_name):
        platform_object = self.get(
            AI_Generated_Images_Platforms_Info, name=platform_name
        )
        platform_id = 0
        if platform_object:
            platform_id = platform_object[0].id
        if not platform_id>0:
            return f"Platform not Found!"
        session=self.Session()
        # Subquery to select ids from AI_Generated_Images_Search_Words_Track for a specific platform_id
        subquery = (
            select(AI_Generated_Images_Search_Words_Track.search_word_id)
            .where(AI_Generated_Images_Search_Words_Track.platform_id == platform_id)
            .alias()
        )

        # Query to select 20 records from AI_Generated_Images_Search_Words where id is not in the subquery
        query = (
            select(AI_Generated_Images_Search_Words)
            .where(not_(AI_Generated_Images_Search_Words.id.in_(subquery)))
            .limit(50)
        )

        result = session.execute(query).scalars().all()
        return result
