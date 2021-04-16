from os import environ

class Config:
    
    FLASK_APP           = 'wsgi.py'
    SECRET_KEY          = environ.get("FlaskPrototypeSecretKey")
    STATIC_FOLDER       = 'static'
    TEMPLATES_FOLDER    = 'templates'

    
class DevelopmentConfig(Config):
    
    ENV                     = environ.get('FlaskPrototypeDevEnv')
    DEBUG                   = True
    TESTING                 = True
    SQLALCHEMY_DATABASE_URI = environ.get('FlaskPrototypeDevDB')  #'mysql://root:root@localhost/build_guild' 

    
class ProductionConfig(Config):
    
    ENV                         = environ.get('FlaskPrototypeProdEnv')
    DEBUG                       = False
    TESTING                     = False
    #SQLALCHEMY_DATABASE_URI    = # production db uri string #
