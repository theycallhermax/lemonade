import sys
import gi
import json
import requests

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw

class LemonadeWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(self.headerbar)

        self.refresh_button = Gtk.Button.new_from_icon_name("view-refresh")
        self.refresh_button.connect("clicked", self.refresh)
        self.refresh_button.set_tooltip_text("Refresh")
        self.headerbar.pack_start(self.refresh_button)

        self.set_default_size(400, 500)
        self.set_title("Lemonade")

        self.sw = Gtk.ScrolledWindow()
        self.sw.set_hexpand(False)
        self.sw.set_vexpand(True)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sw.set_child(self.box)
        self.set_child(self.sw)

        self.listbox = Gtk.ListBox.new()
        self.listbox.props.hexpand = True
        self.listbox.props.vexpand = True
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_show_separators(True)
        self.box.append(self.listbox)

        self.refresh()

    def refresh(self, *args):
        self.list = requests.get("https://lemmy.ml/api/v3/community/list?sort=Hot").json()
        for post in self.list["communities"]:
            box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
            self.listbox.append(box)

            label = Gtk.Label.new()
            label.set_markup(f"""{post["community"]["title"]}
<small>{post["community"]["description"]}</small>""")
            label.props.margin_start = 5
            label.props.hexpand = True
            label.props.wrap = True
            label.set_halign(Gtk.Align.START)
            label.set_selectable(True)
            box.append(label)

class Lemonade(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = LemonadeWindow(application=app)
        self.win.present()

app = Lemonade(application_id="ml.mdwalters.Lemonade")
app.run(sys.argv)

