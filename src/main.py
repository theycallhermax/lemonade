import sys
import gi
import json
import requests
import urllib.request
import http
import os

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gdk, Gio

class LemonadeWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        MENU_XML = """
            <?xml version="1.0" encoding="UTF-8"?>
                <interface>
                    <menu id="app-menu">
                        <section>
                            <item>
                                <attribute name="action">win.login</attribute>
                                <attribute name="label" translatable="yes">_Log in</attribute>
                            </item>
                        </section>
                        <section>
                            <item>
                                <attribute name="action">win.about</attribute>
                                <attribute name="label" translatable="yes">_About</attribute>
                            </item>
                            <item>
                                <attribute name="action">win.quit</attribute>
                                <attribute name="label" translatable="yes">_Quit</attribute>
                                <attribute name="accel">&lt;Primary&gt;Q</attribute>
                            </item>
                        </section>
                    </menu>
                </interface>
        """

        try:
            os.mkdir(os.path.join(f"{os.environ['XDG_RUNTIME_DIR']}/app/ml.mdwalters.Lemonade", "cache"))
        except FileExistsError as e:
            print(e)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        self.headerbar = Adw.HeaderBar.new()
        self.headerbar.get_style_context().add_class("flat")
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

        quit_action = Gio.SimpleAction.new("quit", None) # look at MENU_XML win.quit
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action) # (self window) == win in MENU_XML

        about_action = Gio.SimpleAction.new("about", None) # look at MENU_XML win.about
        about_action.connect("activate", self.on_about)
        self.add_action(about_action) # (self window) == win in MENU_XML

        login_action = Gio.SimpleAction.new("login", None) # look at MENU_XML win.about
        login_action.connect("activate", self.on_login)
        self.add_action(login_action) # (self window) == win in MENU_XML

        self.menu_button = Gtk.MenuButton.new()
        self.headerbar.pack_end(self.menu_button) # or pack_start
        menu = Gtk.Builder.new_from_string(MENU_XML, -1).get_object("app-menu")
        self.menu_button.set_icon_name("open-menu-symbolic")
        self.menu_button.set_menu_model(menu)

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
        self.clamp = Adw.Clamp.new()
        self.listbox.get_style_context().add_class("boxed-list")
        self.clamp.set_child(self.listbox)
        self.listbox.props.hexpand = True
        self.listbox.props.vexpand = True
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_show_separators(True)
        self.box.append(self.clamp)

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
                    print(f"Downloading icon for {community['community']['title']}")
                    name = community["community"]["icon"].split("/")[-1]
                    urllib.request.urlretrieve(community["community"]["icon"], f"{os.environ['XDG_RUNTIME_DIR']}/app/ml.mdwalters.Lemonade/cache/{name}")
                    avatar.set_custom_image(Gdk.Texture.new_from_file(Gio.File.new_for_path(f"{os.environ['XDG_RUNTIME_DIR']}/app/ml.mdwalters.Lemonade/cache/{name}")))
                    print(f"Successfully downloaded icon for {community['community']['title']}")
                except:
                    print(f"Error getting icon for {community['community']['title']}")
                    pass
            else:
                print(f"No icon found for {community['community']['title']}, skipping")
                pass

            if not "description" in community["community"]:
                label.set_markup(f"""<big><b>{community["community"]["title"]}</b></big> <small>!{community["community"]["name"]}@{community["community"]["actor_id"].split("/")[2]}</small>""")
            else:
                split = community["community"]["description"].split("\n")[0].replace("&", "&amp;").replace("<", "&what;").replace(">", "&what;")
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
    def on_quit(self, action, param=None):
        exit()

    def on_about(self, action, param=None):
        self.about = Adw.AboutWindow.new()

        self.about.set_application_name("Lemonade")
        self.about.set_application_icon("ml.mdwalters.Lemonade")
        self.about.set_version("2023.09.08")
        self.about.set_developer_name("M.D. Walters")
        self.about.set_debug_info(f"""Lemonade version: {self.about.get_version()}
libadwaita version: {Adw.get_major_version()}.{Adw.get_minor_version()}.{Adw.get_micro_version()}
GTK version: {Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}""")
        self.about.set_developers(["M.D. Walters https://github.com/mdwalters"])
        self.about.set_artists(["daudix-UFO https://github.com/daudix-UFO"])
        self.about.set_issue_url("https://github.com/mdwalters/lemonade/issues/new")
        self.about.set_website("https://github.com/mdwalters/lemonade")
        self.about.set_license_type(Gtk.License.MIT_X11)
        self.about.set_comments("Follow discussions on Lemmy")
        self.about.set_release_notes("""<ul>
            <li>New icon by daudix-UFO on GitHub!</li>
            <li>Update <code>requests</code> dependency</li>
        </ul>""")

        self.about.show()

    def on_login(self, action, param=None):
        status = Adw.StatusPage().new()
        status.set_icon_name("arrow-into-box-symbolic")
        status.set_title("Log in")
        status.show()

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

