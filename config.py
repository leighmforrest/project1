class Config:
    """Common configurations"""
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'prodcution': ProductionConfig
}
