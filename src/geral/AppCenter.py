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
        file_path = "./dictionaries/"
        file_dic = file_path + self.lang + ".json"
        if os.path.exists(file_dic):
            self.dictionary = json.load(open(file_dic))
        else:
            self.dictionary = {}
    
    def translate(self, key, others = {}):
        """Return de translate of key"""
        if key in self.dictionary:
            value = self.dictionary[key]
            for i in others:
                value.replace("{" + i + "}", others[i])
            return value
        else:
            return key