import os

# API host 
host = os.getenv('DVM_HOST', "https://api.doppler.market")


# Local datastore
local_directory = os.path.expanduser("~/.dvm/")
store_db = os.path.join(local_directory, "store.db")
app_store = os.path.join(local_directory, "apps")
queue_db = os.path.join(local_directory, "queue.db")

# How many of the latests model
# versions to support per app
apps_supported_versions = 5

# Provider server port
provider_host = "0.0.0.0"
provider_port = 3677

# If Doppler server is down, wait
# 5 seconds for it to come back online
provider_availability_backoff = 5

# Give the provider a little buffer
# before having to checkin with Doppler again
provider_availability_buffer = 5