import sys
#import readline

from geral.AppCenter import AppCenter
from actions.Repository import Repository
from actions.Applications import Applications

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
        self.applications = Applications()
        self.repository = Repository()
    
    def completer(self, text, state):
        """Autocomplete of params"""
        options = [i for i in commands if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None
        
    def start(self):
        """Start the app"""
#        args = self.get_list_by_args()
#        readline.parse_and_bind("tab: complete")
#        readline.set_completer(selfcompleter)
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
            "find-package": self.applications.find,
            "install": self.applications.install,
            "installeds": self.applications.installeds,
            "remove": self.applications.remove
        }
        
        if action not in actions:
            print self.translate("invalid_action")
            exit(100)
        
        actions[action](package)
        
    def get_list_by_args(self):
        """Get a list parans by args"""
        ret = {}
        key = ""
        qt = 0
        for arg in sys.argv:
            if arg[0:2] == "--":
                key = arg[2:len(arg)]
            else:
                value = arg
                if len(key) > 0:
                    ret[key] = value
                else:
                    ret[qt] = value
                    
            qt = qt + 1
            
        return ret