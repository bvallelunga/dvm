import requests, config
from ..models.provider import *


class ProviderService:
  
  @staticmethod
  def register(app, endpoint):
    if not app.store.get("access-token"):
      app.log.error("Please login first! dvm auth login [wallet]")
      return
     
    response = requests.post(config.host + "/v1/providers/create", json={
      "endpoint": endpoint,
      "type": "server"
    }, headers={
      "access-token": app.store.get("access-token")
    }).json()
    
    if not response["success"]:
      for error in response["errors"]:
        app.log.error(error)

      return None
        
    return Provider.build(response["provider"])