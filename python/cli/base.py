from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

VERSION = '0.0.1'
BANNER = """
Doppler Virtual Machine v%s
Copyright (c) 2018 Doppler Foundation
""" % VERSION

class BaseController(CementBaseController):
  class Meta:
    label = 'base'
    description = "Doppler Virtual Machine CLI"
    arguments = [
      ( ['-v', '--version'], dict(action='version', version=BANNER) ),
    ]

  @expose(hide=True)
  def default(self):
    self.app.args.print_help()
