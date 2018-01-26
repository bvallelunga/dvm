from jsonmodels import models, fields


class ProviderMetrics(models.Base):
  daily = fields.IntField(required=True)
  weekly = fields.IntField(required=True)
  monthly = fields.IntField(required=True)
  
  @staticmethod
  def build(json):
    return ProviderMetrics(
      daily = json["daily"],
      weekly = json["weekly"],
      monthly = json["monthly"]
    )
    

class ProviderStats(models.Base):
  trust = fields.FloatField(required=True)
  
  @staticmethod
  def build(json):
    return ProviderStats(
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
  predictions = fields.EmbeddedField(ProviderMetrics, required=True)
  predictions_ent = fields.EmbeddedField(ProviderMetrics, required=True)
  stats = fields.EmbeddedField(ProviderStats, required=True)
  
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
      predictions = ProviderMetrics.build(json["predictions"]),
      predictions_sent = ProviderMetrics.build(json["predictions_sent"]),
      stats = ProviderStats.build(json["stats"])
    )