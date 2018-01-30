from threading import Thread
from utils.models.prediction import Prediction
import json 


def _process(prediction):
  print(prediction)


def _worker(queue):
  while True:
    data = queue.get().decode("utf-8")
    _process(Prediction.build(json.loads(data)))
    queue.task_done()


def start(queue):
  def _start():
    _worker(queue)
  
  thread = Thread(target=_start)
  thread.daemon = True
  thread.start()