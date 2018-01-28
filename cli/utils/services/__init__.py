import requests, config, colorlog
from ..timer import ReturnTimer
from ..store import store

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s: %(message)s'))
logger = colorlog.getLogger('services')
logger.addHandler(handler)


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
    endpoint = config.host + request.endpoint
    
    try:
      if request.method == "post":
        response = requests.post(endpoint, json=request.data, headers=request.headers).json()
        
      elif request.method == "get":
        response = requests.get(endpoint, params=request.data, headers=request.headers).json()    
          
    except:
      def retry_request():
        return cls.request(request)
    
      logger.error("Lost connection to Doppler, trying to reestablish...")
      return ReturnTimer(config.provider_availability_backoff, retry_request).start()
      
    
    # Check for errors
    if not response["success"]:
      for error in response["errors"]:
        logger.error(error)

      return None
        
    # Return response
    return response
    
  
  
  @staticmethod
  def login_error():
    logger.error("Please login first! dvm auth login [wallet]")
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
