pub enum MergeMode {
    AppendSources,
    CombineLines,
}

pub enum DuplicateMode {
    KeepDuplicates,
    RemoveDuplicates,
}

pub fn merge_sources(manual_text: &str, files_texts: &[String], mode: MergeMode, dup_mode: DuplicateMode) -> String {
    let mut sources: Vec<String> = Vec::new();
    if !manual_text.trim().is_empty() {
        sources.push(manual_text.to_string());
    }
    for t in files_texts {
        sources.push(t.clone());
    }

    let merged = match mode {
        MergeMode::CombineLines => merge_by_line(&sources),
        MergeMode::AppendSources => sources
            .into_iter()
            .filter(|s| !s.is_empty())
            .collect::<Vec<_>>()
            .join("\n\n"),
    };

    match dup_mode {
        DuplicateMode::KeepDuplicates => merged,
        DuplicateMode::RemoveDuplicates => remove_duplicate_lines(&merged),
    }
}

fn merge_by_line(sources: &[String]) -> String {
    let line_groups: Vec<Vec<&str>> = sources
        .iter()
        .map(|s| s.split_terminator(['\n', '\r']).collect())
        .collect();

    let max_lines = line_groups.iter().map(|g| g.len()).max().unwrap_or(0);
    let mut merged_lines: Vec<String> = Vec::new();

    for line_index in 0..max_lines {
        for group in &line_groups {
            if line_index < group.len() {
                merged_lines.push(group[line_index].to_string());
            }
        }
    }

    merged_lines.join("\n")
}

fn remove_duplicate_lines(text: &str) -> String {
    let mut seen = std::collections::HashSet::<String>::new();
    let mut out: Vec<String> = Vec::new();
    for line in text.split_terminator(['\n', '\r']) {

        if seen.insert(line.to_string()) {
            out.push(line.to_string());
        }
    }
    out.join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn remove_duplicates() {
        let s = "a\nb\na";
        let r = remove_duplicate_lines(s);
        assert_eq!(r, "a\nb");
    }
}

