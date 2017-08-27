from dynaconf import LazySettings

settings = LazySettings(
    ENVVAR_FOR_DYNACONF="QUOKKA_SETTINGS_MODULE",
    DYNACONF_NAMESPACE='QUOKKA',
    SETTINGS_MODULE_FOR_DYNACONF='settings.yml',
    YAML='.secrets.yml'  # extra yaml file override ^
)
