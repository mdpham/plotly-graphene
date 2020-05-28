from graphene import Field, Boolean, ObjectType
from hex_colour_code import HexColour
from positivenum import PositiveNumber

class Meanline(ObjectType):
    visible = Boolean()
    @staticmethod
    def resolve_visible(parent, info):
        return parent['visible']

    color = Field(HexColour)
    @staticmethod
    def resolve_color(parent, info):
        return parent['color']
    
    width = Field(PositiveNumber())
    @staticmethod
    def resolve_width(parent, info):
        return parent['width']
