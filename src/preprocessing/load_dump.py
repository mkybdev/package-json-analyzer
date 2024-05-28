import os
import pickle
from appdirs import user_cache_dir

def load_dump(name):
    
    cache_dir = os.path.join(user_cache_dir('package-json-analyzer', 'pja'), name)
    cache_file_path = os.path.join(cache_dir, 'data.pkl')

    if os.path.exists(cache_file_path):
        with open(cache_file_path, 'rb') as cache_file:
            loaded_data = pickle.load(cache_file)
            print("Loaded data from cache.")
        return loaded_data
    else:
        return None