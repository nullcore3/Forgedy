pub fn escape_html(text: &str) -> String {
    let mut out = String::with_capacity(text.len());
    for ch in text.chars() {
        match ch {
            '&' => out.push_str("&amp;"),
            '<' => out.push_str("<"),
            '>' => out.push_str(">"),
            '"' => out.push_str("\""),
            '\'' => out.push_str("&#x27;"),
            _ => out.push(ch),
        }
    }
    out
}

pub fn escape_json_string(text: &str) -> String {
    let v = serde_json::to_string(text).unwrap();
    v[1..v.len() - 1].to_string()
}

pub fn escape_xml(text: &str) -> String {
    let escaped = escape_html(text);
    escaped.replace("&#x27;", "&apos;")
}

