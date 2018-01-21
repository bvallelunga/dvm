import requests, config
from ..models.user import User

class UserService:
  
  @staticmethod
  def register(app, name, email, password, wallet):    
    response = requests.post(config.host + "/v1/users/create", json={
      "name": name,
      "email": email,
      "password": password,
      "wallet": wallet
    }).json()
    
    if not response["success"]:
      for error in response["errors"]:
        app.log.error(error)

      return None
      
    return User(
      name = response["user"]["name"],
      email = response["user"]["email"],
      wallet = response["user"]["wallet"],
      created_at = response["user"]["created_at"]
    )