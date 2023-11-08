import datetime
import json
import enum
from sqlalchemy import Column
import sqlalchemy as db
from extensions import Base, db_session, ModelMixin
from sqlalchemy.orm.attributes import flag_modified

from util import unix_timestamp


class SkuPrediction(Base, ModelMixin):
    __tablename__ = 'sku_prediction'

    id = Column(db.Integer, autoincrement=True, primary_key=True, comment='pk')
    user_id = Column(db.Integer, nullable=False)
    sku_prediction_info = Column(db.JSON, nullable=False)
    # todo 未使用
    create_time = Column(db.String(length=64), default=0, comment='todo 未使用')

    __table_args__ = (
        db.Index('idx_unique', 'user_id', unique=True),
        {
            'comment': '用户对 sku 的评分表',
        },
    )

    @classmethod
    def one_by_uid(cls, user_id):
        r = cls.query.filter(
            cls.user_id == user_id,
            ).first()
        return r

    @classmethod
    def create(cls, user_id, sku_rating_info):
        m = cls()
        m.user_id = user_id
        m.sku_prediction_info = sku_rating_info
        m.create_time = unix_timestamp()
        m.save()

        return m

    @classmethod
    def update_sku_prediction_info(cls, sku_prediction_info):
        m = cls()
        m.sku_prediction_info = sku_prediction_info
        flag_modified(m, 'sku_prediction_info')
        m.save()

        return m
