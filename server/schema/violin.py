from graphene import Boolean, Enum, Field, Float, List, NonNull, ObjectType, String

from get_data.get_violin import get_violin_data

from secondary.line import Line
from secondary.meanline import Meanline
from secondary.positivenum import PositiveNumber
from secondary.spanmode import SpanMode
from secondary.unitinterval import UnitInterval

class ViolinData(ObjectType):
    name = String()
    @staticmethod
    def resolve_name(parent, info):
        return parent["name"]

    # type = violin if this returns true, else type = box
    isTypeBox = Boolean()
    @staticmethod
    def resolve_type(parent, info):
        return parent["type"] == "box"
    
    spanmode = Field(SpanMode)
    @staticmethod
    def resolve_spanmode(parent, info):
        return parent["spanmode"]
    
    # Actually always empty so didnt use HexColour ¯\_(ツ)_/¯
    fillcolor = String()
    @staticmethod
    def resolve_fillcolor(parent, info):
        return parent["fillcolor"]

    line = Field(Line)
    @staticmethod
    def resolve_line(parent, info):
        return parent["line"]
    
    jitter = UnitInterval()
    @staticmethod
    def resolve_jitter(parent, info):
        return parent['jitter']
    
    width = PositiveNumber()
    @staticmethod
    def resolve_width(parent, info):
        return parent["width"]
    
    meanline = Field(Meanline)
    @staticmethod
    def resolve_meanline(parent, info):
        return parent['meanline']
    
    x = List(NonNull(String))
    @staticmethod
    def resolve_x(parent, info):
        return parent['x']
    
    y = List(NonNull(Float))
    @staticmethod
    def resolve_y(parent, info):
        return parent['y']
    """
    Some of the objects are actually box-plots not violin because 
    they are a zero expression and a zero expression box-plot looks better.
    They don't have a bandwidth property.
    """
    bandwidth = PositiveNumber()
    @staticmethod
    def resolve_bandwidth(parent, info):
        if ('bandwidth' in parent):
            return parent['bandwidth']
        else:
            return None

class Violin(ObjectType):
    data = List(NonNull(ViolinData))
    @staticmethod
    def resolve_data(parent, info):
        return get_violin_data(parent.group, parent.feature, parent.runID, info.context.get('minio_client'))
