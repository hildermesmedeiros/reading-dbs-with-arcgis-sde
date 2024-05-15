import arcpy
from arcgis.geometry import Geometry, Polygon

# TODO verificar se eh wgs84, se for trocar para wkid do sirgas 2000
WGS_84_WKID = 4326
SIRGAS_2000_WKID = 4674
class CreateGeometry:
    @staticmethod
    def create_polygon(shape:str) -> Polygon:
        """
        Creates geometry from Well Know Text (WKT)
        :param shape: WKT string
        :return:
        """
        if shape:
            shape_json = arcpy.FromWKT(shape).JSON
            return Polygon(shape_json.replace('"wkid":null', f'"wkid":{SIRGAS_2000_WKID}'))
        return Polygon({"rings": [[[]]], "spatialReference":{"wkid":SIRGAS_2000_WKID}})
