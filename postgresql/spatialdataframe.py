from sqlalchemy.ext.declarative import declarative_base

import pandas as pd
from arcgis.geometry import Geometry
from psycopg2 import OperationalError
from sqlalchemy.orm import aliased
import arcpy
from arcgis.features import GeoAccessor

from dbcon import GetConn
from models import GeometriaPolyModel

Base = declarative_base()

SIRGAS_2000_WKID = 4674

def geometria_poly_to_geoaccessor() -> GeoAccessor:
    geometria_poly_alias = aliased(GeometriaPolyModel, name='GeometriaPolyModel')
    try:
        with GetConn() as (session, engine):
            query = session.query(geometria_poly_alias.objectid,
                                  geometria_poly_alias.campotexto,
                                  geometria_poly_alias.campointeirocurto,
                                  geometria_poly_alias.campointeirolongo,
                                  geometria_poly_alias.campofloat,
                                  geometria_poly_alias.campodata,
                                  geometria_poly_alias.campobigint,
                                  geometria_poly_alias.campodateonly,
                                  geometria_poly_alias.campotimeonly,
                                  geometria_poly_alias.campoblob,
                                  geometria_poly_alias.globalid,
                                  geometria_poly_alias.created_user,
                                  geometria_poly_alias.created_date,
                                  geometria_poly_alias.last_edited_user,
                                  geometria_poly_alias.last_edited_date,
                                  geometria_poly_alias.shape_wkt
                                  )
            sdf = pd.read_sql(query.statement, engine)
            sdf['SHAPE'] = sdf['SHAPE'].map(
                lambda shape: arcpy.FromWKT(shape).JSON
            ).map(
                lambda shape: Geometry(
                    shape.replace('"wkid":null', f'"wkid":{SIRGAS_2000_WKID}')
                )
            )

            return GeoAccessor.from_df(sdf, geometry_column='SHAPE')
    except OperationalError as e:
        print(e)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    sdf = geometria_poly_to_geoaccessor()
