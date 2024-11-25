import os
from bambu_connect import BambuClient


class Bambu:
    def __init__(self):
        self.__hostname = os.getenv('PRINTER_IP')
        self.__access_code = os.getenv('PRINTER_ACCESS_CODE')
        self.__serial_number = os.getenv('PRINTER_SERIAL_NUMBER')

        self.__BambuClient = BambuClient(self.__hostname, self.__access_code, self.__serial_number)

    def get_status(self):
        return self.__BambuClient.get_status() # unfinished