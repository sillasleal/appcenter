from packages.Package import Package
from geral.AppCenter import AppCenter

class Git(Package, AppCenter):
    """"""
    
    def __init__(self):
        """"""
        AppCenter.__init__(self)
        self.url = "https://appimage.github.io"
        self.url_screenshot = "%s/database" % self.url

        