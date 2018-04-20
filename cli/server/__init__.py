from __future__ import absolute_import
from flask import Flask, request
from cli.utils.models.task import Task
from cli.utils.store import store
from persistqueue import FIFOSQLiteQueue
from cli.server.worker import Worker
import cli.config as config
import simplejson as json

server = Flask(__name__)
apps = None
queue = None
worker = None

@server.route('/prediction', methods=['POST'])
def receive_prediction():
  if request.headers.get('access-token') != store.get("access-token"):
    return error_handler("Invalid access-token")
  
  data = request.get_json(silent=True)
  task = Task.build(data)
  
  if str(task.app_id) not in apps:
    return error_handler("Provider is not enrolled in this app")
  
  if str(task.model_id) not in apps[str(task.app_id)]:
    return error_handler("Provider is not enrolled in model")
  
  if config.provider_use_queue:
    queue.put(data)
    return json.dumps({ "success": True })
  
  try:
    return json.dumps({ 
      "success": True,
      "output": worker.predict(task)
    })
    
  except Exception as e:  
    return json.dumps({
      "success": False,
      "error": str(e)
    }, use_decimal=True)
  

def error_handler(error):  
  return (
    json.dumps({
      "success": False,
      "error": error
    }, use_decimal=True), 
    403
  )
  
  
def run(host, port, debug):
  global apps
  global queue
  global worker
  
  apps = store.get("apps", {})
  queue = FIFOSQLiteQueue(path=config.queue_db, multithreading=True)
  worker = Worker(queue, store)
  
  if config.provider_use_queue:
    worker.start()
  
  server.run(host=host, port=port, debug=debug)
