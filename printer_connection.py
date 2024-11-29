import os
from bambu_connect import BambuClient, PrinterStatus
import time
import asyncio


class Bambu:
    def __init__(self):
        self.__hostname = os.getenv('PRINTER_IP')
        self.__access_code = os.getenv('PRINTER_ACCESS_CODE')
        self.__serial_number = os.getenv('PRINTER_SERIAL_NUMBER')

        self.__bambu_client = BambuClient(self.__hostname, self.__access_code, self.__serial_number)

        self.__bambu_client.start_watch_client(self.__on_watch_client_trigger,self.__on_watch_client_connect)
        self.__capture_next_status = True
        self.__latest_status = None
        self.__callback_count = 0

    def __on_watch_client_trigger(self, msg : PrinterStatus):
        if self.__capture_next_status:
            self.__capture_next_status = False
            self.__latest_status = msg
        self.__callback_count += 1
        print(f"Callback count: {self.__callback_count}")

    def __on_watch_client_connect(self):
        print("Watch client connected to printer")

    async def get_status(self):

        self.__capture_next_status = True
        while self.__latest_status is None:
            await asyncio.sleep(0.1)
        copy = self.__latest_status
        self.__latest_status = None
        self.__capture_next_status = False
        # self.__bambu_client.stop_watch_client()
        print(copy)
        return copy

    def get_camera_frame(self):
        return self.__bambu_client.capture_camera_frame()