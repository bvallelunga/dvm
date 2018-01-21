from jsonmodels import models, fields


class Metrics(models.Base):
    daily = fields.IntField()
    weekly = fields.IntField()
    monthly = fields.IntField()
    

class Stats(models.Base):
    trust = fields.IntField()


class Provider(models.Base):
    id = fields.IntField()
    endpoint = fields.StringField(required=True)
    type = fields.StringField(required=True)
    available_at = fields.BoolField(required=True)
    available_expires_at = fields.DateTimeField(required=True)
    created_at = fields.DateTimeField(required=True)
    predictions = fields.EmbeddedField(Metrics)
    predictions_sent = fields.EmbeddedField(Metrics)
    stats = fields.EmbeddedField(Stats)
