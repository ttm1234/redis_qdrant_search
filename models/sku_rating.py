import datetime
import json
import enum
from sqlalchemy import Column
import sqlalchemy as db
from extensions import Base, db_session, ModelMixin
from util import unix_timestamp


class SkuRating(Base, ModelMixin):
    __tablename__ = 'sku_rating'

    id = Column(db.Integer, autoincrement=True, primary_key=True, comment='pk')
    user_id = Column(db.Integer, nullable=False)
    sku_id = Column(db.Integer, nullable=False)
    rating = Column(db.Integer, nullable=False)
    # todo 未使用
    create_time = Column(db.String(length=64), default=0, comment='todo 未使用')

    __table_args__ = (
        db.Index('idx_unique', 'user_id', 'sku_id', unique=True),
        {
            'comment': '用户对 sku 的评分表',
        },
    )

    @classmethod
    def get_all(cls):
        ms = cls.query.filter().all()
        return ms

    @classmethod
    def find_one(cls, user_id, sku_id):
        r = cls.query.filter(
            cls.user_id == user_id,
            cls.sku_id == sku_id,
            ).first()
        return r

    @classmethod
    def create(cls, user_id, sku_id, rating):
        m = cls()
        m.user_id = user_id
        m.sku_id = sku_id
        m.rating = rating
        m.create_time = unix_timestamp()
        m.save()

        return m

    def update_rating(self, rating):
        if rating != self.rating:
            self.rating = rating
            self.save()
        return self
