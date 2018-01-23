import os

# API Host 
host="http://api.localhost:3030"

# Local Data Store
local_directory=os.path.expanduser("~/.dvm/")
store_db="store.db"


# Array of app ids to automatically 
# enroll in. We will download and prepare
# the app's models.
apps_default_enrolled = []


# How many of the latests model
# versions to support per app
apps_supported_versions = 5