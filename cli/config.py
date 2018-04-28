import os

# Upgrade
pip_package = "git+https://github.com/DopplerFoundation/dvm.git"

# API host 
host = os.getenv('DVM_HOST', "https://api.doppler.market")

# Local datastore
local_directory = os.path.expanduser("~/.dvm/")
store_db = os.path.join(local_directory, "store.db")
app_store = os.path.join(local_directory, "apps")
queue_db = os.path.join(local_directory, "queue")
server_out_log = os.path.join(local_directory, "out.log")
server_error_log = os.path.join(local_directory, "error.log")
server_pid = os.path.join(local_directory, "dvm.pid")

# How many of the latests model
# versions to support per app
apps_supported_versions = 1

# Provider server port
provider_host = "0.0.0.0"
provider_port = 3677
provider_use_queue = False

# If Doppler server is down, wait
# 5 seconds for it to come back online
provider_availability_backoff = 5

# Give the provider a little buffer
# before having to checkin with Doppler again
provider_availability_buffer = 5
