from sqlalchemy import (Column,
                        Integer,
                        BigInteger,
                        String,
                        Float,
                        Date,
                        DateTime,
                        Time,
                        Text,
                        func)
from sqlalchemy.dialects.postgresql import BYTEA, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
import datetime

Base = declarative_base()

SIRGAS_2000_WKID = 4674
class GeometriaPolyModel(Base):
    __tablename__ = 'geometrias_poly'
    objectid = Column(Integer, primary_key=True)
    campotexto = Column(String)
    campointeirocurto = Column(Integer)
    campointeirolongo = Column(Integer)
    campofloat = Column(Float)
    campodata = Column(DateTime)
    campobigint = Column(BigInteger)
    campodateonly = Column(Date)
    campotimeonly = Column(Time)
    campoblob = Column(BYTEA)  # Binary Large Object type in PostgreSQL
    globalid = Column(UUID(as_uuid=True), unique=True)
    created_user = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_edited_user = Column(String)
    last_edited_date = Column(DateTime, default=datetime.datetime.utcnow)
    shape = Column(Text)

    @hybrid_property
    def shape_wkt(self):
        return self.shape

    @shape_wkt.expression
    def shape_wkt(cls):
        shape = func.sde.st_astext(cls.shape).label('SHAPE')
        return shape
