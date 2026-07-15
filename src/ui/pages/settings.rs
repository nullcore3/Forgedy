use eframe::egui;

use crate::settings;

fn merge_json(mut base: serde_json::Value, patch: serde_json::Value) -> serde_json::Value {
    match (base, patch) {
        (serde_json::Value::Object(mut b), serde_json::Value::Object(p)) => {
            for (k, pv) in p {
                let entry = b.entry(k).or_insert(serde_json::Value::Null);
                if !entry.is_null() {
                    *entry = merge_json(entry.take(), pv);
                } else {
                    *entry = pv;
                }
            }
            serde_json::Value::Object(b)
        }
        (_, p) => p,
    }
}


pub struct SettingsPage {
    theme_mode: String,
    font_size_offset: i32,

    // keep last loaded to avoid writing until user edits
    last_loaded: bool,
}

impl Default for SettingsPage {
    fn default() -> Self {
        Self {
            theme_mode: "System".to_string(),
            font_size_offset: 0,
            last_loaded: false,
        }
    }
}

impl SettingsPage {
    pub fn ui(&mut self, ui: &mut egui::Ui) {
        ui.heading("Settings");

        // Minimal settings port: reads forgedy_settings.json and allows updating FontSizeOffset + ThemeMode.
        // Styling (ctk themes) isn't applied in egui yet; but values are persisted.
        if !self.last_loaded {
            if let Ok(s) = settings::load_settings("forgedy_settings.json") {
                self.theme_mode = s.theme.custom.color_theme_mode.clone();
                self.font_size_offset = s.theme.custom.font_size_offset;
            }
            self.last_loaded = true;
        }

        ui.separator();
        ui.label("Theme Mode");
        egui::ComboBox::from_id_source("theme_mode")
            .selected_text(&self.theme_mode)
            .show_ui(ui, |ui| {
                for option in ["System", "Light", "Dark"] {
                    ui.selectable_value(&mut self.theme_mode, option.to_string(), option);
                }
            });


        ui.label("Font Size Offset");
        ui.add(egui::Slider::new(&mut self.font_size_offset, -3..=3).text("offset"));

        if ui.button("Save").clicked() {
            if let Ok(mut s) = settings::load_settings("forgedy_settings.json") {
                s.theme.custom.color_theme_mode = self.theme_mode.clone();
                s.theme.custom.font_size_offset = self.font_size_offset;

                // Avoid requiring serde::Serialize on Settings types.
                if let Ok(json) = std::fs::read_to_string("forgedy_settings.json") {
                    // no-op: keep original json text shape; we’ll rewrite by parsing again.
                    let _ = json;
                }

                // Serialize manually by writing a minimal JSON patch for the fields we edit.
                // (Still relies only on Deserialize side.)
                let patch = serde_json::json!({
                    "Theme": {
                        "Custom": {
                            "ColorThemeMode": self.theme_mode,
                            "FontSizeOffset": self.font_size_offset
                        }
                    }
                });

                if let Ok(current) = serde_json::from_str::<serde_json::Value>(
                    &std::fs::read_to_string("forgedy_settings.json").unwrap_or_default(),
                ) {
                    let merged = merge_json(current, patch);
                    if let Ok(out) = serde_json::to_string_pretty(&merged) {
                        let _ = std::fs::write("forgedy_settings.json", out);
                    }
                }


            }

        }

        ui.separator();
        ui.label("Note: egui port does not yet implement CTk theme switching/loading from themes/*.json.");
    }
}

