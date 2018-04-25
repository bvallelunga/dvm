from jsonmodels import models, fields


class ModelMetrics(models.Base):
  daily = fields.IntField(required=True)
  weekly = fields.IntField(required=True)
  monthly = fields.IntField(required=True)
  
  @staticmethod
  def build(json):
    return ModelMetrics(
      daily = json["daily"],
      weekly = json["weekly"],
      monthly = json["monthly"]
    )
    

class ModelStats(models.Base):
  trust = fields.FloatField(required=True)
  precision = fields.FloatField(required=True)
  recall = fields.FloatField(required=True)
  
  @staticmethod
  def build(json):
    return ModelStats(
      trust = json["trust"],
      precision = json["precision"],
      recall = json["recall"]
    )
    
    
class ModelUrls(models.Base):
  raw = fields.StringField(required=True)
  
  @staticmethod
  def build(json):
    return ModelUrls(
      raw = json["raw"],
    )
  

class Model(models.Base):
  app_id = fields.IntField(required=True)
  version = fields.IntField(required=True)
  enrolled_providers = fields.IntField()
  input_scheme = None
  output_scheme = None
  created_at = fields.DateTimeField(required=True)
  urls = fields.EmbeddedField(ModelUrls, required=True)
  tasks = fields.EmbeddedField(ModelMetrics, required=True)
  stats = fields.EmbeddedField(ModelStats, required=True)
  
  @staticmethod
  def build(json):
    model = Model(
      app_id = json["app_id"],
      version = json["version"],
      enrolled_providers = json["enrolled_providers"],
      urls = ModelUrls.build(json["urls"]),
      created_at = json["created_at"],
      tasks = ModelMetrics.build(json["tasks"]),
      stats = ModelStats.build(json["stats"])
    )
    model.input_scheme = json["input_scheme"]
    model.output_scheme = json["output_scheme"]
    return model
