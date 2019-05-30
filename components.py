import json
import os

jsonPATH = 'path'

class ConfigureData(object):
    def __init__(self):
        self.filename = "./config.json"
        self.data = {jsonPATH: ''}

    def Load(self):
        if (not os.path.isfile(self.filename)):
            return False

        with open(self.filename) as json_data_file:
            self.data = json.load(json_data_file)
        return True

    def Save(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.data, outfile)

    def GetPath(self):
        return self.data[jsonPATH]

    def SetPath(self, path):
        self.data[jsonPATH] = path
