#!/usr/bin/env python3

from __future__ import print_function
import os
import getpass
import glob
from hs_restclient import HydroShare, HydroShareAuthBasic, HydroShareAuthOAuth2
from hs_restclient import HydroShareHTTPException
from datetime import datetime as dt
import pickle
import shutil

import zipfile

from . import threads
from . import resource
from . import utilities
from . import auth
from .compat import *


class hydroshare():
    def __init__(self, save_dir=None, authfile='~/.hs_auth'):

        """
        save_dir is the location that data will hs resources will be saved.
        """

        self.hs = None
        self.content = {}

        # get the download directory from ENV_VAR or input
        if save_dir is not None:
            self.download_dir = save_dir
        else:
            self.download_dir = os.environ.get('JUPYTER_DOWNLOADS', '.')

        if not os.path.exists(self.download_dir):
            raise Exception("HS resource download directory does not exist! "
                            "Set this using the 'save_dir' input argument or "
                            "the JUPYTER_DOWNLOADS environment variable")

        # try to login via oauth
        if self.hs is None:
            try:
                self.hs = auth.oauth2_authorization(authfile)
            except Exception:
                pass

        # try to login via basic auth
        if self.hs is None:
            try:
                self.hs = auth.basic_authorization(authfile)
            except Exception:
                pass
        
        if self.hs is None:
            raise Exception(f'Authentication failed using: {authfile}')

    def close(self):
        """
        closes the connection to HydroShare
        """
        self.hs.session.close()

    def _addContentToExistingResource(self, resid, content_files):
        for f in content_files:
            self.hs.addResourceFile(resid, f)

    def getResourceMetadata(self, resid):
        """Gets metadata for a specified resource.

        args:
        -- resid: hydroshare resource id

        returns:
        -- resource metadata object
        """

        science_meta = self.hs.getScienceMetadata(resid)
        system_meta = self.hs.getSystemMetadata(resid)
        return resource.ResourceMetadata(system_meta, science_meta)

    def createResource(self, abstract, title,
                       keywords=[],
                       content_files=[]):
        """Creates a hydroshare resource.

        args:
        -- abstract: abstract for resource (str, required)
        -- title: title of resource (str, required)
        -- keywords: list of subject keywords (list, default=>[])
        -- content_files: data to save as resource content (list, default=>[])

        returns:
        -- resource_id
        """

        # make sure input files exist before doing anything else
        for f in content_files:
            if not os.path.exists(f):
                raise Exception(f'Could not find file: {f}')

        resid = None

        f = None if len(content_files) == 0 else content_files[0]

        # create the hs resource (1 content file allowed)
        resid = threads.runThreadedFunction('Creating HydroShare Resource',
                                            'Resource Created Successfully',
                                            self.hs.createResource,
                                            'CompositeResource',
                                            title=title,
                                            abstract=abstract,
                                            resource_file=f,
                                            keywords=keywords)

        # add the remaining content files to the hs resource
        try:
            if len(content_files) > 1:
                self.addContentToExistingResource(resid, content_files[1:])
        except Exception as e:
            print(e)

        return resid

    def getResource(self, resourceid):
        """Downloads content of a hydroshare resource.

        args:
        -- resourceid: id of the hydroshare resource (str)

        returns:
        -- None
        """

        dst = self.download_dir

        try:

            # download the resource (threaded)
            threads.runThreadedFunction('Downloading Resource',
                                        'Download Finished',
                                        self.hs.getResource,
                                        resourceid,
                                        destination=dst,
                                        unzip=False)

            print('Successfully downloaded resource %s' % resourceid)

        except Exception as e:
            print('Failed to retrieve '
                  'resource content from HydroShare: %s' % e)
            return None

        archive = f'{os.path.join(dst, resourceid)}.zip'
        with zipfile.ZipFile(archive, 'r') as zip_ref:
            zip_ref.extractall(f'{os.path.join(dst)}')
            os.remove(archive)

        return os.path.join(dst, resourceid)

## todo: move loading data into its own function
#        # load the resource content
#        outdir = os.path.join(dst, '%s/%s' % (resourceid, resourceid))
#        content_files = glob.glob(os.path.join(outdir, 'data/contents/*'))
#
#        content = {}
#        for f in content_files:
#            fname = os.path.basename(f)
#
#            # trim the base name relative to the data directory
#            dest_folder_name = os.path.dirname(destination).split('/')[-1]
#            f = os.path.join(dest_folder_name,
#                             os.path.relpath(f, dest_folder_name))
#
#            content[fname] = f
#
#        # update the content dictionary
#        self.content.update(content)


    def addContentToExistingResource(self, resid, content):
        """Adds content files to an existing hydroshare resource.

        args:
        -- resid: id of an existing hydroshare resource (str)
        -- content: files paths to be added to resource (list)

        returns:
        -- None
        """

        threads.runThreadedFunction('Adding Content to Resource',
                                    'Successfully Added Content Files',
                                    self._addContentToExistingResource,
                                    resid, content)


    def loadResourceFromLocal(self, resourceid):
        """Loads the contents of a previously downloaded resource.

         args:
         -- resourceid: the id of the resource that has been downloaded (str)

         returns:
         -- {content file name: path}
        """

        resdir = utilities.find_resource_directory(resourceid)
        if resdir is None:
            print(f'Could not find any resource matching the id {resource}')
            return

        # create search paths.
        # Need to check 2 paths due to hs_restclient bug #63.
        search_paths = [os.path.join(resdir, f'{resourceid}/data/contents/*'),
                        os.path.join(resdir, 'data/contents/*')]

        content = {}
        found_content = False
        for p in search_paths:
            content_files = glob.glob(p)
            if len(content_files) > 0:
                found_content = True
                print(f'Downloaded content is located at: {resdir}')
                print(f'Found {len(content_files)} content file(s)')
            for f in content_files:
                fname = os.path.basename(f)
                content[fname] = f
        if len(content.keys()) == 0:
            print('Did not find any content files for resource id: '
                  '{resourceid}')

        self.content = content

    def getContentFiles(self, resourceid):
        """Gets the content files for a resource that exists on the
           Jupyter Server

        args:
        -- resourceid: the id of the hydroshare resource

        returns:
        -- {content file name: path}
        """

        content = utilities.get_hs_content(resourceid)
        return content

    def getContentPath(self, resourceid):
        """Gets the server path of a resources content files.

        args:
        -- resourceid: the id of the hydroshare resource

        returns:
        -- server path the the resource content files
        """

        path = utilities.find_resource_directory(resourceid)
        if path is not None:
            return os.path.join(path, resourceid, 'data/contents')
