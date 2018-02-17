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


class ProviderOpenMetrics(models.Base):
  count = fields.IntField(required=True)
  limit = fields.IntField(required=True)
  
  @staticmethod
  def build(json):
    return ProviderOpenMetrics(
      count = json["count"],
      limit = json["limit"]
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
  tasks = fields.EmbeddedField(ProviderMetrics, required=True)
  open_tasks = fields.EmbeddedField(ProviderOpenMetrics, required=True)
  sent_tasks = fields.EmbeddedField(ProviderMetrics, required=True)
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
      tasks = ProviderMetrics.build(json["tasks"]),
      open_tasks = ProviderOpenMetrics.build(json["open_tasks"]),
      sent_tasks = ProviderMetrics.build(json["sent_tasks"]),
      stats = ProviderStats.build(json["stats"])
    )