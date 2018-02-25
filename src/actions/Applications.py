import os
import sys
import requests
from lxml import html
from shutil import copyfile
import mmap

from geral.AppCenter import AppCenter
from definitions.Directories import Directories
from actions.Repository import Repository
from actions.Db import Db

from packages.Git import Git

class Applications(AppCenter):
    """
    Author 
    ----------
    Sillas S. Leal<sillas.s.leal@gmail.com>
    
    Summary line.
    
    Applications
    """
    
    def __init__(self):
        """"""
        AppCenter.__init__(self)
        self.repository = Repository()
        self.db = Db()
    
    def download(self, package, version = False, destination = os.getcwd()):
        """Download a package"""
        print self.translate("download_package", {"package": package["name"]})
        info = False
        
        for data in package['links']:
            if data['type'] == 'Install' or data['type'] == 'Download':
                page = requests.get(data['url'])
                webpage = html.fromstring(page.content)
                
                for link in webpage.xpath('//a/@href'):
                    
                    if (data['url'] + "/download" in link or "/releases/download" in link) and ".appimage" in link.lower():
                        info = {"file": "", "info": {}}
                        link_download =  "https://github.com/%s" % link
                        info["file"] = link.split('/')[-1]
                        info["info"] = package
                        info["info"]["file_download"] = info["file"]
                        dest_appimage = destination + "/" + info["file"]
                        self.create_dir(destination)
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
                        return info
        return info
        
    
    def install(self, package, version = False):
        """Method that install a package"""
        if self.db.search_package(package):
            print self.translate("package_installed")
            return
        
        print self.translate("searching_package", {"package": package})
        package_info = self.repository.get_application_info(package, True)
        
        if not package_info:
            print "\033[93m" + self.translate("package_not_found") + "\033[0m"
            print "\033[93m" + self.translate("use_correct_name") + "\033[0m"
            return
        
        result = self.download(package_info, version, Directories.TMP_DIR)
        
        if result:
            print "Download concluido"
            self.create_dir(Directories.INSTALL_DIR)
            self.create_dir(Directories.INSTALL_BIN)
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
        
    def remove(self):
        """"""
        
    def add_bin_to_path(self):
        """Add bin folder to path"""
        profile = os.environ["HOME"] + "/.profile"
        if os.path.exists(profile):
            f = open(profile)
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            path_string = "PATH=$PATH:" + Directories.INSTALL_BIN
            if s.find(path_string) == -1:
                with open(profile, "a") as myfile:
                    myfile.write(path_string)
        
    def gen_desktop_link(self, file):
        """Generate the desktop file"""
    
    def gen_sym_link(self, file_dest, name):
        """Generate the symbolic link of AppImage"""
        if not os.path.exists(Directories.INSTALL_BIN + "/" + name):
            os.system("ln -s %s %s" % (file_dest, Directories.INSTALL_BIN + "/" + name))