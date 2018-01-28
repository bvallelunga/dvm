from flask import Flask, request
from utils.store import store


# Create App
server = Flask(__name__)


# Routes
@server.route('/prediction', methods=['POST'])
def hello_world():
  print(request.headers.get('access-token'), store.get("access-token"), request.data)
  return ''
