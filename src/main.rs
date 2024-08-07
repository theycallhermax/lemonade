use gtk::{glib, prelude::*};
mod window;

fn main() -> glib::ExitCode {
	let app = adw::Application::builder()
		.application_id("ml.mdwalters.Lemonade")
		.build();

	app.connect_activate(window::init);

	app.set_accels_for_action("win.quit", &["<Ctrl>Q"]);

	app.run()
}
