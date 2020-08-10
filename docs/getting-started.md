# Getting Started 


## Installation

This `hstools` package is currently only supported on MacOSX and Linux. It can be installed using the Python package installer (Pip) or directly from source.

### Install using Pip

The `hstools` package can be found at [https://pypi.org/project/HSTools/](https://pypi.org/project/HSTools/) and installed using the following command.
```
pip install hstools
```

### Install from source

The source code for `hstools` can be found at [https://github.com/Castronova/hstools](https://github.com/Castronova/hstools). Perform the following commands to install from source.

```
git clone https://github.com/Castronova/hstools 
cd hstools
python setup.py install
```

## Overview

After the libary is installed, it can be executed using the following command: `hs`. There are currently 6 options for interacting with HydroShare: `get`, `add`, `create`, `delete`, `ls`, and `init`. For detailed information about any of these add the `--help` flag after the options, e.g. `$hs get --help`.

```
$ hs
usage: hs [-h] {get,add,create,delete,ls,init} ...

HSTools is a humble collection of tools for interacting with data in the
HydroShare repository. It wraps the HydroShare REST API to provide simple
commands for working with resources.

positional arguments:
  {get,add,create,delete,ls,init}
    get                 Retrieve resource content from HydroShare
    add                 Add files to an existing HydroShare resource
    create              Create a new HydroShare resource
    delete              Delete a HydroShare resource
    list                List HydroShare resources that you own
    init                Initialize a connection with HydroShare

optional arguments:
  -h, --help            show this help message and exit
```

### Connect to HydroShare

Connect to HydroShare using the `init` option. This will create an authentication file for accessing HydroShare that is cached in your `$HOME` directory by default. This path can be changed using the `-d` flag. Note, this command only needs to be executed once.


```
$ hs init
Enter HydroShare Username: <username>
Enter HydroShare Password: <password>
Auth saved to: ~/.hs_auth
```

### Create Resource

Create a new HydroShare resource using the `create` options.


```
$ hs create \
-a This is the abstract of my resource \
-t My resource Title \
-k keyword1 keyword2 keyword3 \
-f myfile.txt ./another/file.txt 
```


### List Resources

Listing HydroShare resources using the `ls` options.


```
$ hs list
```

List files in long format

```
$ hs list -l
```

List the first 17 resources in long format

```
$ hs list -l -n 17
```

Filter resources by published

```
$ hs list -filter published=true
```

### Download Resource

Downloading data from the HydroShare platform is done using globally unique identfiers (GUID). This GUIDs are defined for every HydroShare resource and can be aquired from a resources URL. The `get` option downloads the resource bagit archive and unzips it into a directory of your choosing.


```
$ hs get <hydroshare resource id>
```

### Add Files 

Add files to an existing HydroShare resource using the `add` option. This command allows you to optionally overwrite (`--overwrite`) files thatalready exist in a resource, which is helpful when updating content.


```
$ hs add <hydroshare resource id> -f my-file.txt my-other-file.txt
```


### Deleting Resource

Delete an entire HydroShare resource using the `delete` option. This is useful for cleaning up your HydroShare workspace. BEWARE: THIS WILL PERMANENTLY DELETE YOUR HYDROSHARE RESOURCE DATA.

```
$ hs delete <hydroshare resource id>
``` 

