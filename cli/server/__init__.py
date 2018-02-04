from flask import Flask, request
from utils.models.task import Task
from utils.store import store
from persistqueue import FIFOSQLiteQueue
from server.worker import Worker
import config, json


queue = FIFOSQLiteQueue(path=config.queue_db, multithreading=True)
server = Flask(__name__)
apps = store.get("apps", {})
Worker(queue, store).start()


@server.route('/prediction', methods=['POST'])
def revieve_prediction():
  if request.headers.get('access-token') != store.get("access-token"):
    return error_handler("Invalid access-token")
  
  data = request.get_json(silent=True)
  task = Task.build(data)
  
  if str(task.app_id) not in apps:
    return error_handler("Provider is not enrolled in this app")
  
  if str(task.model_id) not in apps[str(task.app_id)]:
    return error_handler("provider is not enrolled in model")
  
  queue.put(data)
  return json.dumps({ "success": True })
  

def error_handler(error):  
  return (
    json.dumps({
      "success": False,
      "error": error
    }), 
    403
  )