from . import *
from ..models.user import User

class UserService(BaseService):
  
  @classmethod
  def register(cls, name, email, password, wallet):    
    request = Request(
      method = "post",
      endpoint = "/v1/users/create",
      data = {
        "name": name,
        "email": email,
        "password": password,
        "wallet": wallet
      }
    )
    
    response = cls.request(request)
    if not response: return 
    return User.build(response["user"])