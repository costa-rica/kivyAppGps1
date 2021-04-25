import logging
import sys

import kivy
from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.utils import platform
from plyer import gps
import requests
import json
from kivy.clock import Clock
from config import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

class MyGrid(Widget):
    activity=ObjectProperty(None)
    latitude = ObjectProperty(None)
    longitude = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.app = MyApp.get_running_app()


    def start_btn(self,*args):
        self.recorded_activity = self.activity.text
        self.start_send_data = Clock.schedule_interval(self.send_data,2)
        #how can i send data without clock?
        #would this be a terrible idea, because i would get an unnecessary amount of data?

    def stop_btn(self, *args):
        self.start_send_data.cancel()

    def send_data(self, *args):
        json_data = {
            "Activity": self.recorded_activity,
            "Latitude":self.latitude.text,
            "Longitude":self.longitude.text
            }
        res = requests.post(url=self.app.firebase_url, json = json_data)


class MyApp(App):
    firebase_url = Config().firebase_url + '.json'
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.my_grid = None

    def on_start(self):
        if platform == 'android' or platform == 'ios':
            gps.configure(on_location=self.on_gps_location)
            gps.start()
        else:
            logger.debug("GPS is not supported outside of Android and iOS.")

    def on_gps_location(self, **kwargs):
        self.grid.latitude.text = str(kwargs.get("lat"))
        self.grid.longitude.text = str(kwargs.get("lon"))
        logger.debug("The latitude is %r", self.grid.latitude)
        # return self.latitude

    def build(self):
        self.grid = MyGrid()
        return self.grid

if __name__=="__main__":
    MyApp().run()
