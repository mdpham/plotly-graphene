from graphene import ObjectType, String, Field, ID, List

from scatter import Scatter
from violin import Violin
from opacity import Opacity

class Query(ObjectType):
    scatter = Field(Scatter)
    @staticmethod
    def resolve_scatter(parent, info):
        return ""
  