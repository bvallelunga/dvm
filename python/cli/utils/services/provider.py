from . import *
from ..models.provider import *


class ProviderService(BaseService):

  @classmethod
  def register(cls, app, endpoint):
    request = Request(
      app = app,
      method = "post",
      endpoint = "/v1/providers/create",
      authenticated = True,
      data = {
        "endpoint": endpoint,
        "type": "server"
      }
    )
    
    response = cls.request(request)
    if not response: return    
    return Provider.build(response["provider"])
    
    
  
  @classmethod
  def availability(cls, app, provider, available):
    request = Request(
      app = app,
      method = "post",
      authenticated = True,
      endpoint = "/v1/providers/" + provider.id + "/availability",
      data = {
        "available": available
      }
    )
    
    response = cls.request(request)
    if not response: return    
    return Provider.build(response["provider"])
    