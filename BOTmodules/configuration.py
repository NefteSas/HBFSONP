import configparser
import os

CONFIG_FILE_PATH: str = "config/configuration.ini"

class ConfigurationOvermind:
    parser = configparser.ConfigParser()

    def __init__(self) -> None:
        self.parser = self._read_or_create_configuration_file()

    def _create_configuration_file(self) -> configparser.ConfigParser:
        parser: configparser.ConfigParser = configparser.ConfigParser()

        parser["FUNDAMENTAL"] = {"TOKEN": "", "DEVS": "", "DEVMODE": False}
        
        with open(CONFIG_FILE_PATH, "w") as configfile:
            parser.write(configfile)

        """FIXME: Исправить потенциальную ошибку, когда при отсутсвии папки config бот ложиться"""

        print("\n CREATED CONFIG FILE")

        return parser

    def getCurrentMode(self) -> bool:
        print(self.parser["FUNDAMENTAL"]["DEVMODE"])
        return self.parser["FUNDAMENTAL"]["DEVMODE"]

    def _read_configuration_file(self) -> configparser.ConfigParser:
        parser: configparser.ConfigParser = configparser.ConfigParser()
        parser.read(CONFIG_FILE_PATH)

        print("\n READED CONFIG FILE")

        return parser

    def _read_or_create_configuration_file(self) -> configparser.ConfigParser:
        if os.path.exists(CONFIG_FILE_PATH):
            return self._read_configuration_file()
        else:
            return self._create_configuration_file()

    def getBotDevs(self) -> list:
        return self.parser["FUNDAMENTAL"]["DEVS"].split(',')

    def getBotToken(self) -> str:
        token: str = self.parser["FUNDAMENTAL"]["TOKEN"]

        if token == "":
            raise Exception(f"TOKEN IS NULL. CHECK {CONFIG_FILE_PATH}")
        else:
            return token
