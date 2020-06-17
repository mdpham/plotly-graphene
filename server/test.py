from graphene import Schema#, ObjectType, String, Field
import json

from schema.get_data import get_scatter
from schema.get_data import get_violin

from query import Query

#from python_modules.scatter import get_scatter

def main():
    # Creating a Schema to execute queries on
    schema = Schema(query=Query)
    test_scatter(schema) # Set displayOutput=True to print graphene result
    
def test_violin(schema, displayOutput=False):
    print("Testing Violin")

    # Setting arguments for a mock call
    group = "Seurat_Clusters_Resolution1"
    feature = "PASK"
    runID = "5eda76def93f82004f4114c6"

    # We get the scatter data from the original python function
    original_result = get_violin.get_violin_data(feature, group, runID)

    result = schema.execute(
    # Query
    """
    query getViolin ($feature: String, $group: String, $runID: String) {
        violin(feature: $feature, group: $group, runID: $runID) {
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
        "feature": feature,
        "group": group,
        "runID": runID
    })

    if(result.errors != None):
        print("ERROR(s)")
        for err in result.errors:
            print(err)
        return False

    # Getting a dictionary which is a plotly-object 
    graphene_result = result.data["violin"]["data"]

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
            previously_similar = similar
            similar = similar and eql
            if (previously_similar and not similar):
                print("Mismatch at idx {idx} with key {k}".format(idx=i, k=key))
                print(gr[key])
                print(ogr[key])
                print("Lengths " + ("match" if (len(gr[key]) == len(ogr[key])) else "do not match"))
            
    print("Graphene output matches data from get_violin" if similar else "Uh Oh! Check Violin")

    if displayOutput:
        print(graphene_result)

def test_scatter(schema, displayOutput=False):
    print("Testing Scatter")

    # Setting arguments for a mock call
    vis = "TSNE"
    group = "Seurat_Clusters_Resolution1"
    runID = "5eda76def93f82004f4114c6"

    # We get the scatter data from the original python function
    original_result = get_scatter.get_scatter_data(vis, group, runID)

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
    })

    if(result.errors != None):
        print("ERROR(s)")
        for err in result.errors:
            print(err)
        return False

    # Getting a dictionary which is a plotly-object
    graphene_result = result.data["scatter"]["data"]

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
            previously_similar = similar
            similar = similar and eql
            if (previously_similar and not similar):
                print("Mismatch at idx {idx} with key {k}".format(idx=i, k=key))
                print(gr[key])
                print(ogr[key])
                print("Lengths " + ("match" if (len(gr[key]) == len(ogr[key])) else "do not match"))
            
    print("Graphene output matches data from get_scatter" if similar else "Uh Oh! Check Scatter")

    if displayOutput:
        print(graphene_result)

if __name__ == "__main__":
    main()
