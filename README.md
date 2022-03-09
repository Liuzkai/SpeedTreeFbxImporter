# SpeedTree Fbx Importer
This tool imports assets generated from SpeedTree into Houdini. Imported assets will be contained within subnets along with Redshift materials and material assignments.

## Table of contents
* [General Info](#general-info)
* [Requirements](#requirements)
* [Setup](#setup)
* [Notes](#notes)
* [Task List](#task-list)

## General Info
The importer will import subnets with this structure into the Houdini scene:
```
/obj                        # obj context
├── AppleTree               # Subnet Generated by SpeedTreeFbxImporter
│   ├── AppleTree_1         # Geometry
│   ├── AppleTree_2         # Geometry
│   ├── AppleTree_3         # Geometry
│   └── AppleTree_matnet    # Material Network
```
## Requirements
* Houdini 19.0 or above
* Redshift in Houdini
* Some setup (see Setup)
	
## Setup
### Folder Setup
> To run this project, each set of SpeedTree assets must live in the same directory:
```
AppleTree                     # Example of AppleTree Folder
├── AppleTree_var1.fbx        # fbx file
├── AppleTree_var1.fbx        # fbx file
├── AppleTree_var1.fbx        # fbx file
├── Bark.png                  # fbx file
└── Leaf.png                  # Textures
```
> Example of a folder structure. Folders may contain any number of subdirectories:
```
FolderWithAllMyTrees          # Folder
├── FruitTrees                # Folder
│   │   Berries               # Folder
│   │   └── Strawberry        # Folder with SpeedTree assets
|   |
│   ├── AppleTree             # Folder with SpeedTree assets
│   ├── BananaPlant           # Folder with SpeedTree assets
│   └── CherryTree            # Folder with SpeedTree assets
| 
├── AfricanTrees              # Folder
│   ├── Acacia                # Folder with SpeedTree assets
│   └── Baobab                # Folder with SpeedTree assets
|
├── Oak                       # Folder with SpeedTree assets
└── MapleTree                 # Folder with SpeedTree assets
```
### Script Location
> Add SpeedTreeAssetGenerator folder $HOUDINI_USER_PREF_DIR/python3.7libs . See [https://www.sidefx.com/docs/houdini/hom/locations.html](url) for docs on Python script locations.
> For Gnomon, place SpeedTreeAssetGenerator folder in Z:/houdini19.0/python3.7libs
> Add SpeedTreeFbxImporterByDaniel.pypanel to python_panels directory. See [https://www.sidefx.com/docs/houdini/ref/windows/pythonpaneleditor.html](https://www.sidefx.com/docs/houdini/ref/windows/pythonpaneleditor.html) for docs on Python Panel Editor
> For Gnomon, place SpeedTreeFbxImporterByDaniel.pypanel folder in Z:/houdini19.0/python_panels
### Houdini Setup
> This tool is accessed through a dockable Python Panel in a Houdini session.

1. Add a python panel.

![This is an image](SpeedTreeAssetGenerator/pythonPanelLocation.png)

2. Select SpeedTree Fbx Importer by Daniel in the drop down menu.

![This is an image](SpeedTreeAssetGenerator/pythonPanelDropDown.png)
## Notes
Importing SpeedTree fbxs automatically creates and assigns primitive groups according to material. Do not change name of the group nodes and group names. Do not change the name of texture files. They match the group names by default.
## Task List
- [ ] Make compatible with versions before Houdini 19.0
- [ ] Support textures other than png
