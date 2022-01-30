from os import environ

class Config:
    
    FLASK_APP           = 'wsgi.py'
    SECRET_KEY          = environ.get("FLASK_PROTOTYPE_SECRET_KEY")
    # SECRET_KEY          = 'sectetKey'
    STATIC_FOLDER       = 'static'
    TEMPLATES_FOLDER    = 'templates'

    
class DevelopmentConfig(Config):
    
    ENV                     = environ.get('FLASK_PROTOTYPE_DEV_ENV')
    DEBUG                   = True
    TESTING                 = True
    SQLALCHEMY_DATABASE_URI = environ.get('FLASK_PROTOTYPE_DEV_DB')
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/build_guild' 


    
class ProductionConfig(Config):
    
    # ENV                         = environ.get('FlaskPrototypeProdEnv')
    ENV                         = 'Production'
    DEBUG                       = False
    TESTING                     = False
    #SQLALCHEMY_DATABASE_URI    = # production db uri string #
