use serde::{Deserialize, Serialize};
use std::{fs, path::Path};


#[derive(Debug, Deserialize)]
pub struct Settings {
    #[serde(rename = "Theme")]
    pub theme: Theme,
}

#[derive(Debug, Deserialize)]
pub struct Theme {
    #[serde(rename = "Custom")]
    pub custom: CustomTheme,
    #[serde(rename = "Default")]
    pub default_theme: DefaultTheme,
}

#[derive(Debug, Deserialize)]
pub struct CustomTheme {
    #[serde(rename = "ColorTheme")]
    pub color_theme: String,
    #[serde(rename = "ColorThemeMode")]
    pub color_theme_mode: String,
    #[serde(rename = "FontSizeOffset")]
    pub font_size_offset: i32,
}

#[derive(Debug, Deserialize)]
pub struct DefaultTheme {
    #[serde(rename = "ColorThemeMode")]
    pub color_theme_mode: String,
    #[serde(rename = "ColorTheme")]
    pub color_theme: String,
    #[serde(rename = "FontSizeOffset")]
    pub font_size_offset: i32,
}

#[derive(Debug, Clone)]
pub struct ComputedSettings {
    pub theme_name: String,
    pub theme_mode: String,
    pub font_size_offset: i32,

    pub base_font_size: i32,
    pub font_family: String,

    pub label_font_size: i32,
    pub button_font_size: i32,
    pub input_font_size: i32,
    pub title_font_size: i32,
    pub format_font_size: i32,
}

impl ComputedSettings {
    pub fn computed_from(s: &Settings) -> Self {
        let base_font_size = 13;
        let font_family = "Segoe UI".to_string();

        let offset = s.theme.custom.font_size_offset;
        Self {
            theme_name: s.theme.custom.color_theme.clone(),
            theme_mode: s.theme.custom.color_theme_mode.clone(),
            font_size_offset: offset,
            base_font_size,
            font_family,
            label_font_size: 13 + offset,
            button_font_size: 16 + offset,
            input_font_size: 14 + offset,
            title_font_size: 20 + offset,
            format_font_size: base_font_size + offset,
        }
    }
}

pub fn load_settings(path: impl AsRef<Path>) -> Result<Settings, Box<dyn std::error::Error>> {
    let p = path.as_ref();
    let data = fs::read_to_string(p)?;
    let s: Settings = serde_json::from_str(&data)?;
    Ok(s)
}

pub fn computed_settings(path: impl AsRef<Path>) -> Result<ComputedSettings, Box<dyn std::error::Error>> {
    let s = load_settings(path)?;
    Ok(ComputedSettings::computed_from(&s))
}


