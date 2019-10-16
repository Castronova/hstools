# HSTools

A humble collection of HydroShare tools written in Python 3. The `hstools` library was originally a port of the CUAHSI JupyterHub `utilities.hydroshare` package modified to work on desktop computers and simplifies user interaction with the HydroShare data archive. 

## Installation

```
git clone https://github.com/Castronova/hstools.git
cd hstools
python setup.py install
```

## Connecting to HydroShare

Connect to HydroShare using the `hs_init` function. This will create an authentication file for accessing HydroShare. Note, this only needs to be executed once.

```
hs_init --help
```
```
hs_init
Enter HydroShare Username: <username>
Enter HydroShare Password: <password>
Auth saved to: ~/.hs_auth
```

## Creating a HydroShare resource

Create a new HydroShare resource using the `hs_create` command.

```
hs_create --help
```

```
hs_create \
-a This is the abstract of my resource \
-t My resource Title \
-k keyword1 keyword2 keyword3 \
-f myfile.txt ./another/file.txt 
```


## Downloading HydroShare resources

Downloading data from the HydroShare platform is done using globally unique identfiers (GUID). This GUIDs are defined for every HydroShare resource and can be aquired from resource URLs. The `hs_get` command downloads resource bagit file and unzips it into a directory of your choosing.

```
hs_get --help
```

```
hs_get <hydroshare resource id>
```

## Adding files to an existing HydroShare resource

Add files to an existing HydroShare resource using the `hs_add` command. This command allows you to optionally overwrite (`--overwrite`) files that already exist in a resource, which is helpful when updating content.

```
hs_add --help
```

```
hs_add <hydroshare resource id> -f my-file.txt my-other-file.txt
```


## Deleting a HydroShare resource

Delete an entire HydroShare resource using the `hs_delete` command. This is useful for cleaning up your HydroShare workspace. BEWARE: THIS WILL PERMANENTLY DELETE YOUR HYDROSHARE RESOURCE DATA.

```
hs_delete <hydroshare resource id>
```

