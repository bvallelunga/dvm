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
  

class Task(models.Base):
  task_id = fields.IntField()
  provider_id = fields.IntField()
  app_id = fields.IntField()
  model_id = fields.IntField()
  input = None
  callback = fields.EmbeddedField(TaskCallback, required=True)
  
  @staticmethod
  def build(json):
    prediction = Task(
      task_id = json["task_id"],
      provider_id = json["provider_id"],
      app_id = json["app_id"],
      model_id = json["model_id"],
      callback = TaskCallback.build(json["callback"]),
    )
    
    prediction.input = json["input"]
    return prediction