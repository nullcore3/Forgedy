pub fn indent_text(text: &str, spaces: usize) -> String {
    let indent = " ".repeat(spaces);
    text.lines()
        .map(|line| {
            if line.is_empty() {
                String::new()
            } else {
                format!("{}{}", indent, line)
            }
        })
        .collect::<Vec<_>>()
        .join("\n")
}

pub fn align_left(text: &str) -> String {
    text.lines().map(|l| l.trim()).collect::<Vec<_>>().join("\n")
}

pub fn wrap_text(text: &str, width: usize) -> String {
    // Simple word-wrap per line block.
    text.lines()
        .map(|block| {
            if block.is_empty() {
                String::new()
            } else {
                word_wrap(block, width)
            }
        })
        .collect::<Vec<_>>()
        .join("\n")
}

fn word_wrap(s: &str, width: usize) -> String {
    if width == 0 {
        return s.to_string();
    }
    let mut out_lines: Vec<String> = Vec::new();
    let mut current = String::new();

    for word in s.split_whitespace() {
        if current.is_empty() {
            current.push_str(word);
        } else if current.len() + 1 + word.len() <= width {
            current.push(' ');
            current.push_str(word);
        } else {
            out_lines.push(current);
            current = word.to_string();
        }
    }
    if !current.is_empty() {
        out_lines.push(current);
    }
    out_lines.join("\n")
}

pub fn align_center(text: &str) -> String {
    text.lines().map(|l| center_line(l.trim())).collect::<Vec<_>>().join("\n")
}

pub fn align_right(text: &str) -> String {
    text.lines().map(|l| right_line(l.trim())).collect::<Vec<_>>().join("\n")
}

fn center_line(s: &str) -> String {
    // Placeholder: real UI would provide container width. For algorithm parity,
    // we just trim.
    s.to_string()
}

fn right_line(s: &str) -> String {
    s.to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn formatting() {
        assert_eq!(indent_text("a\nb", 2), "  a\n  b");
        assert_eq!(align_left("  a\n b"), "a\nb");
        assert!(wrap_text("hello world", 5).contains("\n"));
    }
}

