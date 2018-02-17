import os
import json

from geral.AppCenter import AppCenter
from definitions.Directories import Directories

class Db(AppCenter):
    """"""
    
    def __init__(self):
        """"""
        AppCenter.__init__(self)
        if not os.path.exists(Directories.LOCAL_DB):
            os.system("mkdir -p %s" % Directories.LOCAL_DB)
        self.instaled_db_file = Directories.LOCAL_DB + "/instaled.json"
        self.local_db_file = Directories.LOCAL_DB + "/repository.json"
    
    def insert_package(self, package_info):
        """Insert a package in db of instaled apps"""
        if os.path.exists(self.instaled_db_file):
            data = json.load(open(self.instaled_db_file))
        else:
            json.dump({}, open(self.instaled_db_file, 'w'))
            data = {}
        data[package_info["name"]] = package_info
        data[package_info["name"]]["version"] = package_info["file_download"]
        json.dump(data, open(self.instaled_db_file, 'w'))
        
    def search_package(self, package_name):
        """Search packeg in instaled apps"""
        
        
    def update_local_db(self, data):
        """Update the local db"""
        json.dump(data, open(self.local_db_file, 'w'))
    
    def get_local_db(self):
        """Get the local db"""
        if os.path.exists(self.local_db_file):
            return json.load(open(self.local_db_file))
        else:
            return {}
        
        