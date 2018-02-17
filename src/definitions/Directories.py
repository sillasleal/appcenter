import os

class Directories:
    """Class containing directories definitions"""
    
    INSTALL_DIR = "%s/.AppImages" % os.environ["HOME"]

    INSTALL_BIN = "%s/.AppImages/bin" % os.environ["HOME"]
    
    TMP_DIR = "/tmp/.appimages"
    
    LOCAL_DB = "%s/.appcenter/db" % os.environ["HOME"]