import os
import json

class AppCenter:
    """
    Author 
    ----------
    Sillas S. Leal<sillas.s.leal@gmail.com>
    
    Summary line.
    
    AppCenter
    """

    def __init__(self):
        """Constructor"""
        lang = os.environ["LANG"]
        self.lang = lang
        file_path = "%s/../dictionaries/" % os.path.dirname(__file__)
        file_dic = file_path + self.lang + ".json"
        if os.path.exists(file_dic):
            self.dictionary = json.load(open(file_dic))
        else:
            self.dictionary = {}
    
    def translate(self, key, others = {}):
        """Return the translate of key"""
        if key in self.dictionary:
            if type(key) == list:
                #pluralization
                var = key[2]
                qt = others[var]
                if qt != 1:
                    value = self.dictionary[key[1]]
                else:
                    value = self.dictionary[key[0]]
            else:
                #normal key
                value = self.dictionary[key]

            for i in others:
                value = value.replace("{" + i + "}", others[i])

            return value
        else:
            return key
        
    def create_dir(self, directory):
        """Create a directory on the system"""
        if not os.path.exists(directory):
            os.system("mkdir -p %s" % directory)
            
    def print_info(self, package):
        """Print the package info"""
        print "\n\x1b[6;30;42m" + self.translate("details_package", {"package": package["name"]}) + "\x1b[0m"
        for i in package:
            if type(package[i]) != list:
                print i, ":", package[i]