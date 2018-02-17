import sys

from geral.AppCenter import AppCenter
from actions.Repository import Repository

class Cmd(AppCenter):
    """
    Author 
    ----------
    Sillas S. Leal<sillas.s.leal@gmail.com>
    
    Summary line.
    
    Cmd
    """
    
    def __init__(self):
        """"""
        AppCenter.__init__(self)
        self.repository = Repository()
        
    def start(self):
        """"""
        if len(sys.argv) < 2:
            print self.translate("invalid_params")
            exit(100)
            
        action = sys.argv[1]
        
        if len(sys.argv) > 2:
            package = sys.argv[2]
        else:
            package = "nothing"
            
        actions = {
            "find": self.repository.show_application_info,
#            "download": self.repository.download,
            "install": self.repository.install,
            "remove": self.repository.remove
        }
        
        if action not in actions:
            print self.translate("invalid_action")
            exit(100)
        
        actions[action](package)