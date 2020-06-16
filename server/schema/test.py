from graphene import Schema#, ObjectType, String, Field
from minio import Minio
import json
from get_data import get_scatter

from query import Query

#from python_modules.scatter import get_scatter

def test_scatter(client, schema):
    print("Testing Scatter")

    # Setting arguments for a mock call
    vis = "TSNE"
    group = "Seurat_Clusters_Resolution1"
    runID = "5eda76def93f82004f4114c6"

    # We get the scatter data from the original python function
    original_result = get_scatter.get_scatter_data(vis, group, runID, client)

    result = schema.execute(
    # Query
    """
    query getScatter ($vis: String, $group: String, $runID: String) {
        scatter(vis: $vis, group: $group, runID: $runID) {
            data {
                name
                mode
                text
                x
                y
                marker {
                    color
                }
            }
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
        print("ERROR(s)")
        for err in result.errors:
            print(err)
        return False

    # Getting a dictionary which is a plotly-object 
    graphene_result = result.data['scatter']['data']

    similar = True
    for i in range(len(original_result)):
        gr = graphene_result[i]
        ogr = original_result[i]
        for key in gr:
            if(key == "mode"):
                eql = "+".join(gr["mode"]) == ogr["mode"]
            elif(key == "marker"):
                eql = len(gr["marker"]["color"]) == len(ogr["marker"]["color"])
                if(eql):
                    for j in range(len(ogr["marker"]["color"])):
                        eql = eql and (ogr["marker"]["color"][j].upper() == gr["marker"]["color"][j])
            else:
                eql = (gr[key] == ogr[key])
            last = similar
            similar = similar and eql
            if (last and not similar):
                print("Mismatch at idx {idx} with key {k}".format(idx=i, k=key))
                print(gr[key])
                print(ogr[key])
                print("Lengths " + ("match" if (len(gr[key]) == len(ogr[key])) else "do not match"))
            
    print("Scatter seems to work" if similar else "Uh Oh! Check Scatter")

if __name__ == "__main__":
    # Generating an instance of a minio client
    client = Minio("127.0.0.1:9000", access_key="crescent-access", secret_key="crescent-secret", secure=False)

    # Creating a Schema to execute queries on
    schema = Schema(query=Query)
    test_scatter(client, schema)
