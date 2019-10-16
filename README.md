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


Getting resources

Downloads data from the HydroShare platform using globally unique identfiers (GUID). This GUIDs are defined for every HydroShare resource and can be aquired from resource URLs.  

```
hs_get --help
```

```
hs_get <hydroshare resource id>
```

Adding files to an existing resource

```
hs_add --help
```

Deleting a resource

```
hs_delete
```

