pub fn count_characters(t: &str) -> usize {
    t.chars().count()
}

pub fn count_words(t: &str) -> usize {
    t.split_whitespace().count()
}

pub fn count_lines(t: &str) -> usize {
    if t.is_empty() {
        0
    } else {
        t.lines().count()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn counts() {
        let t = "a b\nc";
        assert_eq!(count_characters(t), 5);
        assert_eq!(count_words(t), 3);
        assert_eq!(count_lines(t), 2);
    }
}

