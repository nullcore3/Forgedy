use std::cmp::min;

/// Simple diff-style report between two texts.
///
/// Port intention: replace Python difflib.SequenceMatcher report builder.
pub fn build_diff_report(original: &str, modified: &str) -> String {
    let original_lines: Vec<&str> = original.split_terminator(['\n', '\r']).collect();
    let modified_lines: Vec<&str> = modified.split_terminator(['\n', '\r']).collect();


    // Minimal custom matcher: O(n*m) LCS to get stable opcodes.
    // For now, good enough for small inputs and unit-testable.
    let lcs = lcs_table(&original_lines, &modified_lines);
    let mut i = original_lines.len();
    let mut j = modified_lines.len();

    let mut report: Vec<String> = vec!["Text Comparison Report".to_string(), "".to_string()];

    // Backtrack to compute operations.
    while i > 0 && j > 0 {
        if original_lines[i - 1] == modified_lines[j - 1] {
            i -= 1;
            j -= 1;
        } else if lcs[i - 1][j] >= lcs[i][j - 1] {
            // delete
            report.push(format!("- Removed line {}: {}", i, original_lines[i - 1]));
            i -= 1;
        } else {
            // insert
            report.push(format!("+ Added line {}: {}", j, modified_lines[j - 1]));
            j -= 1;
        }
    }

    while i > 0 {
        report.push(format!("- Removed line {}: {}", i, original_lines[i - 1]));
        i -= 1;
    }
    while j > 0 {
        report.push(format!("+ Added line {}: {}", j, modified_lines[j - 1]));
        j -= 1;
    }

    if report.len() == 2 {
        report.push("No differences found.".to_string());
    }

    report.join("\n")
}

fn lcs_table(a: &[&str], b: &[&str]) -> Vec<Vec<usize>> {
    let n = a.len();
    let m = b.len();
    let mut dp = vec![vec![0usize; m + 1]; n + 1];

    for i in 1..=n {
        for j in 1..=m {
            if a[i - 1] == b[j - 1] {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]);
                // Fix: use max for LCS.
                dp[i][j] = std::cmp::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    dp
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn no_diff() {
        let r = build_diff_report("a\nb", "a\nb");
        assert!(r.contains("No differences"));
    }

    #[test]
    fn simple_insert_delete() {
        let r = build_diff_report("a\nb", "a\nc");
        assert!(r.contains("Removed") || r.contains("Added"));
    }
}

