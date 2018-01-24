from jsonmodels import models, fields


class AppMetrics(models.Base):
  daily = fields.IntField(required=True)
  weekly = fields.IntField(required=True)
  monthly = fields.IntField(required=True)
  
  @staticmethod
  def build(json):
    return AppMetrics(
      daily = json["daily"],
      weekly = json["weekly"],
      monthly = json["monthly"]
    )
  

class App(models.Base):
  id = fields.IntField(required=True)
  category_id = fields.IntField()
  enrolled_providers = fields.IntField()
  versions = fields.IntField()
  name = fields.StringField(required=True)
  description = fields.StringField(required=True)
  created_at = fields.DateTimeField(required=True)
  predictions = fields.EmbeddedField(AppMetrics, required=True)
  
  @staticmethod
  def build(json):
    return App(
      id = json["id"],
      category_id = json["category_id"],
      enrolled_providers = json["enrolled_providers"],
      versions = json["versions"],
      name = json["name"],
      description = json["description"],
      created_at = json["created_at"],
      predictions = AppMetrics.build(json["predictions"])
    )
