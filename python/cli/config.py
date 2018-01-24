import os

# API host 
host="http://api.localhost:3030"

# Local datastore
local_directory=os.path.expanduser("~/.dvm/")
store_db="store.db"

# How many of the latests model
# versions to support per app
apps_supported_versions = 5

# Provider server port
provider_port = 3677