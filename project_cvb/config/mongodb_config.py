# db_config.py
from mongoengine import connect
from project_cvb.config.settings import Settings


def initialize_mongodb():
  connect(host=Settings().MONGODB_URI)
