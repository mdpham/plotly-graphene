from graphene import Field, List, ObjectType

from hex_colour_code import HexColour
from positivenum import PositiveNumber

class Line(ObjectType):
    color = Field(List(HexColour))
    @staticmethod
    def resolve_color(parent, info):
        return parent['color']
    
    width = Field(PositiveNumber())
    @staticmethod
    def resolve_width(parent, info):
        return parent['width']
