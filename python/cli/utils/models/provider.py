from jsonmodels import models, fields


class Metrics(models.Base):
  daily = fields.IntField()
  weekly = fields.IntField()
  monthly = fields.IntField()
  
  @staticmethod
  def build(json):
    return Metrics(
      daily = json["daily"],
      weekly = json["weekly"],
      monthly = json["monthly"]
    )
    

class Stats(models.Base):
  trust = fields.IntField()
  
  @staticmethod
  def build(json):
    return Stats(
      trust = json["trust"]
    )
  

class Provider(models.Base):
  id = fields.IntField()
  endpoint = fields.StringField(required=True)
  type = fields.StringField(required=True)
  available = fields.BoolField(required=True)
  available_at = fields.DateTimeField(required=True)
  available_expires_at = fields.DateTimeField(required=True)
  created_at = fields.DateTimeField(required=True)
  predictions = fields.EmbeddedField(Metrics, required=True)
  predictions_ent = fields.EmbeddedField(Metrics, required=True)
  stats = fields.EmbeddedField(Stats, required=True)
  
  @staticmethod
  def build(json):
    return Provider(
      id = json["id"],
      endpoint = json["endpoint"],
      type = json["type"],
      available = json["available"],
      available_at = json["available_at"],
      available_expires_at = json["available_expires_at"],
      created_at = json["created_at"],
      predictions = Metrics.build(json["predictions"]),
      predictions_sent = Metrics.build(json["predictions_sent"]),
      stats = Stats.build(json["stats"])
    )