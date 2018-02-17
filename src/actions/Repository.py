import os
import sys
import requests
from lxml import html
import json
from shutil import copyfile

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
        response = requests.get(Urls.PUBLIC_REPO)
        self.db.update_local_db(response.json())
        
    def download(self, package, version = False, destination = os.getcwd()):
        """Download a package"""
        info = False
        self.update()
        for line in self.db.get_local_db()['items']:
            if package.lower() == line['name'].lower():
                print " "
                
                info = {"file": "", "info": {}};
                for data in line['links']:
                    if data['type'] == 'Install' or data['type'] == 'Download':
#                        print line
#                        print data['url']
                        page = requests.get(data['url'])
                        webpage = html.fromstring(page.content)
                        
                        for link in webpage.xpath('//a/@href'):
                            if (data['url'] + "/download" in link or "/releases/download" in link) and ".AppImage" in link:
                                link_download =  "https://github.com/%s" % link
                                info["file"] = link.split('/')[-1]
                                info["info"] = line
                                info["info"]["file_download"] = info["file"]
                                dest_appimage = destination + "/" + info["file"]
                                if not os.path.exists(destination):
                                    os.system("mkdir -p %s" % destination)
                                r = requests.get(link_download, stream=True)
                                total_length = r.headers.get('content-length')
                                print "Downloading " + info["file"]
                                with open(dest_appimage, 'wb') as f:
                                    dl = 0
                                    total_length = int(total_length)
                                    for chunk in r.iter_content(chunk_size=1024): 
                                        if chunk: 
                                            dl += len(chunk)
                                            f.write(chunk)
                                            done = int(50 * dl / total_length)
                                            perc = 100 * float(dl)/float(total_length)
                                            total = '=' * done
                                            un_total = ' ' * (50-done)
                                            sys.stdout.write("\r%d of %d (%.1f%s) [%s%s]" % (dl, total_length, perc, "%", total, un_total))
                                            sys.stdout.flush()
                                if not version:
                                    break
                break
                
        if not info:
            print self.translate("package_not_found")
        
        return info
    
    def install(self, package, version = False):
        """Method that install a package"""
        result = self.download(package, version, Directories.TMP_DIR)
        if result:
            print "Download concluido"
            if not os.path.exists(Directories.INSTALL_DIR):
                os.system("mkdir -p %s" % Directories.INSTALL_DIR)
            if not os.path.exists(Directories.INSTALL_BIN):
                os.system("mkdir -p %s" % Directories.INSTALL_BIN)
            print Directories.TMP_DIR + "/" + result["file"]
            file_dest = Directories.INSTALL_DIR + "/" + result["info"]["name"] + ".AppImage"
            copyfile(Directories.TMP_DIR + "/" + result["file"], file_dest)
            os.system("chmod +x %s" % file_dest)
            self.gen_sym_link(file_dest, result["info"]["name"].lower())
            self.add_bin_to_path()
            self.gen_desktop_link(file_dest)
            self.db.insert_package(result["info"])
            print self.translate("success_install")
        else:
            print self.translate("filed_install")
    
    def gen_desktop_link(self, file):
        """Generate the desktop file"""
        
            
    def add_bin_to_path(self):
        """Add bin folder to path"""
    
    def gen_sym_link(self, file_dest, name):
        """Generate the symbolic link of AppImage"""
        if not os.path.exists(Directories.INSTALL_BIN + "/" + name):
            os.system("ln -s %s %s" % (file_dest, Directories.INSTALL_BIN + "/" + name))
        

    def remove(self):
        """Remove a package of system"""
        
    def get_application_info(self, package, is_exact = False):
        """Get informations about the packege"""
        info = False
        self.update()
        for line in self.db.get_local_db()['items']:
            if package.lower() in line['name'].lower() and not is_exact:
                if not info:
                    info = []
                info.append(line)
            elif package.lower() == line['name'].lower() and is_exact:
                info = line
                break
        
        return info
        
    
    def show_application_info(self, package):
        """Show package info"""
        items = self.get_application_info(package)
        if len(items) > 0:
            for info in items:
                print "\n%s '%s'" % (self.translate("details_package"), info["name"])
                for i in info:
                    if type(info[i]) != list:
                        print i, ":", info[i]
        else:
            print self.translate("package_not_found")
            
            