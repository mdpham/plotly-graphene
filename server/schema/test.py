from graphene import Schema#, ObjectType, String, Field
from minio import Minio
import json
from get_data import get_scatter

from query import Query

#from python_modules.scatter import get_scatter

def test_scatter(client, schema):
    # Setting arguments for a mock call
    vis = "TSNE"
    group = "Seurat_Clusters_Resolution1"
    runID = "5eda76def93f82004f4114c6"
    
    result = schema.execute(
    # Query
    """
    query getScatter ($vis: String, $group: String, $runID: String) {
        scatter {
            data(vis: $vis, group: $group, runID: $runID)
        }
    }
    """,
    # Setting Arguments
    variables={
        "vis": vis,
        "group": group,
        "runID": runID
    },
    # Passing the client through context
    context={"minio_client": client})

    if(result.errors != None):
        print("ERROR")
        for err in result.errors:
            print(err)
        #print(json.dumps(result.errors, indent=4))
        return

    # Getting a dictionary which is a pltoly-object 
    graphene_result = result.data['scatter']

    # Now we get the scatter data from the original python function
    #original_result = get_scatter(vis, group, runID, projectID)

    #similar = graphene_result == original_result

    print(graphene_result)
    # Should return True
    #return similar

if __name__ == "__main__":
    # Generating an instance of a minio client
    client = Minio("127.0.0.1:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)

    # Creating a Schema to execute queries on
    schema = Schema(query=Query)

    test_scatter(client, schema)
