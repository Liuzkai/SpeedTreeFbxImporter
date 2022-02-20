"""
API for building tree fbx subnet given SpeedTree Fbx imports
"""

import hou
import os
from . import classNodeNetwork

def getFbxFilesList(rootDir):
    """ Returns a list of fbx file paths """

    # Find fbx files in directory
    fbxFilePaths = []
    fbxFiles = []
    for (root, dirs, files) in os.walk(rootDir):
        for file in files:
            if file.endswith(".fbx"):
                fbxFilePaths.append(os.path.join(root, file))
                fbxFiles.append(file)
    fbxFilePaths = [fbxFilePath.replace("\\", "/") for fbxFilePath in fbxFilePaths]

    # get fbxFileDirs
    fbxFileDirs = []
    for fbxFilePath in fbxFilePaths:
        lastSlashIndex = fbxFilePath.rfind("/")
        fbxFileDirs.append(fbxFilePath[0:lastSlashIndex])

    return fbxFilePaths, fbxFileDirs, fbxFiles


def importSpeedTreeFbx(fbxFilePathsList, treeName):
    """ Imports all Speed Tree fbx files in a directory and collapses into a single subnet
    Returns subnet with cleaned geometry nodes """

    # Define obj context
    obj = hou.node("/obj")

    # If subnet already exists, delete it
    oldTreeSubnet = hou.node("/obj/{TREENAME}".format(TREENAME=treeName))
    if oldTreeSubnet:
        action = "Updated"
        oldTreeSubnet.destroy()
    else:
        action = "Created"

    # Import Fbx geo and collapse into subnet
    subnetGeos = []
    for fbxFile in fbxFilePathsList:
        importedSubnet, importMsgs = hou.hipFile.importFBX(fbxFile, import_cameras=False,
                                                   import_joints_and_skin=False,
                                                   import_lights=False,
                                                   import_animation=False,
                                                   import_materials=True,
                                                   import_geometry=True,
                                                   hide_joints_attached_to_skin=True,
                                                   convert_joints_to_zyx_rotation_order=False,
                                                   material_mode=hou.fbxMaterialMode.VopNetworks,
                                                   compatibility_mode=hou.fbxCompatibilityMode.Maya,
                                                   unlock_geometry=True,
                                                   import_nulls_as_subnets=True,
                                                   import_into_object_subnet=True,
                                                   create_sibling_bones=False)

        mySubnet = classNodeNetwork.MyNetwork(importedSubnet)
        mySubnet.cleanNetwork("shopnet", method="type")
        subnetChildren = mySubnet.extractChildren()

        for subnetChild in subnetChildren:
            subnetGeos.append(subnetChild)

        importedSubnet.destroy()

    collapsedSubnet = obj.collapseIntoSubnet(subnetGeos, treeName)
    print("{ACTION} Tree Subnet: {TREENAME}".format(ACTION=action, TREENAME=treeName))
    # Set subnet color
    subnetColor = hou.Color((.71, .518, .004))
    collapsedSubnet.setColor(subnetColor)
    # Layout children
    collapsedSubnet.layoutChildren()

    return collapsedSubnet


def AssignMaterials(subnet):
    """ Creates s@shop_materialpath attribute to existing primitive groups
    Returns formatted subnet and matnetName"""
    treeSubnet = classNodeNetwork.MyNetwork(subnet)
    treeName = subnet.name()

    for treeGeo in treeSubnet.children:
        treeGeo.parm("tx").revertToDefaults()
        treeGeo.parm("ty").revertToDefaults()
        treeGeo.parm("tz").revertToDefaults()
        treeGeoNet = classNodeNetwork.MyNetwork(treeGeo)
        print("Creating MaterialAssignments for " + treeGeoNet.name)

        # Prefix of new nodes
        newNodesPrefix = "myTree"

        # Clean old sops if any
        treeGeoNet.cleanNetwork("material", "pack", "output", method="type")
        treeGeoNet.cleanNetwork("assign_materials", method="name")
        #fileNode = treeGeoNet.findNodes("type", "file")[0]
        lastSop = treeGeoNet.findLastNode()

        # Add nodes and wire

        newNodes = treeGeoNet.addNodes("attribwrangle", "pack", "output", prefix=newNodesPrefix)
        treeGeoNet.wireNodes(newNodes, lastSop)

        # Add vex snippet to attribute wrangle. Create s@shop_materialpath to primitives
        assignWrangle = treeGeoNet.findNodes("type","attribwrangle")[0]
        assignWrangle.setName(newNodesPrefix+"_assign_materials")
        snippetParm = assignWrangle.parm("snippet")
        matnetName = treeName + "_matnet"
        matnetPath = "../../{MATNETNAME}/".format(MATNETNAME=matnetName)
        assignSnippet = '''// Assign different materials for each primitive group
string groups[] = detailintrinsic(0, "primitivegroups");

foreach (string group; groups) {{
    if (inprimgroup(0,group,@primnum) == 1){{
        string path = "{MATNETPATH}" + re_replace("_group","",group) + "/";
        s@shop_materialpath = opfullpath(path);
        }}

    }}
        '''.format(MATNETPATH=matnetPath)
        snippetParm.set(assignSnippet)
        assignWrangle.setParms({"class": 1})

        # Layout children
        treeGeo.layoutChildren(vertical_spacing=1)
        # Set display flag
        treeGeoNet.findLastNode().setDisplayFlag(True)
        treeGeoNet.findLastNode().setRenderFlag(True)

    return subnet, matnetName


def createMatnet(subnet, matnetName):
    treeSubnet = subnet
    treeMatnet = treeSubnet.createNode("matnet", matnetName)

    # Query first tree geo node in subnet
    treeGeo = treeSubnet.children()[0]
    treeGeoNet = classNodeNetwork.MyNetwork(treeGeo)

    # Create material networks based on existing group nodes
    groupNodes = treeGeoNet.findNodes("group", method="name")
    groupNodeNames = [groupNode.name() for groupNode in groupNodes]
    groupMaterials = [groupNodeName.replace("_group", "") for groupNodeName in groupNodeNames]
    print(groupMaterials)
    """
    for groupMaterial in groupMaterials:
        rsmb = treeMatnet.createNode("redshift_vopnet", groupMaterial)
        rsmbOut = rsmb.children()[0]
        shader = rsmb.children()[1]
        shaderTexName = groupMaterial.replace("_Mat","")
    """


def exe():

    # Get hip directory path
    hipPath = hou.hipFile.path()
    hipBaseName = hou.hipFile.basename()
    hipDir = hipPath.replace(hipBaseName, "")

    fbxFilePaths, fbxFileDirs, fbxFiles = getFbxFilesList("{HIPDIR}assets/myTrees".format(HIPDIR=hipDir))

    for fbxFilePath in fbxFilePaths:
        print(fbxFilePath)
    for fbxFileDir in fbxFileDirs:
        print(fbxFileDir)
    for fbxFile in fbxFiles:
        print(fbxFile)

    # Determine fbx file dir set
    fbxSubnetKeys = []
    for fbxFileDir in fbxFileDirs:
        lastSlashIndex = fbxFileDir.rfind("/")
        fbxSubnetKeys.append(fbxFileDir[lastSlashIndex+1:])

    fbxImportFormat = {}
    i = 0
    for fbxSubnetKey in fbxSubnetKeys:
        print(fbxSubnetKey)
        if fbxSubnetKey in fbxImportFormat:
            fbxImportFormat[fbxSubnetKey] = fbxImportFormat[fbxSubnetKey].append(fbxFilePaths[i])
        else:
            fbxImportFormat[fbxSubnetKey] = [fbxFilePaths[i]]
        i += 1

    print(fbxImportFormat)

    #treeSubnet = importSpeedTreeFbx(fbxFilePaths, "BostonFern")
    #treeSubnet, matnetName = AssignMaterials(treeSubnet)

    """
    createMatnet(treeSubnet, matnetName)
    """

