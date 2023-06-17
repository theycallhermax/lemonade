import sys
import gi
import json
import requests

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_default_size(400, 500)
        self.set_title("Lemonade")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.box)

        self.list = requests.get("https://lemmy.ml/api/v3/community/list?sort=Hot").json()
        for post in self.list["communities"]:
            self.box.append(Gtk.Label(label=post["community"]["title"]))

class Lemonade(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = Lemonade(application_id="ml.mdwalters.Lemonade")
app.run(sys.argv)

