from __future__ import absolute_import
from cli.utils.models.wallet import Wallet


class WalletService:
  
  @staticmethod
  def generate():
    # TODO: Generate Wallet Address & Private Key
    return Wallet(
      address="ru8o_supsnjqvxpecqnpd6lyyzvqjcyn5drt7baa",
      private_key="abcabcabcabcabcabc"
    )