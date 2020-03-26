import os
import pickle


class Storage:
    path: str

    def __init__(self, path):
        self.path = path

    def get_data(self):
        if not os.path.exists(self.get_path()):
            return None

        # check if file is not empty
        if os.path.getsize(self.get_path()) > 0:
            # get data from pickle
            with open(self.get_path(), 'rb') as pkl:
                return pickle.load(pkl)
        else:
            return None

    def set_data(self, data):
        # create the directory and file if it doesn't exist.
        if not os.path.exists(self.get_path()):
            os.makedirs(os.path.dirname(self.get_path()))

        with open(self.get_path(), 'wb') as output:
            pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

    def get_path(self):
        return self.path
