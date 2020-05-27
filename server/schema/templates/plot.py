from graphene import ObjectType, String, Field, ID
from minio_client.client import minio_client
from schema.minio_bucket import MinioBucket

class Plot(ObjectType):
  plot_type = String()
  
  def resolve_plot_type(parent, info):
    return parent['plot_type']