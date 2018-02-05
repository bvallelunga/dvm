import json, os.path
import cli.config as config

class Store:
  
  datastore = {}
  
  def __init__(self):
    os.makedirs(config.local_directory, exist_ok=True)

    if os.path.exists(config.store_db):
      with open(config.store_db, 'r') as f:
        self.datastore = json.load(f)
        f.close()
    
    else:
      self._update()

  
  def get(self, key, default=None):
    if key in self.datastore:
      return self.datastore[key]
      
    return default
    
    
  def set(self, key, value):
    self.datastore[key] = value
    self._update()
    
  
  def _update(self):
    with open(config.store_db, 'w') as f:
      json.dump(self.datastore, f)
      f.close()


store = Store()