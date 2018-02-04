from jsonmodels import models, fields


class Wallet(models.Base):
  address = fields.StringField()
  private_key = fields.StringField(required=True)
  
  @staticmethod
  def build(json):
    return User(
      address = json["address"],
      private_key = json["private_key"]
    )