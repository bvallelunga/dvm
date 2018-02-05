from cli.utils.services import *
from cli.utils.models.provider import Provider
from cli.utils.models.model import Model


class ProviderService(BaseService):

  @classmethod
  def register(cls, endpoint):
    request = Request(
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
  def availability(cls, available):
    provider_id = cls.provider_helper()
    if not provider_id: return
    
    request = Request(
      method = "post",
      authenticated = True,
      endpoint = "/v1/providers/{}/availability".format(provider_id),
      data = {
        "available": available
      }
    )
    
    response = cls.request(request)
    if not response: return    
    return Provider.build(response["provider"]) 
    
  
  @classmethod
  def enroll_app(cls, app_id, enroll):
    provider_id = cls.provider_helper()
    if not provider_id: return
    
    request = Request(
      method = "post",
      authenticated = True,
      endpoint = "/v1/providers/{}/apps/{}/enroll".format(provider_id, app_id),
      data = {
        "enroll": enroll
      }
    )
    
    response = cls.request(request)
    if not response: return
    if not enroll: return True
    return list(map(lambda m: Model.build(m), response["models"]))
    
    
  @classmethod
  def enroll_model(cls, app_id, version, enroll):
    provider_id = cls.provider_helper()
    if not provider_id: return
    
    request = Request(
      method = "post",
      authenticated = True,
      endpoint = "/v1/providers/{}/apps/{}/models/{}/enroll".format(provider_id, app_id, version),
      data = {
        "enroll": enroll
      }
    )
    
    response = cls.request(request)
    if not response: return
    return True

    