from jsonmodels import models, fields


class User(models.Base):
    name = fields.StringField()
    email = fields.StringField(required=True)
    wallet = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)
