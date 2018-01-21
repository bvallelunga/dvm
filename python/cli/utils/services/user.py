import requests, config
from ..models import *

class UserService:
  
  @staticmethod
  def register(app, name, email, password, wallet):
    json = requests.post(config.host + "/v1/users/create", {
      "name": name,
      "email": email,
      "password": password,
      "wallet": wallet
    }).json()
    
    if not json["success"]:
      for error in json["errors"]:
        app.log.error(error)
    
      return None
      
    return User(json["user"])