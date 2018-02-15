from __future__ import absolute_import
import os
import cli.config as config
from cement.core.controller import CementBaseController, expose


class UpgradeController(CementBaseController):
  class Meta:
    label = 'upgrade'
    stacked_on = 'base'
    
  
  @expose(help="Upgrade [dvm] command line interface")
  def upgrade(self):
    os.system('pip3 install --upgrade  --user {}'.format(config.pip_package))