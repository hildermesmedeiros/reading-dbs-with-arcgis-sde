from sqlalchemy.ext.declarative import declarative_base

import pandas as pd
from arcgis.geometry import Geometry
from psycopg2 import OperationalError
from sqlalchemy.orm import aliased
from sqlalchemy import or_, and_

import arcpy
from arcgis.features import GeoAccessor
from typing import Union

from dbcon import GetConn
from models import GeometriaPolyModel
from geom import CreateGeometry

Base = declarative_base()


class QueryPolygon:
    @staticmethod
    def execute(query_all: bool = True) -> Union[pd.DataFrame, GeoAccessor]:

        model_alias = aliased(GeometriaPolyModel, name='GeometriaPolyModel')
        try:
            with GetConn() as (session, engine):

                query = session.query(model_alias.objectid,
                                      model_alias.campotexto,
                                      model_alias.campointeirocurto,
                                      model_alias.campointeirolongo,
                                      model_alias.campofloat,
                                      model_alias.campodata,
                                      model_alias.campobigint,
                                      model_alias.campodateonly,
                                      model_alias.campotimeonly,
                                      model_alias.campoblob,
                                      model_alias.globalid,
                                      model_alias.created_user,
                                      model_alias.created_date,
                                      model_alias.last_edited_user,
                                      model_alias.last_edited_date,
                                      model_alias.shape_wkt
                                      )

                if not query_all:
                    #query exemple
                    query = query.filter(
                        or_(
                            and_(
                                model_alias.campotexto != 'abc',
                                model_alias.objectid != 5
                            ),
                            model_alias.globalid.is_(None)
                        )
                    )

                sdf = pd.read_sql(query.statement, engine)
                if sdf.empty:
                    return sdf
                sdf['SHAPE'] = sdf['SHAPE'].map(
                    lambda shape: CreateGeometry.create_polygon(shape)
                )
                return sdf
        except OperationalError as e:
            print(e)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    sdf = QueryPolygon.execute()
