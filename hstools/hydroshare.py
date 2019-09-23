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

from . import threads
from . import resource
from . import utilities
from . import auth
from .compat import *


class hydroshare():
    def __init__(self, save_dir=None):

        """
        save_dir is the location that data will hs resources will be saved.
        """

        self.hs = None
        self.content = {}

        # get the download directory from ENV_VAR or input
        self.download_dir = save_dir if save_dir is not None else \
        os.environ.get('JUPYTER_DOWNLOADS', '.')
        if not os.path.exists(self.download_dir):
            raise Exception("HS resource download directory does not exist! "
                            "Set this using the 'save_dir' input argument or "
                            "the JUPYTER_DOWNLOADS environment variable")

        # try to login via oauth
        if self.hs is None:
            self.hs = auth.oauth2_authorization()

        # try to login via basic auth
        if self.hs is None:
            self.hs = auth.basic_authorization()

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

    def createResource(self, abstract, title, derivedFromId=None,
                       keywords=[], resource_type='GenericResource',
                       content_files=[], public=False):
        """Creates a hydroshare resource.

        args:
        -- abstract: abstract for resource (str, required)
        -- title: title of resource (str, required)
        -- derivedFromId: id of parent hydroshare resource (str, default=>None)
        -- keywords: list of subject keywords (list, default=>[])
        -- resource_type: type of resource to create (str, default=>
                                                     'GenericResource')
        -- content_files: data to save as resource content (list, default=>[])
        -- public: resource sharing status (bool, default=>False)

        returns:
        -- None
        """

        # query the hydroshare resource types and make sure that
        # resource_type is valid
        restypes = {r.lower(): r for r in self.hs.getResourceTypes()}
        try:
            res_type = restypes[resource_type]
        except KeyError:
            print('<b style="color:red;">[%s] is not a valid '
                         'HydroShare resource type.</p>' % resource_type)
            return None

        # get the 'derived resource' metadata
        if derivedFromId is not None:
            try:
                # update the abstract and keyword metadata
                meta = self.getResourceMetadata(derivedFromId)

                abstract = meta.abstract \
                    + '\n\n[Modified in JupyterHub on %s]\n%s' \
                    % (dt.now(), abstract)

                keywords = set(keywords + meta.keywords)
            except:
                print('<b style="color:red;">Encountered an error '
                             ' while setting the derivedFrom relationship '
                             ' using id=%s. Make sure this resource is '
                             ' is accessible to your account. '
                             % derivedFromId)
                print('<a href=%s target="_blank">%s<a>' %
                             ('https://www.hydroshare.org/resource/%s'
                              % derivedFromId, 'View the "DerivedFrom" '
                              'Resource'))
                return None

        f = None if len(content_files) == 0 else content_files[0]

        # create the hs resource (1 content file allowed)
        resid = threads.runThreadedFunction('Creating HydroShare Resource',
                                            'Resource Created Successfully',
                                            self.hs.createResource,
                                            resource_type=res_type,
                                            title=title,
                                            abstract=abstract,
                                            resource_file=f,
                                            keywords=keywords)

        print('Resource id: %s' % resid)
        print('<a href=%s target="_blank">%s<a>' %
                     ('https://www.hydroshare.org/resource/%s'
                      % resid, 'Open Resource in HydroShare'))

        # add the remaining content files to the hs resource
        try:
            if len(content_files) > 1:
                self.addContentToExistingResource(resid, content_files[1:])
        except Exception as e:
            print(e)

    def getResource(self, resourceid, destination='.'):
        """Downloads content of a hydroshare resource.

        args:
        -- resourceid: id of the hydroshare resource (str)
        -- destination: path to save resource, default
                        /user/[username]/notebooks/data (str)

        returns:
        -- None
        """

        default_dl_path = self.download_dir
        dst = os.path.abspath(os.path.join(default_dl_path, destination))
        download = True

        # check if the data should be overwritten
        dst_res_folder = os.path.join(dst, resourceid)
        if os.path.exists(dst_res_folder):
            print('This resource already exists in your userspace.')
            utilities.tree(dst_res_folder)
            res = input('\nDo you want to overwrite these data [Y/n]? ')
            if res != 'n':
                shutil.rmtree(dst_res_folder)
            else:
                download = False

        # re-download the content if desired
        if download:
            try:

                # download the resource (threaded)
                threads.runThreadedFunction('Downloading Resource',
                                            'Download Finished',
                                            self.hs.getResource,
                                            resourceid,
                                            destination=dst,
                                            unzip=True)

                print('Successfully downloaded resource %s' % resourceid)

            except Exception as e:
                print('Failed to retrieve '
                      'resource content from HydroShare: %s' % e)
                return None

        # load the resource content
        outdir = os.path.join(dst, '%s/%s' % (resourceid, resourceid))
        content_files = glob.glob(os.path.join(outdir, 'data/contents/*'))

        content = {}
        for f in content_files:
            fname = os.path.basename(f)

            # trim the base name relative to the data directory
            dest_folder_name = os.path.dirname(destination).split('/')[-1]
            f = os.path.join(dest_folder_name,
                             os.path.relpath(f, dest_folder_name))

            content[fname] = f

        # update the content dictionary
        self.content.update(content)


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
        search_paths = [os.path.join(resdir, f'{resourceid}/data/contents/*',
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
