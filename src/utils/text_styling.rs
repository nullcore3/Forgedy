pub fn style_as_markdown(text: &str, style: &str) -> String {
    match style {
        "Bold" => format!("**{}**", text),
        "Italic" => format!("*{}*", text),
        "Underline" => format!("<u>{}</u>", escape_html(text)),
        "Heading" => text
            .lines()
            .map(|l| if l.is_empty() { l.to_string() } else { format!("# {}", l) })
            .collect::<Vec<_>>()
            .join("\n"),
        "Quote" => text
            .lines()
            .map(|l| if l.is_empty() { ">".to_string() } else { format!("> {}", l) })
            .collect::<Vec<_>>()
            .join("\n"),
        "Code" => format!("```\n{}\n```", text),
        _ => text
            .lines()
            .map(|l| if l.is_empty() { l.to_string() } else { format!("- {}", l) })
            .collect::<Vec<_>>()
            .join("\n"),
    }
}

pub fn style_as_html(text: &str, style: &str) -> String {
    let escaped = escape_html(text);
    match style {
        "Bold" => format!("<strong>{}</strong>", escaped),
        "Italic" => format!("<em>{}</em>", escaped),
        "Underline" => format!("<u>{}</u>", escaped),
        "Heading" => format!("<h1>{}</h1>", escaped),
        "Quote" => format!("<blockquote>{}</blockquote>", escaped),
        "Code" => format!("<pre><code>{}</code></pre>", escaped),
        _ => {
            let items = text
                .lines()
                .filter(|l| !l.is_empty())
                .map(|l| format!("  <li>{}</li>", escape_html(l)))
                .collect::<Vec<_>>()
                .join("\n");
            format!("<ul>\n{}\n</ul>", items)
        }
    }
}

pub fn style_as_bbcode(text: &str, style: &str) -> String {
    match style {
        "Bold" => format!("[b]{text}[/b]"),
        "Italic" => format!("[i]{text}[/i]"),
        "Underline" => format!("[u]{text}[/u]"),
        "Heading" => format!("[size=150][b]{text}[/b][/size]"),
        "Quote" => format!("[quote]{text}[/quote]"),
        "Code" => format!("[code]{text}[/code]"),
        _ => {
            let items = text
                .lines()
                .filter(|l| !l.is_empty())
                .map(|l| format!("[*]{l}"))
                .collect::<Vec<_>>()
                .join("\n");
            format!("[list]\n{}\n[/list]", items)
        }
    }
}

fn escape_html(text: &str) -> String {
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn markdown_bold() {
        assert_eq!(style_as_markdown("a", "Bold"), "**a**");
    }
}

