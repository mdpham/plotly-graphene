from graphene import ObjectType, String, Field, ID, List

from get_data import get_scatter

from scatter import Scatter
from violin import Violin
from opacity import Opacity

class Query(ObjectType):
    scatter = Field(Scatter, vis=String(), group=String(), runID=String())
    @staticmethod
    def resolve_scatter(parent, info, vis, group, runID):
        return {"data": get_scatter.get_scatter_data(vis, group, runID, info.context.get('minio_client'))}
  