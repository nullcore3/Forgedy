use regex::Regex;

pub fn sort_lines(text: &str, mode: &str, descending: bool) -> Vec<String> {
    let lines: Vec<&str> = text.split_terminator(['\n', '\r']).collect();

    let sortable: Vec<&str> = lines.into_iter().filter(|l| !l.trim().is_empty()).collect();

    let mut out: Vec<String>;
    match mode {
        "Numerically" => {
            let mut v: Vec<&str> = sortable;
            v.sort_by(|a, b| numeric_key(a).partial_cmp(&numeric_key(b)).unwrap());
            if descending { v.reverse(); }
            out = v.into_iter().map(|s| s.to_string()).collect();
        }
        "By Length" => {
            let mut v: Vec<&str> = sortable;
            v.sort_by(|a, b| {
                let la = a.len();
                let lb = b.len();
                (la, a.to_lowercase()).cmp(&(lb, b.to_lowercase()))
            });
            if descending { v.reverse(); }
            out = v.into_iter().map(|s| s.to_string()).collect();
        }
        _ => {
            let mut v: Vec<&str> = sortable;
            v.sort_by(|a, b| a.to_lowercase().cmp(&b.to_lowercase()));
            if descending { v.reverse(); }
            out = v.into_iter().map(|s| s.to_string()).collect();
        }
    }

    out
}

fn numeric_key(s: &str) -> f64 {
    let re = Regex::new(r"-?\d+(?:\.\d+)?").unwrap();
    if let Some(m) = re.find(s) {
        m.as_str().parse::<f64>().unwrap_or(0.0)
    } else {
        f64::INFINITY
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn alpha_sort() {
        let sorted = sort_lines("b\na", "Alphabetically", false);
        assert_eq!(sorted, vec!["a".to_string(), "b".to_string()]);
    }
}

