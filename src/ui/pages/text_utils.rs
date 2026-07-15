use eframe::egui;

use crate::utils::{
    text_case_conversion, text_comparison, text_compression, text_counting, text_encryption,
    text_escaping, text_formatting, text_generation, text_merging, text_metrics, text_noise_removal,
    text_parsing, text_search, text_sorting, text_styling, text_translation, text_validation,
};

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum TextUtilTab {
    CaseConversion,
    Counting,
    Formatting,
    Comparison,
    Generation,
    Validation,
    Search,
    Sorting,
    Merging,
    NoiseRemoval,
    Escaping,
    Metrics,
    Styling,
    Parsing,
    Translation,
    Compression,
    Encryption,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum CaseOp {
    Uppercase,
    Lowercase,
    TitleCase,
    CamelCase,
    SnakeCase,
    KebabCase,
    PascalCase,
    FlatCase,
    ConstantCase,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum FormatChoice {
    Indent,
    AlignLeft,
    AlignCenter,
    AlignRight,
    Wrap,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum ComparisonChoice {
    Levenshtein,
    Jaccard,
    All,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum GenerationChoice {
    RandomString,
    Password,
    LoremIpsum,
    Template,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum ValidationChoice {
    Email,
    Phone,
    Url,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum SortMode {
    Alphabetically,
    Numerically,
    ByLength,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum MergeMode {
    AppendSources,
    CombineLines,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum DuplicateMode {
    Keep,
    Remove,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum NoiseChoice {
    RemoveHtmlTags,
    RemoveComments,
    FilterStopwords,
    RemoveAllNoise,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum EscapeChoice {
    Html,
    Json,
    Xml,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum MetricsChoice {
    All,
    Levenshtein,
    Jaccard,
    Entropy,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum StylingFormat {
    Markdown,
    Html,
    Bbcode,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum StylingStyle {
    Bold,
    Italic,
    Underline,
    Heading,
    Quote,
    Code,
    List,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum ParsingChoice {
    Csv,
    Json,
    Xml,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum TranslationProvider {
    DetectOnly,
    MyMemory,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum CompressionAlgorithm {
    Gzip,
    Brotli,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum CompressionAction {
    Compress,
    Decompress,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum EncryptionChoice {
    AesEncrypt,
    AesDecrypt,
    RsaEncrypt,
    RsaDecrypt,
    Md5,
    Sha256,
    Sha512,
}

pub struct TextUtilsPage {
    tab: TextUtilTab,

    // Shared inputs
    input: String,
    input_b: String,
    output: String,

    // Case conversion
    case_op: CaseOp,

    // Formatting
    format_choice: FormatChoice,
    indent_spaces: usize,
    wrap_width: usize,
    align_choice: AlignChoice,

    // Comparison
    comparison_choice: ComparisonChoice,

    // Generation
    generation_choice: GenerationChoice,
    gen_length: usize,
    gen_count: usize,
    gen_template: String,

    // Validation
    validation_choice: ValidationChoice,

    // Search
    search_query: String,
    search_use_regex: bool,

    // Sorting
    sort_mode: SortMode,
    sort_desc: bool,

    // Merging
    merge_mode: MergeMode,
    merge_dup_mode: DuplicateMode,

    // Noise removal
    noise_choice: NoiseChoice,

    // Escaping
    escape_choice: EscapeChoice,

    // Metrics
    metrics_choice: MetricsChoice,

    // Styling
    styling_format_choice: StylingFormat,
    styling_style_choice: StylingStyle,

    // Parsing
    parsing_choice: ParsingChoice,

    // Translation
    translation_provider_choice: TranslationProvider,
    translation_source: String,
    translation_target: String,

    // Compression
    compression_algorithm_choice: CompressionAlgorithm,
    compression_action_choice: CompressionAction,

    // Encryption
    encryption_choice: EncryptionChoice,
    encryption_key: String,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum AlignChoice {
    Left,
    Center,
    Right,
}

impl Default for TextUtilsPage {
    fn default() -> Self {
        Self {
            tab: TextUtilTab::CaseConversion,
            input: String::new(),
            input_b: String::new(),
            output: String::new(),
            case_op: CaseOp::Uppercase,

            format_choice: FormatChoice::Indent,
            indent_spaces: 4,
            wrap_width: 80,
            align_choice: AlignChoice::Left,

            comparison_choice: ComparisonChoice::All,

            generation_choice: GenerationChoice::RandomString,
            gen_length: 16,
            gen_count: 5,
            gen_template: "item-{number}-{word}".to_string(),

            validation_choice: ValidationChoice::Email,

            search_query: String::new(),
            search_use_regex: false,

            sort_mode: SortMode::Alphabetically,
            sort_desc: false,

            merge_mode: MergeMode::AppendSources,
            merge_dup_mode: DuplicateMode::Keep,

            noise_choice: NoiseChoice::RemoveAllNoise,

            escape_choice: EscapeChoice::Html,

            metrics_choice: MetricsChoice::All,

            styling_format_choice: StylingFormat::Markdown,
            styling_style_choice: StylingStyle::Bold,

            parsing_choice: ParsingChoice::Json,

            translation_provider_choice: TranslationProvider::DetectOnly,
            translation_source: "auto".to_string(),
            translation_target: "en".to_string(),

            compression_algorithm_choice: CompressionAlgorithm::Gzip,
            compression_action_choice: CompressionAction::Compress,

            encryption_choice: EncryptionChoice::Md5,
            encryption_key: String::new(),
        }
    }
}

impl TextUtilsPage {
    pub fn ui(&mut self, ui: &mut egui::Ui) {
        ui.heading("Text Utilities");
        ui.separator();

        ui.horizontal_wrapped(|ui| {
            for (tab, label) in [
                (TextUtilTab::CaseConversion, "Case"),
                (TextUtilTab::Counting, "Counting"),
                (TextUtilTab::Formatting, "Formatting"),
                (TextUtilTab::Comparison, "Comparison"),
                (TextUtilTab::Generation, "Generation"),
                (TextUtilTab::Validation, "Validation"),
                (TextUtilTab::Search, "Search"),
                (TextUtilTab::Sorting, "Sorting"),
                (TextUtilTab::Merging, "Merging"),
                (TextUtilTab::NoiseRemoval, "Noise Removal"),
                (TextUtilTab::Escaping, "Escaping"),
                (TextUtilTab::Metrics, "Metrics"),
                (TextUtilTab::Styling, "Styling"),
                (TextUtilTab::Parsing, "Parsing"),
                (TextUtilTab::Translation, "Translation"),
                (TextUtilTab::Compression, "Compression"),
                (TextUtilTab::Encryption, "Encryption"),
            ] {
                let selected = self.tab == tab;
                if ui.selectable_label(selected, label).clicked() {
                    self.tab = tab;
                }
            }
        });

        ui.separator();

        match self.tab {
            TextUtilTab::CaseConversion => self.case_conversion_ui(ui),
            TextUtilTab::Counting => self.counting_ui(ui),
            TextUtilTab::Formatting => self.formatting_ui(ui),
            TextUtilTab::Comparison => self.comparison_ui(ui),
            TextUtilTab::Generation => self.generation_ui(ui),
            TextUtilTab::Validation => self.validation_ui(ui),
            TextUtilTab::Search => self.search_ui(ui),
            TextUtilTab::Sorting => self.sorting_ui(ui),
            TextUtilTab::Merging => self.merging_ui(ui),
            TextUtilTab::NoiseRemoval => self.noise_removal_ui(ui),
            TextUtilTab::Escaping => self.escaping_ui(ui),
            TextUtilTab::Metrics => self.metrics_ui(ui),
            TextUtilTab::Styling => self.styling_ui(ui),
            TextUtilTab::Parsing => self.parsing_ui(ui),
            TextUtilTab::Translation => self.translation_ui(ui),
            TextUtilTab::Compression => self.compression_ui(ui),
            TextUtilTab::Encryption => self.encryption_ui(ui),
        }
    }



    fn case_conversion_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Operation");
            let list = [
                (CaseOp::Uppercase, "Uppercase"),
                (CaseOp::Lowercase, "Lowercase"),
                (CaseOp::TitleCase, "Title Case"),
                (CaseOp::CamelCase, "camelCase"),
                (CaseOp::SnakeCase, "snake_case"),
                (CaseOp::KebabCase, "kebab-case"),
                (CaseOp::PascalCase, "PascalCase"),
                (CaseOp::FlatCase, "flatcase"),
                (CaseOp::ConstantCase, "CONSTANT_CASE"),
            ];
            egui::ComboBox::from_id_source("case_op")
                .selected_text(match self.case_op {
                    CaseOp::Uppercase => "Uppercase",
                    CaseOp::Lowercase => "Lowercase",
                    CaseOp::TitleCase => "Title Case",
                    CaseOp::CamelCase => "camelCase",
                    CaseOp::SnakeCase => "snake_case",
                    CaseOp::KebabCase => "kebab-case",
                    CaseOp::PascalCase => "PascalCase",
                    CaseOp::FlatCase => "flatcase",
                    CaseOp::ConstantCase => "CONSTANT_CASE",
                })
                .show_ui(ui, |ui| {
                    for (op, label) in list {
                        ui.selectable_value(&mut self.case_op, op, label);
                    }
                });
        });

        ui.separator();
        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Run").clicked() {
            let t = self.input.as_str();
            self.output = match self.case_op {
                CaseOp::Uppercase => text_case_conversion::to_uppercase(t),
                CaseOp::Lowercase => text_case_conversion::to_lowercase(t),
                CaseOp::TitleCase => text_case_conversion::to_title_case(t),
                CaseOp::CamelCase => text_case_conversion::to_camel_case(t),
                CaseOp::SnakeCase => text_case_conversion::to_snake_case(t),
                CaseOp::KebabCase => text_case_conversion::to_kebab_case(t),
                CaseOp::PascalCase => text_case_conversion::to_pascal_case(t),
                CaseOp::FlatCase => text_case_conversion::to_flat_case(t),
                CaseOp::ConstantCase => text_case_conversion::to_constant_case(t),
            };
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(8));
    }

    fn counting_ui(&mut self, ui: &mut egui::Ui) {
        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Count").clicked() {
            let chars = text_counting::count_characters(&self.input);
            let words = text_counting::count_words(&self.input);
            let lines = text_counting::count_lines(&self.input);
            self.output = format!("chars: {chars}\nwords: {words}\nlines: {lines}");
        }

        ui.separator();
        ui.label("Report");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(6));
    }

    fn formatting_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Format");
            egui::ComboBox::from_id_source("format_choice")
                .selected_text(match self.format_choice {
                    FormatChoice::Indent => "Indent Text",
                    FormatChoice::AlignLeft => "Align Left",
                    FormatChoice::AlignCenter => "Align Center",
                    FormatChoice::AlignRight => "Align Right",
                    FormatChoice::Wrap => "Wrap Text",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.format_choice, FormatChoice::Indent, "Indent Text");
                    ui.selectable_value(&mut self.format_choice, FormatChoice::AlignLeft, "Align Left");
                    ui.selectable_value(&mut self.format_choice, FormatChoice::AlignCenter, "Align Center");
                    ui.selectable_value(&mut self.format_choice, FormatChoice::AlignRight, "Align Right");
                    ui.selectable_value(&mut self.format_choice, FormatChoice::Wrap, "Wrap Text");
                });
        });

        ui.horizontal(|ui| {
            match self.format_choice {
                FormatChoice::Indent => {
                    ui.label("Spaces");
                    ui.add(egui::DragValue::new(&mut self.indent_spaces).speed(1.0));
                }
                FormatChoice::Wrap => {
                    ui.label("Width");
                    ui.add(egui::DragValue::new(&mut self.wrap_width).speed(1.0));
                }
                _ => {}
            }
        });

        ui.separator();
        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Run").clicked() {
            let t = self.input.as_str();
            self.output = match self.format_choice {
                FormatChoice::Indent => text_formatting::indent_text(t, self.indent_spaces),
                FormatChoice::AlignLeft => text_formatting::align_left(t),
                FormatChoice::AlignCenter => text_formatting::align_center(t),
                FormatChoice::AlignRight => text_formatting::align_right(t),
                FormatChoice::Wrap => text_formatting::wrap_text(t, self.wrap_width),
            };
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(8));
    }

    fn comparison_ui(&mut self, ui: &mut egui::Ui) {
        ui.label("Text A");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(6));
        ui.label("Text B");
        ui.add(egui::TextEdit::multiline(&mut self.input_b).desired_rows(6));

        if ui.button("Build Diff Report").clicked() {
            self.output = text_comparison::build_diff_report(&self.input, &self.input_b);
        }

        ui.separator();
        ui.label("Report");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(8));
    }

    fn generation_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Type");
            egui::ComboBox::from_id_source("gen_choice")
                .selected_text(match self.generation_choice {
                    GenerationChoice::RandomString => "Random String",
                    GenerationChoice::Password => "Password",
                    GenerationChoice::LoremIpsum => "Lorem Ipsum",
                    GenerationChoice::Template => "Template / Pattern",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.generation_choice, GenerationChoice::RandomString, "Random String");
                    ui.selectable_value(&mut self.generation_choice, GenerationChoice::Password, "Password");
                    ui.selectable_value(&mut self.generation_choice, GenerationChoice::LoremIpsum, "Lorem Ipsum");
                    ui.selectable_value(&mut self.generation_choice, GenerationChoice::Template, "Template / Pattern");
                });
        });

        if matches!(self.generation_choice, GenerationChoice::RandomString | GenerationChoice::Password) {
            ui.horizontal(|ui| {
                ui.label("Length");
                ui.add(egui::DragValue::new(&mut self.gen_length).speed(1.0));
                ui.label("Count");
                ui.add(egui::DragValue::new(&mut self.gen_count).speed(1.0));
            });
        } else {
            ui.horizontal(|ui| {
                ui.label("Count");
                ui.add(egui::DragValue::new(&mut self.gen_count).speed(1.0));
            });
        }

        if self.generation_choice == GenerationChoice::Template {
            ui.label("Template");
            ui.add(egui::TextEdit::singleline(&mut self.gen_template));
        }

        ui.separator();
        if ui.button("Generate").clicked() {
            self.output = match self.generation_choice {
                GenerationChoice::RandomString => text_generation::generate_random_strings(self.gen_length, self.gen_count),
                GenerationChoice::Password => text_generation::generate_passwords(self.gen_length, self.gen_count),
                GenerationChoice::LoremIpsum => text_generation::generate_lorem_ipsum(self.gen_count),
                GenerationChoice::Template => text_generation::generate_from_template(&self.gen_template, self.gen_count),
            };
        }

        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn validation_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Validation");
            egui::ComboBox::from_id_source("val_choice")
                .selected_text(match self.validation_choice {
                    ValidationChoice::Email => "Email Addresses",
                    ValidationChoice::Phone => "Phone Numbers",
                    ValidationChoice::Url => "URLs",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.validation_choice, ValidationChoice::Email, "Email Addresses");
                    ui.selectable_value(&mut self.validation_choice, ValidationChoice::Phone, "Phone Numbers");
                    ui.selectable_value(&mut self.validation_choice, ValidationChoice::Url, "URLs");
                });
        });

        ui.separator();
        ui.label("Input (one per line)");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Validate").clicked() {
            let values: Vec<&str> = self.input.lines().map(|l| l.trim()).filter(|l| !l.is_empty()).collect();
            let total = values.len();
            if total == 0 {
                self.output = "No values to validate.".to_string();
            } else {
                match self.validation_choice {
                    ValidationChoice::Email => {
                        let (valid_count, body) = text_validation::validate_emails(&values);
                        self.output = text_validation::format_validation_report("Email Addresses", valid_count, total, body);
                    }
                    ValidationChoice::Phone => {
                        let (valid_count, body) = text_validation::validate_phone_numbers(&values);
                        self.output = text_validation::format_validation_report("Phone Numbers", valid_count, total, body);
                    }
                    ValidationChoice::Url => {
                        let (valid_count, body) = text_validation::validate_urls(&values);
                        self.output = text_validation::format_validation_report("URLs", valid_count, total, body);
                    }
                }
            }
        }

        ui.separator();
        ui.label("Report");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn search_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Query");
            ui.add(egui::TextEdit::singleline(&mut self.search_query));
            ui.checkbox(&mut self.search_use_regex, "Regex");
        });

        ui.separator();
        ui.label("Text");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Search").clicked() {
            match text_search::find_matches(&self.input, &self.search_query, self.search_use_regex) {
                Ok(matches) => self.output = text_search::build_search_report(&self.input, &matches),
                Err(e) => self.output = format!("Search error: {e}"),
            }
        }

        ui.separator();
        ui.label("Results");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn sorting_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Mode");
            egui::ComboBox::from_id_source("sort_mode")
                .selected_text(match self.sort_mode {
                    SortMode::Alphabetically => "Alphabetically",
                    SortMode::Numerically => "Numerically",
                    SortMode::ByLength => "By Length",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.sort_mode, SortMode::Alphabetically, "Alphabetically");
                    ui.selectable_value(&mut self.sort_mode, SortMode::Numerically, "Numerically");
                    ui.selectable_value(&mut self.sort_mode, SortMode::ByLength, "By Length");
                });

            ui.checkbox(&mut self.sort_desc, "Descending");
        });

        ui.separator();
        ui.label("Input (one per line)");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Sort").clicked() {
            let mode_str = match self.sort_mode {
                SortMode::Alphabetically => "Alphabetically",
                SortMode::Numerically => "Numerically",
                SortMode::ByLength => "By Length",
            };
            let sorted = text_sorting::sort_lines(&self.input, mode_str, self.sort_desc);
            self.output = sorted.join("\n");
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn merging_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Mode");
            egui::ComboBox::from_id_source("merge_mode")
                .selected_text(match self.merge_mode {
                    MergeMode::AppendSources => "Append Sources",
                    MergeMode::CombineLines => "Combine Lines",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.merge_mode, MergeMode::AppendSources, "Append Sources");
                    ui.selectable_value(&mut self.merge_mode, MergeMode::CombineLines, "Combine Lines");
                });
            egui::ComboBox::from_id_source("dup_mode")
                .selected_text(match self.merge_dup_mode {
                    DuplicateMode::Keep => "Keep Duplicates",
                    DuplicateMode::Remove => "Remove Duplicates",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.merge_dup_mode, DuplicateMode::Keep, "Keep Duplicates");
                    ui.selectable_value(&mut self.merge_dup_mode, DuplicateMode::Remove, "Remove Duplicates");
                });
        });

        ui.separator();
        ui.label("Manual Source Text (Text A)");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(6));
        ui.label("Manual Source Text (Text B)");
        ui.add(egui::TextEdit::multiline(&mut self.input_b).desired_rows(6));

        if ui.button("Merge").clicked() {
            // No file selection in this scaffold; use A + B.
            let mode = match self.merge_mode {
                MergeMode::AppendSources => text_merging::MergeMode::AppendSources,
                MergeMode::CombineLines => text_merging::MergeMode::CombineLines,
            };
            let dup = match self.merge_dup_mode {
                DuplicateMode::Keep => text_merging::DuplicateMode::KeepDuplicates,
                DuplicateMode::Remove => text_merging::DuplicateMode::RemoveDuplicates,
            };
            self.output = text_merging::merge_sources(&self.input, &[self.input_b.clone()], mode, dup);
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn noise_removal_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Noise");
            egui::ComboBox::from_id_source("noise_choice")
                .selected_text(match self.noise_choice {
                    NoiseChoice::RemoveHtmlTags => "Remove HTML Tags",
                    NoiseChoice::RemoveComments => "Remove Comments",
                    NoiseChoice::FilterStopwords => "Filter Stopwords",
                    NoiseChoice::RemoveAllNoise => "Remove All Noise",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.noise_choice, NoiseChoice::RemoveHtmlTags, "Remove HTML Tags");
                    ui.selectable_value(&mut self.noise_choice, NoiseChoice::RemoveComments, "Remove Comments");
                    ui.selectable_value(&mut self.noise_choice, NoiseChoice::FilterStopwords, "Filter Stopwords");
                    ui.selectable_value(&mut self.noise_choice, NoiseChoice::RemoveAllNoise, "Remove All Noise");
                });
        });

        ui.separator();
        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Clean").clicked() {
            // Uses internal stopword set only for the provided module API.
            self.output = match self.noise_choice {
                NoiseChoice::RemoveHtmlTags => text_noise_removal::remove_html_tags(&self.input),
                NoiseChoice::RemoveComments => text_noise_removal::remove_comments(&self.input),
                NoiseChoice::FilterStopwords => {
                    let mut stop = std::collections::HashSet::new();
                    for s in ["a","an","and","are","as","at","be","but","by","for","from","has","have","he","her","his","i","in","is","it","its","of","on","or","our","she","that","the","their","they","this","to","was","we","were","with","you","your"] {
                        stop.insert(s);
                    }
                    text_noise_removal::filter_stopwords(&self.input, &stop)
                }
                NoiseChoice::RemoveAllNoise => {
                    let mut stop = std::collections::HashSet::new();
                    for s in ["a","an","and","are","as","at","be","but","by","for","from","has","have","he","her","his","i","in","is","it","its","of","on","or","our","she","that","the","their","they","this","to","was","we","were","with","you","your"] {
                        stop.insert(s);
                    }
                    text_noise_removal::remove_all_noise(&self.input, &stop)
                },

            };
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn escaping_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Escape");
            egui::ComboBox::from_id_source("escape_choice")
                .selected_text(match self.escape_choice {
                    EscapeChoice::Html => "Escape HTML",
                    EscapeChoice::Json => "Escape JSON",
                    EscapeChoice::Xml => "Escape XML",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.escape_choice, EscapeChoice::Html, "Escape HTML");
                    ui.selectable_value(&mut self.escape_choice, EscapeChoice::Json, "Escape JSON");
                    ui.selectable_value(&mut self.escape_choice, EscapeChoice::Xml, "Escape XML");
                });
        });

        ui.separator();
        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Escape Text").clicked() {
            self.output = match self.escape_choice {
                EscapeChoice::Html => text_escaping::escape_html(&self.input),
                EscapeChoice::Json => text_escaping::escape_json_string(&self.input),
                EscapeChoice::Xml => text_escaping::escape_xml(&self.input),
            };
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn metrics_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Metric");
            egui::ComboBox::from_id_source("metrics_choice")
                .selected_text(match self.metrics_choice {
                    MetricsChoice::All => "All Metrics",
                    MetricsChoice::Levenshtein => "Levenshtein Similarity",
                    MetricsChoice::Jaccard => "Jaccard Similarity",
                    MetricsChoice::Entropy => "Text Entropy",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.metrics_choice, MetricsChoice::All, "All Metrics");
                    ui.selectable_value(&mut self.metrics_choice, MetricsChoice::Levenshtein, "Levenshtein Similarity");
                    ui.selectable_value(&mut self.metrics_choice, MetricsChoice::Jaccard, "Jaccard Similarity");
                    ui.selectable_value(&mut self.metrics_choice, MetricsChoice::Entropy, "Text Entropy");
                });
        });

        ui.separator();
        ui.label("Text A");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(6));
        ui.label("Text B");
        ui.add(egui::TextEdit::multiline(&mut self.input_b).desired_rows(6));

        if ui.button("Calculate").clicked() {
            // Minimal parity: reuse module-level helpers.
            let mut lines: Vec<String> = Vec::new();
            let a = &self.input;
            let b = &self.input_b;
            if matches!(self.metrics_choice, MetricsChoice::All | MetricsChoice::Levenshtein) {
                let sim = text_metrics::levenshtein_similarity(a, b);
                lines.push(format!("Levenshtein similarity: {:.2}%", sim * 100.0));
            }
            if matches!(self.metrics_choice, MetricsChoice::All | MetricsChoice::Jaccard) {
                let sim = text_metrics::jaccard_similarity_words(a, b);
                lines.push(format!("Jaccard similarity: {:.2}%", sim * 100.0));
            }
            if matches!(self.metrics_choice, MetricsChoice::All | MetricsChoice::Entropy) {
                lines.push(format!("Entropy A: {:.4}", text_metrics::text_entropy_bits_per_char(a)));
                lines.push(format!("Entropy B: {:.4}", text_metrics::text_entropy_bits_per_char(b)));

            }
            self.output = lines.join("\n");
        }

        ui.separator();
        ui.label("Report");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn styling_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Format");
            egui::ComboBox::from_id_source("styling_format")
                .selected_text(match self.styling_format_choice {
                    StylingFormat::Markdown => "Markdown",
                    StylingFormat::Html => "HTML",
                    StylingFormat::Bbcode => "BBCode",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.styling_format_choice, StylingFormat::Markdown, "Markdown");
                    ui.selectable_value(&mut self.styling_format_choice, StylingFormat::Html, "HTML");
                    ui.selectable_value(&mut self.styling_format_choice, StylingFormat::Bbcode, "BBCode");
                });

            ui.label("Style");
            egui::ComboBox::from_id_source("styling_style")
                .selected_text(match self.styling_style_choice {
                    StylingStyle::Bold => "Bold",
                    StylingStyle::Italic => "Italic",
                    StylingStyle::Underline => "Underline",
                    StylingStyle::Heading => "Heading",
                    StylingStyle::Quote => "Quote",
                    StylingStyle::Code => "Code",
                    StylingStyle::List => "List",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.styling_style_choice, StylingStyle::Bold, "Bold");
                    ui.selectable_value(&mut self.styling_style_choice, StylingStyle::Italic, "Italic");
                    ui.selectable_value(&mut self.styling_style_choice, StylingStyle::Underline, "Underline");
                    ui.selectable_value(&mut self.styling_style_choice, StylingStyle::Heading, "Heading");
                    ui.selectable_value(&mut self.styling_style_choice, StylingStyle::Quote, "Quote");
                    ui.selectable_value(&mut self.styling_style_choice, StylingStyle::Code, "Code");
                    ui.selectable_value(&mut self.styling_style_choice, StylingStyle::List, "List");
                });
        });

        ui.separator();
        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Apply Styling").clicked() {
            let fmt = match self.styling_format_choice {
                StylingFormat::Markdown => "Markdown",
                StylingFormat::Html => "HTML",
                StylingFormat::Bbcode => "BBCode",
            };
            let style = match self.styling_style_choice {
                StylingStyle::Bold => "Bold",
                StylingStyle::Italic => "Italic",
                StylingStyle::Underline => "Underline",
                StylingStyle::Heading => "Heading",
                StylingStyle::Quote => "Quote",
                StylingStyle::Code => "Code",
                StylingStyle::List => "List",
            };
            self.output = match fmt {
                "Markdown" => text_styling::style_as_markdown(&self.input, style),
                "HTML" => text_styling::style_as_html(&self.input, style),
                "BBCode" => text_styling::style_as_bbcode(&self.input, style),
                _ => text_styling::style_as_markdown(&self.input, style),
            };

        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn parsing_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Parse");
            egui::ComboBox::from_id_source("parsing_choice")
                .selected_text(match self.parsing_choice {
                    ParsingChoice::Csv => "Parse CSV",
                    ParsingChoice::Json => "Parse JSON",
                    ParsingChoice::Xml => "Parse XML",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.parsing_choice, ParsingChoice::Csv, "Parse CSV");
                    ui.selectable_value(&mut self.parsing_choice, ParsingChoice::Json, "Parse JSON");
                    ui.selectable_value(&mut self.parsing_choice, ParsingChoice::Xml, "Parse XML");
                });
        });

        ui.separator();
        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Parse Text").clicked() {
            self.output = match self.parsing_choice {
                ParsingChoice::Csv => text_parsing::parse_csv_text(&self.input)
                    .unwrap_or_else(|e| format!("Parse error: {e}")),
                ParsingChoice::Json => text_parsing::parse_json_text(&self.input)
                    .unwrap_or_else(|e| format!("Parse error: {e}")),
                ParsingChoice::Xml => text_parsing::parse_xml_text(&self.input)
                    .unwrap_or_else(|e| format!("Parse error: {e}")),
            };
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn translation_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Provider");
            egui::ComboBox::from_id_source("translation_provider")
                .selected_text(match self.translation_provider_choice {
                    TranslationProvider::DetectOnly => "Detect Only",
                    TranslationProvider::MyMemory => "MyMemory API",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.translation_provider_choice, TranslationProvider::DetectOnly, "Detect Only");
                    ui.selectable_value(&mut self.translation_provider_choice, TranslationProvider::MyMemory, "MyMemory API");
                });

            ui.label("Source");
            ui.add(egui::TextEdit::singleline(&mut self.translation_source).desired_width(120.0));
            ui.label("Target");
            ui.add(egui::TextEdit::singleline(&mut self.translation_target).desired_width(80.0));
        });

        ui.separator();
        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Translate").clicked() {
            match self.translation_provider_choice {
                TranslationProvider::DetectOnly => {
                    let detected = text_translation::detect_language(&self.input);
                    self.output = format!("Detected language: {detected}");
                }
                TranslationProvider::MyMemory => {
                    match text_translation::translate_with_mymemory(&self.input, &self.translation_source, &self.translation_target) {
                        Ok(s) => self.output = s,
                        Err(e) => self.output = format!("Translation error: {e}"),
                    }
                }
            }
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn compression_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            egui::ComboBox::from_id_source("compression_algo")
                .selected_text(match self.compression_algorithm_choice {
                    CompressionAlgorithm::Gzip => "Gzip",
                    CompressionAlgorithm::Brotli => "Brotli",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.compression_algorithm_choice, CompressionAlgorithm::Gzip, "Gzip");
                    ui.selectable_value(&mut self.compression_algorithm_choice, CompressionAlgorithm::Brotli, "Brotli");
                });

            egui::ComboBox::from_id_source("compression_action")
                .selected_text(match self.compression_action_choice {
                    CompressionAction::Compress => "Compress",
                    CompressionAction::Decompress => "Decompress",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.compression_action_choice, CompressionAction::Compress, "Compress");
                    ui.selectable_value(&mut self.compression_action_choice, CompressionAction::Decompress, "Decompress");
                });
        });

        ui.separator();
        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Run Compression").clicked() {
            let algo = self.compression_algorithm_choice;
            let action = self.compression_action_choice;

            self.output = match (algo, action) {
                (CompressionAlgorithm::Gzip, CompressionAction::Compress) =>
                    text_compression::compress_gzip_base64(&self.input)
                        .unwrap_or_else(|e| format!("Compression error: {e}")),
                (CompressionAlgorithm::Gzip, CompressionAction::Decompress) =>
                    text_compression::decompress_gzip_base64(&self.input)
                        .unwrap_or_else(|e| format!("Compression error: {e}")),
                (CompressionAlgorithm::Brotli, CompressionAction::Compress) =>
                    text_compression::compress_brotli_base64(&self.input)
                        .unwrap_or_else(|e| format!("Compression error: {e}")),
                (CompressionAlgorithm::Brotli, CompressionAction::Decompress) =>
                    text_compression::decompress_brotli_base64(&self.input)
                        .unwrap_or_else(|e| format!("Compression error: {e}")),
            };
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }

    fn encryption_ui(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.label("Operation");
            egui::ComboBox::from_id_source("encryption_choice")
                .selected_text(match self.encryption_choice {
                    EncryptionChoice::AesEncrypt => "AES Encrypt",
                    EncryptionChoice::AesDecrypt => "AES Decrypt",
                    EncryptionChoice::RsaEncrypt => "RSA Encrypt",
                    EncryptionChoice::RsaDecrypt => "RSA Decrypt",
                    EncryptionChoice::Md5 => "MD5 Hash",
                    EncryptionChoice::Sha256 => "SHA-256 Hash",
                    EncryptionChoice::Sha512 => "SHA-512 Hash",
                })
                .show_ui(ui, |ui| {
                    ui.selectable_value(&mut self.encryption_choice, EncryptionChoice::AesEncrypt, "AES Encrypt");
                    ui.selectable_value(&mut self.encryption_choice, EncryptionChoice::AesDecrypt, "AES Decrypt");
                    ui.selectable_value(&mut self.encryption_choice, EncryptionChoice::RsaEncrypt, "RSA Encrypt");
                    ui.selectable_value(&mut self.encryption_choice, EncryptionChoice::RsaDecrypt, "RSA Decrypt");
                    ui.selectable_value(&mut self.encryption_choice, EncryptionChoice::Md5, "MD5 Hash");
                    ui.selectable_value(&mut self.encryption_choice, EncryptionChoice::Sha256, "SHA-256 Hash");
                    ui.selectable_value(&mut self.encryption_choice, EncryptionChoice::Sha512, "SHA-512 Hash");
                });
        });

        ui.separator();

        match self.encryption_choice {
            EncryptionChoice::AesEncrypt | EncryptionChoice::AesDecrypt => {
                ui.label("AES passphrase");
                ui.add(egui::TextEdit::singleline(&mut self.encryption_key).desired_width(240.0));
            }
            _ => {}
        }

        ui.label("Input");
        ui.add(egui::TextEdit::multiline(&mut self.input).desired_rows(8));

        if ui.button("Run Encryption").clicked() {
            self.output = match self.encryption_choice {
                EncryptionChoice::AesEncrypt => text_encryption::aes_encrypt(&self.input, &self.encryption_key)
                    .unwrap_or_else(|e| format!("Encryption error: {e}")),
                EncryptionChoice::AesDecrypt => text_encryption::aes_decrypt(&self.input, &self.encryption_key)
                    .unwrap_or_else(|e| format!("Encryption error: {e}")),
                EncryptionChoice::RsaEncrypt => text_encryption::rsa_encrypt(&self.input)
                    .unwrap_or_else(|e| format!("Encryption error: {e}")),
                EncryptionChoice::RsaDecrypt => text_encryption::rsa_decrypt(&self.input)
                    .unwrap_or_else(|e| format!("Encryption error: {e}")),
                EncryptionChoice::Md5 => text_encryption::md5_hash(&self.input),
                EncryptionChoice::Sha256 => text_encryption::sha256_hash(&self.input),
                EncryptionChoice::Sha512 => text_encryption::sha512_hash(&self.input),
            };
        }

        ui.separator();
        ui.label("Output");
        ui.add(egui::TextEdit::multiline(&mut self.output).desired_rows(10));
    }
}

