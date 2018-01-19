import os
import requests
import json

from geral.AppCenter import AppCenter
from definitions.Urls import Urls
from definitions.Directories import Directories

class Repository(AppCenter):
    """
    Author 
    ----------
    Sillas S. Leal<sillas.s.leal@gmail.com>
    
    Summary line.
    
    Repository
    """
    
    FILE_DB = Directories.LOCAL_DB + "/db.json"
    
    def read(self):
        """Read the local db"""
        self.db = json.load(open(self.FILE_DB))
    
    def update(self):
        """Update the local repositories"""
        response = requests.get(Urls.PUBLIC_REPO)
        self.db = response.json()
        os.system("mkdir -p %s" % Directories.LOCAL_DB)
        json.dump(self.db, open(self.FILE_DB, 'w'))
        
    def download(self, package, version = False):
        """"""
        info = False
        self.read()
        for line in self.db['items']:
            if package.lower() == line['name'].lower():
                info = line
        print info
        
    def get_application_info(self, package):
        """"""
        info = False
        self.read()
        for line in self.db['items']:
            if package.lower() in line['name'].lower():
                info = line
                print line["name"] if line["name"] is not None else ""
                print line["description"] if line["description"] is not None else ""
                print line["license"] if line["license"] is not None else ""
                print ""
        
        if not info:
            print self.translate("package_not_found")
            
        return info
            
    def search_update(self, package):
        """"""
        
        