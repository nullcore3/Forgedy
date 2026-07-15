/// Text case conversion utilities (port from Python TxtUtils.text_case_conversion)

pub fn to_uppercase(t: &str) -> String {
    t.to_uppercase()
}

pub fn to_lowercase(t: &str) -> String {
    t.to_lowercase()
}

pub fn to_title_case(t: &str) -> String {
    // Rust's title_case is locale-aware enough for basic ASCII; for a closer
    // port we keep Python behavior via split words.
    let mut out = String::new();
    for (i, w) in t.split_whitespace().enumerate() {
        if i > 0 {
            out.push(' ');
        }
        let mut chars = w.chars();
        if let Some(first) = chars.next() {
            out.extend(first.to_uppercase());
            out.extend(chars.flat_map(|c| c.to_lowercase()));
        }
    }
    out
}

pub fn to_camel_case(text: &str) -> String {
    let mut iter = text.split_whitespace();
    let first = match iter.next() {
        Some(w) => w.to_lowercase(),
        None => return String::new(),
    };
    let mut out = first;
    for w in iter {
        let mut chars = w.chars();
        if let Some(first) = chars.next() {
            out.push_str(&first.to_uppercase().to_string());
            out.extend(chars.flat_map(|c| c.to_lowercase()));
        }
    }
    out
}

pub fn to_snake_case(text: &str) -> String {
    text.split_whitespace().collect::<Vec<_>>().join("_").to_lowercase()
}

pub fn to_kebab_case(text: &str) -> String {
    text.split_whitespace().collect::<Vec<_>>().join("-").to_lowercase()
}

pub fn to_pascal_case(text: &str) -> String {
    text.split_whitespace()
        .map(|w| {
            let mut chars = w.chars();
            if let Some(first) = chars.next() {
                let mut s = first.to_uppercase().to_string();
                s.push_str(&chars.as_str().to_lowercase());
                s
            } else {
                String::new()
            }
        })
        .collect::<String>()
}

pub fn to_flat_case(text: &str) -> String {
    text.split_whitespace().collect::<String>().to_lowercase()
}

pub fn to_constant_case(text: &str) -> String {
    text.split_whitespace()
        .collect::<Vec<_>>()
        .join("_")
        .to_uppercase()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn basic_cases() {
        assert_eq!(to_uppercase("aBc"), "ABC");
        assert_eq!(to_lowercase("aBc"), "abc");
        assert_eq!(to_snake_case("Hello World"), "hello_world");
        assert_eq!(to_kebab_case("Hello World"), "hello-world");
        assert_eq!(to_constant_case("Hello World"), "HELLO_WORLD");
        assert_eq!(to_camel_case("Hello world"), "helloWorld");
        assert_eq!(to_pascal_case("hello world"), "HelloWorld");
        assert_eq!(to_flat_case("hello   world"), "helloworld");
    }
}

