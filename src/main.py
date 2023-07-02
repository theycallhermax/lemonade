import sys
import gi
import json
import requests
import urllib.request
import http

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gdk, Gio

class LemonadeWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        self.headerbar = Adw.HeaderBar.new()
        self.set_titlebar(self.headerbar)

        home_button = Gtk.Button()
        home_button.connect("clicked", self.home)
        stack.add_titled(home_button, "home", "Home")

        # e_button = Gtk.Button()
        # stack.add_titled(e_button, "e", "e")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        # self.refresh_button = Gtk.Button.new_from_icon_name("view-refresh")
        # self.refresh_button.connect("clicked", self.refresh)
        # self.refresh_button.set_tooltip_text("Refresh")
        self.headerbar.set_title_widget(stack_switcher)
        # self.headerbar.pack_start(self.refresh_button)

        self.set_default_size(700, 500)
        self.set_title("Lemonade")

        self.home()

    def home(self):
        self.sw = Gtk.ScrolledWindow()
        self.sw.set_hexpand(False)
        self.sw.set_vexpand(True)

        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_top = 20,
            margin_bottom = 20,
            margin_start = 20,
            margin_end = 20
        )
        self.sw.set_child(self.box)
        self.set_child(self.sw)

        self.listbox = Gtk.ListBox.new()
        self.listbox.get_style_context().add_class("boxed-list")
        self.listbox.props.hexpand = True
        self.listbox.props.vexpand = True
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_show_separators(True)
        self.box.append(self.listbox)

        self.refresh()

    def refresh(self, *args):
        self.communities = requests.get("https://lemmy.ml/api/v3/community/list?sort=Hot").json()
        for community in self.communities["communities"]:
            box = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                margin_top = 20,
                margin_bottom = 20,
                margin_start = 20,
                margin_end = 20
            )
            self.listbox.append(box)

            label = Gtk.Label.new()
            avatar = Adw.Avatar.new(40, community["community"]["title"], True)

            if "icon" in community["community"]:
                try:
                    name = community["community"]["icon"].split("/")[-1]
                    urllib.request.urlretrieve(community["community"]["icon"], f"/tmp/{name}")
                    avatar.set_custom_image(Gdk.Texture.new_from_file(Gio.File.new_for_path(f"/tmp/{name}")))
                except:
                    pass
            else:
                pass

            if not "description" in community["community"]:
                label.set_markup(f"""<big><b>{community["community"]["title"]}</b></big> <small>!{community["community"]["name"]}@{community["community"]["actor_id"].split("/")[2]}</small>""")
            else:
                split = community["community"]["description"].split("\n")[0]
                label.set_markup(f"""<big><b>{community["community"]["title"]}</b></big>  <small>!{community["community"]["name"]}@{community["community"]["actor_id"].split("/")[2]}</small>
{split}""")

            label.props.margin_start = 5
            label.props.hexpand = True
            label.props.wrap = True
            label.set_halign(Gtk.Align.START)
            label.set_selectable(False)

            # refresh_button = Gtk.Button.new_from_icon_name("network-wireless")
            # refresh_button.connect("clicked", self.refresh)
            # refresh_button.set_tooltip_text("Refresh")
            # box.append(refresh_button)
            box.append(avatar)
            box.append(label)

class Lemonade(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = LemonadeWindow(application=app)
        self.win.present()

def main(version):
    app = Lemonade(application_id="ml.mdwalters.Lemonade")
    app.run(sys.argv)

