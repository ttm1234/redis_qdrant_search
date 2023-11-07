import datetime
import json
import enum
from sqlalchemy import Column
import sqlalchemy as db
from extensions import Base, db_session, ModelMixin


class Sku(Base, ModelMixin):
    __tablename__ = 'sku'

    id = Column(db.Integer, autoincrement=True, primary_key=True, comment='sku id')
    title = Column(db.String(length=64), nullable=False, comment='title')
    description = Column(db.Text, nullable=False, comment='description')
    synced = Column(db.Boolean, default=False, comment='是否同步完成')

    __table_args__ = (
        {
            'comment': 'sku表',
        },
    )

    def to_dict(self):
        r = {
            'sku_id': self.id,
            'title': self.title,
            'description': self.description,
        }
        return r

    @classmethod
    def unsave_create(cls, _id, title, description):
        m = cls()
        m.id = _id
        m.title = title
        m.description = description
        m.synced = False
        return m

    @classmethod
    def create(cls, _id, title, description):
        m = cls.unsave_create(_id, title, description)
        m.save()
        return m

    @classmethod
    def get_all_need_sync(cls):
        ms = cls.query.filter(cls.synced == False).all()
        return ms

    @classmethod
    def get_one(cls, _id):
        r = cls.query.filter(cls.id == _id).first()
        return r

    def update(self, title, description):
        self.title = title
        self.description = description
        self.synced = False
        self.save()
        return self

    def update_synced(self):
        self.synced = True
        self.save()
        return self
