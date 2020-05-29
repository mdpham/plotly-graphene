from graphene import Field, List, ObjectType

from hex_colour_code import HexColour
from unitinterval import UnitInterval

class Marker(ObjectType):
    color = List(Field(HexColour))
    @staticmethod
    def resolve_color(parent, info):
        return parent["color"]
    
    opacity = UnitInterval()
    @staticmethod
    def resolve_opacity(parent, info):
        return parent["opacity"]

