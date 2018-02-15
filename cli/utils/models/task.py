from jsonmodels import models, fields


class TaskCallback(models.Base):
  method = fields.StringField(required=True)
  url = fields.StringField(required=True)
  
  @staticmethod
  def build(json):
    return TaskCallback(
      method = json["method"],
      url = json["url"]
    )
    
    
class TaskCallbacks(models.Base):
  success = fields.EmbeddedField(TaskCallback, required=True)
  error = fields.EmbeddedField(TaskCallback, required=True)
  
  @staticmethod
  def build(json):
    return TaskCallbacks(
      success = TaskCallback.build(json["success"]),
      error = TaskCallback.build(json["error"])
    )
  

class Task(models.Base):
  task_id = fields.IntField()
  provider_id = fields.IntField()
  app_id = fields.IntField()
  model_id = fields.IntField()
  input = None
  callbacks = fields.EmbeddedField(TaskCallbacks, required=True)
  
  @staticmethod
  def build(json):
    prediction = Task(
      task_id = json["task_id"],
      provider_id = json["provider_id"],
      app_id = json["app_id"],
      model_id = json["model_id"],
      callbacks = TaskCallbacks.build(json["callbacks"]),
    )
    
    prediction.input = json["input"]
    return prediction