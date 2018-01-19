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
        self.dictionary = json.load(open(file_path + self.lang + ".json"))
    
    def translate(self, key, others = {}):
        """Return de translate of key"""
        if key in self.dictionary:
            return self.dictionary[key]
        else:
            return key