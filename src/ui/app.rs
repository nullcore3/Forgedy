use eframe::egui;


use super::pages::text_utils::TextUtilsPage;
use super::pages::settings::SettingsPage;

pub struct App {
    page: Page,
    text_utils: TextUtilsPage,
    settings: SettingsPage,
}


#[derive(Clone, Copy, PartialEq, Eq)]
enum Page {
    TextUtils,
    Settings,
    About,
}

impl App {
    pub fn new(_cc: &eframe::CreationContext<'_>) -> Self {
        Self {
            page: Page::TextUtils,
            text_utils: TextUtilsPage::default(),
            settings: SettingsPage::default(),
        }
    }
}


impl eframe::App for App {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::TopBottomPanel::top("top").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.selectable_value(&mut self.page, Page::TextUtils, "Text Utilities");
                ui.selectable_value(&mut self.page, Page::Settings, "Settings");
                ui.selectable_value(&mut self.page, Page::About, "About");
            });
        });

        egui::CentralPanel::default().show(ctx, |ui| match self.page {
            Page::TextUtils => self.text_utils.ui(ui),
            Page::Settings => self.settings.ui(ui),
            Page::About => self.page_about(ui),
        });
    }
}

impl App {
    fn page_settings(&mut self, ui: &mut egui::Ui) {
        ui.heading("Settings");
        ui.label("Theme/font computation will load forgedy_settings.json once dependencies are finalized.");
    }

    fn page_about(&mut self, ui: &mut egui::Ui) {
        ui.heading("About Forgedy");
        ui.label("Porting Python utilities to Rust (utils split per util). UI migration to egui.");
    }
}


