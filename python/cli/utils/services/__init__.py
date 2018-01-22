import requests, config


class Request:
  
  app = None
  method = None
  endpoint = None
  authenticated = False
  data={}
  headers={}
  
  def __init__(self, app, method, endpoint, authenticated=False, data={}, headers={}):
    self.app = app
    self.method = method
    self.endpoint = endpoint
    self.authenticated = authenticated
    self.data = data
    self.headers = headers



class BaseService:
  
  method = "post"
  endpoint = ""
  access_required = False
  
  @staticmethod
  def request(request):
    # Check for authentication
    if request.authenticated:
      if not request.app.store.get("access-token"):
        request.app.log.error("Please login first! dvm auth login [wallet]")
        return None
      
      else:
        request.headers["access-token"] = request.app.store.get("access-token")
     
    # Make requests
    endpoint = config.host + request.endpoint
    
    if request.method == "post":
      response = requests.post(endpoint, json=request.data, headers=request.headers).json()
      
    elif request.method == "get":
      response = requests.get(endpoint, json=request.data, headers=request.headers).json()
    
    # Check for errors
    if not response["success"]:
      for error in response["errors"]:
        request.app.log.error(error)

      return None
        
    # Return response
    return response
    