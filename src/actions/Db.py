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
        self.installed_db_file = Directories.LOCAL_DB + "/installed.json"
        self.local_db_file = Directories.LOCAL_DB + "/repository.json"
    
    def insert_package(self, package_info):
        """Insert a package in db of installed apps"""
        data = self.load_installed_db()
        data[package_info["name"]] = package_info
        data[package_info["name"]]["version"] = package_info["file_download"]
        json.dump(data, open(self.installed_db_file, 'w'))
        
    def search_package(self, package_name):
        """Search packeg in installed apps"""
        data = self.load_installed_db()
        
        if package_name in data:
            return data[package_name]
        else:
            return False
   
    def load_installed_db(self):
        """Load the db of installeds apps"""
        if os.path.exists(self.installed_db_file):
            data = json.load(open(self.installed_db_file))
        else:
            json.dump({}, open(self.installed_db_file, 'w'))
            data = {}

        return data
        
    def update_local_db(self, data):
        """Update the local db"""
        json.dump(data, open(self.local_db_file, 'w'))
    
    def get_local_db(self):
        """Get the local db"""
        if os.path.exists(self.local_db_file):
            return json.load(open(self.local_db_file))
        else:
            return {}
        
        