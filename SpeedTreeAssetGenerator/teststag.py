"""
test python file
"""

import hou
from . import fbxSubnet
from . import fbxSubnetFormat
from . import treeScatterSubnet

def myFunc():
    obj = hou.node("/obj")
    objNetworkBoxes = obj.networkBoxes()

    treeName = "BostonFern"

    box = fbxSubnet.getNetworkBox(treeName)
    print(box.comment() if box else "No network box found")


def exe1():
    # Get hip directory path
    hipPath = hou.hipFile.path()
    hipBaseName = hou.hipFile.basename()
    hipDir = hipPath.replace(hipBaseName, "")

    fbxImportFormat, fbxFilePaths, fbxFileDirs = \
        fbxSubnet.getFbxFilesList("{HIPDIR}assets/myTrees/stagTest".format(HIPDIR=hipDir))

    # Import fbx
    generatedTreeSubnets = []
    for key in fbxImportFormat:
        subnetName = key
        fbxFilePaths = fbxImportFormat[key]
        treeSubnet, actionMessage = fbxSubnet.importSpeedTreeFbx(fbxFilePaths, subnetName)
        print("\n{MSG}".format(MSG=actionMessage))
        # Create Matnet
        matnetName = subnetName + "_matnet"
        treeSubnet = fbxSubnetFormat.createMatnet(treeSubnet, matnetName)
        print("Materials Created for: " + treeSubnet.name())
        # Create Material Assignments
        treeSubnet = fbxSubnetFormat.AssignMaterials(treeSubnet, matnetName)
        print("Created MaterialAssignments for: " + treeSubnet.name())

        generatedTreeSubnets.append(treeSubnet)

    # Layout tree subnets
    if actionMessage.split()[0] == "Created":
        obj = hou.node("/obj")
        obj.layoutChildren(tuple(generatedTreeSubnets), vertical_spacing=0.35)


def exe2():
    treeSubnet = hou.node("/obj/BostonFern")
    hfGeoNode = hou.node("/obj/hf_scatter_example")

    scatterSubnet, actionMessage = treeScatterSubnet.createTreeScatterSubnet(treeSubnet, hfGeoNode)
    print(actionMessage)

if __name__ == "__main__":
    myFunc()


