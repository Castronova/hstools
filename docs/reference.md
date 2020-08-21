<a name="hstools"></a>
# hstools

<a name="hstools.auth"></a>
# hstools.auth

<a name="hstools.auth.basic_authorization"></a>
#### basic\_authorization

```python
basic_authorization(authfile='~/.hs_auth_basic')
```

This function performs basic HS authorization using username and password stored in an external file, e.g. ~/.hs_auth_basic. The file should be b64 encoded and contain JSON dictionary of username and password.

**Arguments**:

- `authfile`: base64 encoded authorization file of the format

This is a simple example::
```
import math
print 'import done'

{
"usr": "username",
"pwd": "password"
}
```

**Returns**:

`HydroShare.HydroShare` object or None

<a name="hstools.auth.oauth2_authorization"></a>
#### oauth2\_authorization

```python
oauth2_authorization(authfile='~/.hs_auth')
```

performs HS authorization using OAuth2 credentials stored in
~/.hs_auth file, in a pickled binary format.

Returns hs_restclient instance or None

<a name="hstools.compat"></a>
# hstools.compat

<a name="hstools.log"></a>
# hstools.log

<a name="hstools.resource"></a>
# hstools.resource

<a name="hstools.threads"></a>
# hstools.threads

<a name="hstools.funcs"></a>
# hstools.funcs

<a name="hstools.funcs.delete"></a>
# hstools.funcs.delete

<a name="hstools.funcs.describe"></a>
# hstools.funcs.describe

<a name="hstools.funcs.add"></a>
# hstools.funcs.add

<a name="hstools.funcs.create"></a>
# hstools.funcs.create

<a name="hstools.funcs.ls"></a>
# hstools.funcs.ls

<a name="hstools.funcs.content"></a>
# hstools.funcs.content

<a name="hstools.funcs.init"></a>
# hstools.funcs.init

<a name="hstools.funcs.get"></a>
# hstools.funcs.get

<a name="hstools.progress"></a>
# hstools.progress

<a name="hstools.utilities"></a>
# hstools.utilities

<a name="hstools.utilities.get_server_url_for_path"></a>
#### get\_server\_url\_for\_path

```python
get_server_url_for_path(p)
```

gets the url corresponding to a given file or directory path
p : path to convert into a url

returns the url path for the filepath p

<a name="hstools.utilities.get_relative_path"></a>
#### get\_relative\_path

```python
get_relative_path(p)
```

gets the path relative to the jupyter home directory
p: path to convert into relative path

returns the path relative to the default jupyter home directory

<a name="hstools.hydroshare"></a>
# hstools.hydroshare

<a name="hstools.hydroshare.hydroshare"></a>
## hydroshare Objects

```python
class hydroshare()
```

<a name="hstools.hydroshare.hydroshare.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(save_dir=None, authfile='~/.hs_auth')
```

save_dir is the location that data will hs resources will be saved.

<a name="hstools.hydroshare.hydroshare.close"></a>
#### close

```python
 | close()
```

closes the connection to HydroShare

<a name="hstools.hydroshare.hydroshare.deleteResource"></a>
#### deleteResource

```python
 | deleteResource(resid)
```

Deletes a hydroshare resource

args:
-- resid: hydroshare resource id

returns:
-- True if successful, else False

<a name="hstools.hydroshare.hydroshare.getResourceMetadata"></a>
#### getResourceMetadata

```python
 | getResourceMetadata(resid)
```

Gets metadata for a specified resource.

args:
-- resid: hydroshare resource id

returns:
-- resource metadata object

<a name="hstools.hydroshare.hydroshare.createResource"></a>
#### createResource

```python
 | createResource(abstract, title, keywords=[], content_files=[])
```

Creates a hydroshare resource.

args:
-- abstract: abstract for resource (str, required)
-- title: title of resource (str, required)
-- keywords: list of subject keywords (list, default=>[])
-- content_files: data to save as resource content (list, default=>[])

returns:
-- resource_id

<a name="hstools.hydroshare.hydroshare.getResource"></a>
#### getResource

```python
 | getResource(resourceid)
```

Downloads content of a hydroshare resource.

args:
-- resourceid: id of the hydroshare resource (str)

returns:
-- None

<a name="hstools.hydroshare.hydroshare.getResourceFiles"></a>
#### getResourceFiles

```python
 | getResourceFiles(resid)
```

returns a list of files in a hydroshare resource

<a name="hstools.hydroshare.hydroshare.addContentToExistingResource"></a>
#### addContentToExistingResource

```python
 | addContentToExistingResource(resid, source, target=None)
```

Adds content files to an existing hydroshare resource.

args:
-- resid: id of an existing hydroshare resource (str)
-- source: file path to be added to resource
-- target: target path relative to the root directory of the resource

returns:
-- None

<a name="hstools.hydroshare.hydroshare.loadResourceFromLocal"></a>
#### loadResourceFromLocal

```python
 | loadResourceFromLocal(resourceid)
```

Loads the contents of a previously downloaded resource.

args:
-- resourceid: the id of the resource that has been downloaded (str)

returns:
-- {content file name: path}

