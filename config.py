from os import environ

class Config:
    
    FLASK_APP           = 'wsgi.py'
    SECRET_KEY          = environ.get("FlaskPrototypeSecretKey")
    # SECRET_KEY          = 'sectetKey'
    STATIC_FOLDER       = 'static'
    TEMPLATES_FOLDER    = 'templates'

    
class DevelopmentConfig(Config):
    
    ENV                     = environ.get('FlaskPrototypeDevEnv')
    DEBUG                   = True
    TESTING                 = True
    SQLALCHEMY_DATABASE_URI = environ.get('FlaskPrototypeDevDB')
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/build_guild' 


    
class ProductionConfig(Config):
    
    # ENV                         = environ.get('FlaskPrototypeProdEnv')
    ENV                         = 'Production'
    DEBUG                       = False
    TESTING                     = False
    #SQLALCHEMY_DATABASE_URI    = # production db uri string #
