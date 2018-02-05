from cli.utils.services import *

class TaskService(BaseService):
  
  @classmethod
  def send(cls, method, endpoint, output):    
    request = Request(
      method = method,
      authenticated = True,
      endpoint = endpoint,
      partial_url = False,
      data = {
        "output": output
      }
    )
    
    response = cls.request(request)
    return response != None