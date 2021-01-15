from flask import Blueprint, \
                  render_template,\
                  url_for,\
                  request,\
                  redirect,\
                  session

from logging import getLogger


logger = getLogger('flask.app')

route =  Blueprint('webhook', __name__, url_prefix='/webhook')
