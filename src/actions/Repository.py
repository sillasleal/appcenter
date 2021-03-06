import os
import requests
import json

from geral.AppCenter import AppCenter
from definitions.Urls import Urls
from definitions.Directories import Directories
from actions.Db import Db

class Repository(AppCenter):
    """
    Author 
    ----------
    Sillas S. Leal<sillas.s.leal@gmail.com>
    
    Summary line.
    
    Repository
    """
    
    def __init__(self):
        """"""
        AppCenter.__init__(self)
        self.db = Db()
    
    def update(self):
        """Update the local repositories"""
        if not os.path.exists(Directories.REPO_FILE):
            repos = [Urls.PUBLIC_REPO]
            json.dump(repos, open(Directories.REPO_FILE, 'w'))
        else:
            repos = json.load(open(Directories.REPO_FILE))

        data = {}
        for url in repos:
            if "items" in data:
                tmp = requests.get(url).json()
                data["items"] = data["items"] + tmp["items"]
            else:
                data = requests.get(url).json()
            
        self.db.update_local_db(data)
        
    def get_application_info(self, package, is_exact = False):
        """Get informations about the package"""
        info = False
        self.update()
        for line in self.db.get_local_db()['items']:
            if is_exact:
                if package == line['name']:
                    info = line
                    break
            else:
                if package.lower() in line['name'].lower() or ("description" in line and package.lower() in line['description'].lower()):
                    if not info:
                        info = []
                    info.append(line)
    
        return info
        
    
    def show_application_info(self, package):
        """Show package info"""
        print self.translate("get_package_info", {"package": package})
        items = self.get_application_info(package)
        if items and len(items) > 0:
            for info in items:
                self.print_info(info)
        else:
            print "\033[93m" + self.translate("package_not_found") + "\033[0m"
            
            