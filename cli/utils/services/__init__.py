import requests, config
from ..logger import logger
from ..timer import ReturnTimer
from ..store import store


class Request:
  
  method = None
  endpoint = None
  authenticated = False
  data={}
  headers={}
  
  def __init__(self, method, endpoint, authenticated=False, data={}, headers={}):
    self.method = method
    self.endpoint = endpoint
    self.authenticated = authenticated
    self.data = data
    self.headers = headers



class BaseService:
  
  @classmethod
  def request(cls, request):
    # Check for authentication
    if request.authenticated:
      token = cls.token_helper()
      if not token: return
      request.headers["access-token"] = token
     
    # Make requests
    response = cls._request(request)
      
    
    # Check for errors
    if not response["success"]:
      for error in response["errors"]:
        logger.error(error)

      return None
        
    # Return response
    return response
    
  
  @classmethod  
  def _request(cls, request, init_request=True):
    endpoint = config.host + request.endpoint
    
    try:
      if request.method == "post":
        return requests.post(endpoint, json=request.data, headers=request.headers).json()
        
      elif request.method == "get":
        return requests.get(endpoint, params=request.data, headers=request.headers).json()    
          
    except:
      def retry_request():
        return cls._request(request, init_request=False)
        
      if init_request: logger.error("Lost connection to Doppler, trying to reestablish...")
      response = ReturnTimer(config.provider_availability_backoff, retry_request).start()
      if init_request: logger.info("Restored connection to Doppler")
      return response
  
  
  @staticmethod
  def login_error():
    logger.error("Please login first!\n$dvm auth login [wallet]")
    return None
    
    
  @classmethod
  def provider_helper(cls):
    provider = store.get("provider")
    if provider: return provider
    return cls.login_error()
    
    
  @classmethod
  def token_helper(cls):
    token = store.get("access-token")
    if token: return token
    return cls.login_error()
