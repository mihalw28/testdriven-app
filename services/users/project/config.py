class BaseConfig:
    """Base configuration"""

    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Developmen configuration"""

    pass


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True


class ProductionConfiguration(BaseConfig):
    """Production configuration"""

    pass
