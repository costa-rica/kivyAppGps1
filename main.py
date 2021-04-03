import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from plyer import gps

class MyGrid(Widget):
    name=ObjectProperty(None)
    email=ObjectProperty(None)
    app = MyApp.get_running_app()
    self.latParam.text=app.latParam

    print('did this work for latParam:::', app.latParam)


    def btn(self):
        print('Name: ', self.name.text, 'email: ',self.email.text)
        self.name.text=''
        self.email.text=''


class MyApp(App):
    def on_start(self):
        gps.configure(on_location=self.on_gps_location)
        gps.start()

    def on_gps_location(self, **kwargs):
        self.latParam=kwargs['lat']
        print('print only latitude:::',kwargs['lat'])
        print('print all kwargs:::',kwargs)

    def build(self):
        return MyGrid()


if __name__=="__main__":
    MyApp().run()
