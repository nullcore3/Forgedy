use regex::Regex;

pub fn remove_html_tags(text: &str) -> String {
    // Remove <script|style>...</script>
    let re_script_style = Regex::new(r"(?is)<(script|style).*?>.*?</\\1>").unwrap();
    let tmp = re_script_style.replace_all(text, "");

    // Remove all remaining tags
    let re_tags = Regex::new(r"(?s)<[^>]+>").unwrap();
    let tmp2 = re_tags.replace_all(&tmp, "");

    html_escape::decode_html_entities(tmp2.as_ref()).to_string()
}

pub fn remove_comments(text: &str) -> String {
    let re_html = Regex::new(r"(?s)<!--.*?-->").unwrap();
    let tmp = re_html.replace_all(text, "");

    let re_c = Regex::new(r"(?s)/\\*.*?\\*/").unwrap();
    let tmp2 = re_c.replace_all(&tmp, "");

    let re_hash = Regex::new(r"(?m)^\s*#.*$").unwrap();
    let tmp3 = re_hash.replace_all(&tmp2, "");

    let re_slash = Regex::new(r"(?m)//.*$").unwrap();
    re_slash.replace_all(&tmp3, "").to_string()
}

pub fn filter_stopwords(text: &str, stopwords: &std::collections::HashSet<&'static str>) -> String {
    let re_words = Regex::new(r"\b[A-Za-z]+\b").unwrap();
    let cleaned = re_words.replace_all(text, |caps: &regex::Captures| {
        let w = caps.get(0).unwrap().as_str();
        if stopwords.contains(w.to_lowercase().as_str()) {
            "".to_string()
        } else {
            w.to_string()
        }
    });

    let tmp = Regex::new(r"[ \t]{2,}").unwrap().replace_all(&cleaned, " ");
    let tmp2 = Regex::new(r"(?m)^[ \t]+|[ \t]+$").unwrap().replace_all(&tmp, "");
    tmp2.to_string()
}

pub fn remove_all_noise(text: &str, stopwords: &std::collections::HashSet<&'static str>) -> String {
    let t = remove_html_tags(text);
    let t = remove_comments(&t);
    filter_stopwords(&t, stopwords)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn strips_tags() {
        let s = "<b>Hello</b>";
        let r = remove_html_tags(s);
        assert!(r.to_lowercase().contains("hello"));
    }
}

