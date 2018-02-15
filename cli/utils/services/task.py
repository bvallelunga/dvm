from __future__ import absolute_import
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
    
    
  @classmethod
  def error(cls, method, endpoint, message):  
    print(method, endpoint, message)  
    request = Request(
      method = method,
      authenticated = True,
      endpoint = endpoint,
      partial_url = False,
      data = {
        "message": message
      }
    )
    
    response = cls.request(request)
    return response != None