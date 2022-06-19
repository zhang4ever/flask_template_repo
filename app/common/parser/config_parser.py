class ConfigParser:

    def as_int(self, key: str, default=None, from_remote = False):
        return self.__get_env(
            key=key,
            default=default,
            converter=int,
            from_remote=from_remote
        )

    def __get_env(self, key: str, default: str, converter=None, from_remote=False):
        value = self.__get_value(key, default, from_remote)
        if converter is not None:
            if converter == 'list':
                return eval(value)
            return converter(value)

    def __get_value(self, key: str, default = None, from_remote = False):
        value = self.__get_value_from_remote(key) if from_remote else None
        return value if value else default

    def __get_value_from_remote(self, key):
        return ''
