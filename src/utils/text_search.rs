use regex::Regex;

pub struct TextMatch {
    pub start: usize,
    pub end: usize,
    pub group0: String,
}

pub fn find_matches(text: &str, query: &str, use_regex: bool) -> Result<Vec<TextMatch>, regex::Error> {
    if use_regex {
        let re = Regex::new(query)?;
        let mut matches = Vec::new();
        for m in re.find_iter(text) {
            matches.push(TextMatch {
                start: m.start(),
                end: m.end(),
                group0: m.as_str().to_string(),
            });
        }
        Ok(matches)
    } else {
        let escaped = regex::escape(query);
        let re = Regex::new(&escaped)?;
        let mut matches = Vec::new();
        for m in re.find_iter(text) {
            matches.push(TextMatch {
                start: m.start(),
                end: m.end(),
                group0: m.as_str().to_string(),
            });
        }
        Ok(matches)
    }
}

pub fn build_search_report(text: &str, matches: &[TextMatch]) -> String {
    if matches.is_empty() {
        return "No matches found.".to_string();
    }

    let lines: Vec<&str> = text.split_terminator(['\n', '\r']).collect();

    let mut line_starts: Vec<usize> = Vec::with_capacity(lines.len());
    let mut position = 0usize;
    for line in &lines {
        line_starts.push(position);
        position += line.len() + 1; // approximate keepends
    }

    let mut out = Vec::new();
    out.push(format!("Found {} match(es).", matches.len()));
    out.push(String::new());

    for m in matches {
        let line_number = line_number_for_index(&line_starts, m.start);
        let line_text = lines.get(line_number - 1).copied().unwrap_or("");
        let col_start = m.start - line_starts[line_number - 1] + 1;
        let col_end = m.end - line_starts[line_number - 1];
        out.push(format!("Line {}, columns {}-{}: {}", line_number, col_start, col_end, m.group0));
        out.push(format!("    {}", line_text.trim()));
    }

    out.join("\n")
}

fn line_number_for_index(line_starts: &[usize], index: usize) -> usize {
    let mut line_number = 1usize;
    for (i, &start) in line_starts.iter().enumerate() {
        if start > index {
            break;
        }
        line_number = i + 1;
    }
    line_number
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn keyword() {
        let m = find_matches("a b a", "a", false).unwrap();
        assert_eq!(m.len(), 2);
    }
}

