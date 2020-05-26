from graphene import Enum, Field, Float, List, NonNull, ObjectType, String

import importlib
importlib.import_module("get_data", "scatter")
importlib.import_module("hex_colour_code")

class Mode(Enum):
    lines = "lines"
    markers = "markers"
    text = "text"
    none = "none"

class Marker(ObjectType):
    color = List(Field(HexColor))
    def resolve_color(parent, info):
        return parent["marker"]["color"]

class ScatterData(ObjectType):
    name = String()
    def resolve_name(parent, info):
        return parent["name"]
    
    mode = List(Mode)
    def resolve_mode(parent, info):
        return parent["mode"].split("+")
    
    text = NonNull(List(String()))
    def resolve_text(parent, info):
        return parent["text"]

    x = NonNull(List(NonNull(Float())))
    def resolve_x(parent, info):
        return parent["x"]

    y = NonNull(List(NonNull(Float())))
    def resolve_y(parent, info):
        return parent["y"]
    
    marker = Field(Marker)

class Scatter(ObjectType):
    """docstring for Scatter"""
    data = Field(List(NonNull(ScatterData)))
    def resolve_data(parent, info):
        return get_scatter_data(parent.vis, parent.group, parent.runID, parent.projectID)


