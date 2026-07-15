use std::collections::HashMap;

pub fn levenshtein_distance(a: &str, b: &str) -> usize {
    let mut s1: &str = a;
    let mut s2: &str = b;
    if a.len() < b.len() {
        s1 = b;
        s2 = a;
    }
    let s1_chars: Vec<char> = s1.chars().collect();
    let s2_chars: Vec<char> = s2.chars().collect();

    let mut prev: Vec<usize> = (0..=s2_chars.len()).collect();
    for (i, c1) in s1_chars.iter().enumerate() {
        let mut cur = vec![i + 1];
        for (j, c2) in s2_chars.iter().enumerate() {
            let insert = cur[j] + 1;
            let delete = prev[j + 1] + 1;
            let replace = prev[j] + if c1 != c2 { 1 } else { 0 };
            cur.push(std::cmp::min(insert, std::cmp::min(delete, replace)));
        }
        prev = cur;
    }
    *prev.last().unwrap_or(&0)
}

pub fn levenshtein_similarity(a: &str, b: &str) -> f64 {
    let dist = levenshtein_distance(a, b) as f64;
    let longest = std::cmp::max(a.chars().count(), b.chars().count()) as f64;
    if longest == 0.0 {
        1.0
    } else {
        1.0 - dist / longest
    }
}

pub fn jaccard_similarity_words(a: &str, b: &str) -> f64 {
    let set_a: std::collections::HashSet<String> = regex::Regex::new(r"\b\w+\b").unwrap()
        .find_iter(&a.to_lowercase())
        .map(|m| m.as_str().to_string())
        .collect();
    let set_b: std::collections::HashSet<String> = regex::Regex::new(r"\b\w+\b").unwrap()
        .find_iter(&b.to_lowercase())
        .map(|m| m.as_str().to_string())
        .collect();

    if set_a.is_empty() && set_b.is_empty() {
        return 1.0;
    }

    let inter = set_a.intersection(&set_b).count() as f64;
    let union = set_a.union(&set_b).count() as f64;
    inter / union
}

pub fn text_entropy_bits_per_char(text: &str) -> f64 {
    if text.is_empty() {
        return 0.0;
    }

    let len = text.chars().count() as f64;
    let mut counts: HashMap<char, usize> = HashMap::new();
    for ch in text.chars() {
        *counts.entry(ch).or_default() += 1;
    }

    let mut entropy = 0.0;
    for (_ch, cnt) in counts {
        let p = (cnt as f64) / len;
        entropy -= p * p.log2();
    }
    entropy
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn entropy_zero() {
        assert_eq!(text_entropy_bits_per_char(""), 0.0);
    }

    #[test]
    fn levenshtein() {
        assert_eq!(levenshtein_distance("kitten", "sitting"), 3);
    }
}

