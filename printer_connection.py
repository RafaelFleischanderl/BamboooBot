from bambu_connect import BambuClient, PrinterStatus
import time
import asyncio


class Bambu:

    def __init__(self, ip, access_code, serial_number):
        self.__hostname = ip
        self.__access_code = access_code
        self.__serial_number = serial_number
        self.__is_connected_to_printer = False

    def try_reconnect(self):
        try:
            self.__bambu_client = BambuClient(self.__hostname, self.__access_code, self.__serial_number)
            self.__is_connected_to_printer = True
            self.__start_watch_client()
        except Exception as e:
            print(f"Failed to connect to bambu printer")
            self.__is_connected_to_printer = False

    def is_connected(self):
        return self.__is_connected_to_printer

    def __start_watch_client(self):
        self.__bambu_client.start_watch_client(self.__on_watch_client_trigger,self.__on_watch_client_connect)
        self.__status_future = None  # for status to transform callback of BambuClient into awaitable Promise

    def __on_watch_client_trigger(self, msg : PrinterStatus):
        if self.__status_future and not self.__status_future.done():
            self.__status_future.set_result(msg)

    def __on_watch_client_connect(self):
        print("Watch client connected to printer")

    async def get_status(self):
        self.__status_future = asyncio.Future()
        status = await self.__status_future
        self.__status_future = None
        # print(status)
        return status

    def get_camera_frame(self):
        return self.__bambu_client.capture_camera_frame()