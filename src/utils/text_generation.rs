use rand::{distributions::Alphanumeric, Rng};

pub fn generate_random_strings(length: usize, count: usize) -> String {
    let mut rng = rand::thread_rng();
    let mut lines = Vec::new();
    for _ in 0..count {
        let s: String = (0..length)
            .map(|_| rng.sample(Alphanumeric) as char)
            .collect();
        lines.push(s);
    }
    lines.join("\n")
}

pub fn generate_passwords(length: usize, count: usize) -> String {
    use rand::distributions::Uniform;
    let mut rng = rand::thread_rng();
    let alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:,.?"
        .chars()
        .collect();
    let dist = Uniform::from(0..alphabet.len());

    let mut lines = Vec::new();
    for _ in 0..count {
        let s: String = (0..length).map(|_| alphabet[rng.sample(dist)]).collect();
        lines.push(s);
    }
    lines.join("\n")
}

pub fn generate_lorem_ipsum(paragraph_count: usize) -> String {
    let words = [
        "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do",
        "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua", "ut",
        "enim", "ad", "minim", "veniam", "quis", "nostrud", "exercitation",
    ];

    let mut rng = rand::thread_rng();
    let mut paras = Vec::new();
    for _ in 0..paragraph_count {
        let mut line_words = Vec::new();
        for _ in 0..30 {
            line_words.push(words[rng.gen_range(0..words.len())]);
        }
        let mut paragraph = line_words.join(" ");
        if let Some(first) = paragraph.get(0..1) {
            paragraph.replace_range(0..1, &first.to_uppercase());
        }
        paragraph.push('.');
        paras.push(paragraph);
    }
    paras.join("\n\n")
}

pub fn generate_from_template(template: &str, count: usize) -> String {
    let trimmed = template.trim();
    let tpl: &str = if trimmed.is_empty() {
        "item-{number}-{word}"
    } else {
        trimmed
    };

    let mut rng = rand::thread_rng();
    let words = ["alpha", "bravo", "charlie", "delta", "echo", "forge", "spark", "vector"];

    let mut out = Vec::new();
    for idx in 1..=count {
        let word = words[rng.gen_range(0..words.len())];

        let letter = (b'a' + (rng.gen_range(0..26) as u8)) as char;
        let ch = (b'0' + (rng.gen_range(0..10) as u8)) as char;

        let number = idx.to_string();
        let letter_s = letter.to_string();
        let char_s = ch.to_string();

        let mut s = tpl.to_string();
        s = s.replace("{word}", word);
        s = s.replace("{number}", number.as_str());
        s = s.replace("{letter}", letter_s.as_str());
        s = s.replace("{char}", char_s.as_str());

        out.push(s);
    }

    out.join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn template_count() {
        let s = generate_from_template("x-{number}", 3);
        assert_eq!(s.lines().count(), 3);
    }
}

