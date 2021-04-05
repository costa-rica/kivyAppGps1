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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

print("Start::: This is running on %r",platform)


class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        # self.my_grid = None

    def on_start(self):
        if platform == 'android' or platform == 'ios':
            gps.configure(on_location=self.on_gps_location)
            gps.start()
        else:
            # self.my_grid.latitude ='21'
            logger.debug("GPS is not supported outside of Android and iOS.")

    def on_gps_location(self, **kwargs):
        self.latitude = kwargs.get("lat")
        self.longitude = kwargs.get("lon")
        logger.debug("The latitude is %r", self.latitude)

    def build(self):
        return MyGrid()


class MyGrid(Widget):
    name=ObjectProperty(None)
    email=ObjectProperty(None)
    latitude = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.app = MyApp.get_running_app()
        # self.gps_coordinates = None
        self.latitude.text = self.app.latitude
        # self.longitude = None
        # self.app.my_grid = self

    def btn(self):
        print('Name: ', self.name.text, 'email: ',self.email.text)
        self.name.text=''
        self.email.text=''
        # if self.app.latitude is not None:
        #     self.gps_coordinates = (self.app.latitude, self.app.longitude)


if __name__=="__main__":
    MyApp().run()
