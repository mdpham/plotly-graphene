from graphene import Field, Float, ID, List, NonNull, ObjectType, String

from get_data import get_scatter

from secondary.marker import Marker
from secondary.mode import Mode

class ScatterData(ObjectType):
    name = String()
    @staticmethod
    def resolve_name(parent, info):
        return parent["name"]
    
    mode = List(Mode)
    @staticmethod
    def resolve_mode(parent, info):
        return parent["mode"].split("+")
    
    text = List(NonNull(String))
    @staticmethod
    def resolve_text(parent, info):
        return parent["text"]

    x = List(NonNull(Float))
    @staticmethod
    def resolve_x(parent, info):
        return parent["x"]

    y = List(NonNull(Float))
    @staticmethod
    def resolve_y(parent, info):
        return parent["y"]  
    
    marker = Marker()
    @staticmethod
    def resolve_marker(parent, info):
        return parent["marker"]

class Scatter(ObjectType):
    """docstring for Scatter"""
    data = List(NonNull(ScatterData), vis=String(), group=String(), runID=String())
    @staticmethod
    def resolve_data(parent, info, vis, group, runID):
        return get_scatter.get_scatter_data(vis, group, runID, info.context.get('minio_client'))
