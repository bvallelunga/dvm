from flask import Flask, request, jsonify
from utils.models.prediction import Prediction
from utils.store import store

  
server = Flask(__name__)
apps = store.get("apps", {})


@server.route('/prediction', methods=['POST'])
def revieve_prediction():
  if request.headers.get('access-token') != store.get("access-token"):
    return error_handler("Invalid access-token")
  
  data = request.get_json(silent=True)
  prediction = Prediction.build(data)
  
  if str(prediction.app_id) not in apps:
    return error_handler("Provider is not enrolled in this app")
  
  if str(prediction.model_id) not in apps[str(prediction.app_id)]:
    return error_handler("provider is not enrolled in model")
  
  
  return jsonify({ "success": True })
  

def error_handler(error):
  return (
    jsonify({
      "success": False,
      "error": error
    }), 
    403
  )