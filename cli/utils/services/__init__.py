from __future__ import absolute_import
import requests, simplejson as json
import cli.config as config
from cli.utils.logger import logger
from cli.utils.timer import ReturnTimer
from cli.utils.store import store


class Request:
  
  method = None
  endpoint = None
  authenticated = False
  partial_url = True
  data={}
  headers={}
  
  def __init__(self, method, endpoint, authenticated=False, data={}, headers={}, partial_url=True):
    self.method = method
    self.endpoint = endpoint
    self.authenticated = authenticated
    self.data = data
    self.headers = headers
    self.partial_url = partial_url



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
    endpoint = request.endpoint
    
    if request.partial_url:
      endpoint = config.host + endpoint
    
    try:
      if request.method == "post":
        request.headers["Content-Type"] = "application/json"
        return requests.post(endpoint, data=json.dumps(request.data, use_decimal=True), headers=request.headers).json()
        
      elif request.method == "get":
        return requests.get(endpoint, params=request.data, headers=request.headers).json()    
          
    except Exception as e:
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
