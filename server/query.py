from graphene import ObjectType, String, Field, ID, List

from schema.get_data.get_scatter import get_scatter_data
from schema.get_data.get_violin import get_violin_data

from schema.scatter import Scatter
from schema.violin import Violin
from schema.opacity import Opacity

class Query(ObjectType):
    scatter = Field(Scatter, vis=String(), group=String(), runID=String())
    @staticmethod
    def resolve_scatter(parent, info, vis, group, runID):
        return {"data": get_scatter_data(vis, group, runID, info.context.get('minio_client'))}
    """
    violin = Field(Violin, feature=String(), group=String(), runID=String())
    @staticmethod
    def resolve_violin(parent, info, feature, group, runID):
        return {"data": get_violin_data(feature, group, runID, info.context.get('minio_client'))}
    """
  