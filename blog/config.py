import os
class DevelopmentConfig(object): #why does this need a name?
    SQLALCHEMY_DATABASE_URI = "postgresql://vagrant:vagrant@localhost:5432/blogful"
    DEBUG = True
