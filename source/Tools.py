from . import *

class Tools:
    
    
    def save_obj(obj, name, folder_path = Params.SAVED_FILES_FOLDER):
        '''
        saves a certain object as a pickle file
        *obj*: the object to be saved
        *name*: the name of the file where the object will be saved
        *folder_path*: the path to the folder where the data should be saved
        '''
        with open("{}/".format(folder_path) + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            
    
    
    def load_obj(name, folder_path = Params.SAVED_FILES_FOLDER):
        '''
        loads a specific intermediate file
        *name*: the name of the file to be loaded (str)
        *folder_path*: the path to the folder where the data are saved
        '''
        with open('{}/{}.pkl'.format(folder_path, name), 'rb') as f:
            return pickle.load(f)
