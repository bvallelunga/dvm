from flask import Flask


class Server(Flask):
  
  def __init__(self):
    super(Server, self).__init__(__name__)