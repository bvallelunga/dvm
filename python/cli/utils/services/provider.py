from . import *
from ..models.provider import Provider
from ..models.model import Model


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
  def availability(cls, app, available):
    provider_id = app.store.get("provider")
    
    if not provider_id:
      return cls.login_error(app)
    
    request = Request(
      app = app,
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
  def enroll_app(cls, app, app_id, enroll):
    provider_id = app.store.get("provider")
    
    if not provider_id:
      return cls.login_error(app)
    
    request = Request(
      app = app,
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
  def enroll_model(cls, app, app_id, version, enroll):
    provider_id = app.store.get("provider")
    
    if not provider_id:
      return cls.login_error(app)
    
    request = Request(
      app = app,
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

    