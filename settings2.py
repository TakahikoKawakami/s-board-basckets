# coding: UTF-8

import sys
from database import db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from authorizations import controllers, models

    
