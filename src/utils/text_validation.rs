use regex::Regex;

pub fn validate_emails(lines: &[&str]) -> (usize, Vec<String>) {
    let re = Regex::new(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$").unwrap();
    let mut report = Vec::new();
    let mut valid_count = 0;
    for &v in lines {
        let ok = re.is_match(v);
        if ok { valid_count += 1; }
        report.push(format!("{}: {}", if ok {"VALID"} else {"INVALID"}, v));
    }
    (valid_count, report)
}

pub fn validate_phone_numbers(lines: &[&str]) -> (usize, Vec<String>) {
    let re = Regex::new(r"^\+?[0-9][0-9\s().-]{6,}[0-9]$").unwrap();
    let mut report = Vec::new();
    let mut valid_count = 0;
    for &v in lines {
        let ok = re.is_match(v);
        if ok { valid_count += 1; }
        report.push(format!("{}: {}", if ok {"VALID"} else {"INVALID"}, v));
    }
    (valid_count, report)
}

pub fn validate_urls(lines: &[&str]) -> (usize, Vec<String>) {
    let re = Regex::new(r"^https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/[^\s]*)?$").unwrap();
    let mut report = Vec::new();
    let mut valid_count = 0;
    for &v in lines {
        let ok = re.is_match(v);
        if ok { valid_count += 1; }
        report.push(format!("{}: {}", if ok {"VALID"} else {"INVALID"}, v));
    }
    (valid_count, report)
}

pub fn format_validation_report(header: &str, valid_count: usize, total: usize, mut body: Vec<String>) -> String {
    let mut out = Vec::new();
    out.push(format!("{}: {}/{} valid", header, valid_count, total));
    out.push(String::new());
    out.append(&mut body);
    out.join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn email_valid() {
        let (n, _) = validate_emails(&["a@b.com"]);
        assert_eq!(n, 1);
    }
}

