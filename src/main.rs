mod settings;
mod utils;
mod ui;

use eframe;

fn main() -> eframe::Result<()> {
    let options = eframe::NativeOptions::default();
    eframe::run_native(
        "Forgedy",
        options,
        Box::new(|cc| Box::new(ui::App::new(cc))),
    )
}

pub struct AppState;


