import os

class Directories:
    """Class containing directories definitions"""
    
    INSTALL_DIR = "%s/.AppImages" % os.environ["HOME"]
    
    LOCAL_DB = "%s/.appcenter/db" % os.environ["HOME"]