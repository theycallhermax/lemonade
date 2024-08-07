use adw::prelude::*;
use gio::ActionEntry;
// use glib::clone;
// use gtk::glib;

pub fn init(app: &adw::Application) {
	let builder = gtk::Builder::from_string(include_str!("ui/window.ui"));
	let window = builder
		.object::<adw::ApplicationWindow>("window")
		.expect("Couldn't get window");

	#[cfg(feature = "devel")]
	window.add_css_class("devel");

	window.set_application(Some(app));
	window.present();

	let action_quit = ActionEntry::builder("quit")
		.activate(|window: &adw::ApplicationWindow, _, _| {
			window.close();
		})
		.build();
	window.add_action_entries([action_quit]);
}
