from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import config


echo = False
# echo = True
max_overflow = 1010
engine = create_engine(config.DB_CONFIG, pool_size=40, max_overflow=max_overflow, pool_recycle=28000, pool_pre_ping=True, convert_unicode=True, echo=echo)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base()
Base.query = db_session.query_property()
Base.__table_args__ = {
    'mysql_collate': 'utf8mb4_unicode_ci'
}


class ModelMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def save(self, *args, **kwargs):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


# def init_db():
#     import yourapplication.models
#     Base.metadata.create_all(bind=engine)
#     Base.metadata.tables[Model.__tablename__].create(bind=engine)