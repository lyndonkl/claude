#!/usr/bin/env python3
"""
Analyze sentence rhythm and variety.

Usage:
    python sentence-variety.py input.txt
"""

import sys
import re
from pathlib import Path
from collections import Counter
import statistics

def parse_sentences(text):
    """Parse text into sentences with word counts."""
    # Split on sentence-ending punctuation
    sentence_pattern = r'([^.!?]+[.!?]+)'
    sentences = re.findall(sentence_pattern, text)

    sentence_data = []
    for i, sent in enumerate(sentences, 1):
        sent = sent.strip()
        if sent:
            words = len(sent.split())
            sentence_data.append({
                'number': i,
                'text': sent[:60] + '...' if len(sent) > 60 else sent,
                'words': words
            })

    return sentence_data

def create_histogram(sentence_data):
    """Create histogram of sentence lengths."""
    if not sentence_data:
        return {}

    lengths = [s['words'] for s in sentence_data]

    # Define buckets
    buckets = {
        '0-5': 0,
        '6-10': 0,
        '11-15': 0,
        '16-20': 0,
        '21-25': 0,
        '26-30': 0,
        '31-40': 0,
        '41+': 0
    }

    for length in lengths:
        if length <= 5:
            buckets['0-5'] += 1
        elif length <= 10:
            buckets['6-10'] += 1
        elif length <= 15:
            buckets['11-15'] += 1
        elif length <= 20:
            buckets['16-20'] += 1
        elif length <= 25:
            buckets['21-25'] += 1
        elif length <= 30:
            buckets['26-30'] += 1
        elif length <= 40:
            buckets['31-40'] += 1
        else:
            buckets['41+'] += 1

    return buckets

def detect_monotony(sentence_data, threshold=5):
    """Detect monotonous patterns of similar-length sentences."""
    if len(sentence_data) < threshold:
        return []

    monotony_patterns = []
    lengths = [s['words'] for s in sentence_data]

    i = 0
    while i < len(lengths) - threshold + 1:
        # Check if next 'threshold' sentences are within 3 words of each other
        window = lengths[i:i+threshold]
        if max(window) - min(window) <= 3:
            # Found monotonous pattern
            pattern = {
                'start': sentence_data[i]['number'],
                'end': sentence_data[i+threshold-1]['number'],
                'count': threshold,
                'range': f"{min(window)}-{max(window)} words"
            }
            monotony_patterns.append(pattern)
            i += threshold  # Skip past this pattern
        else:
            i += 1

    return monotony_patterns

def calculate_variety_score(sentence_data):
    """Calculate variety score based on standard deviation."""
    if not sentence_data or len(sentence_data) < 3:
        return 0

    lengths = [s['words'] for s in sentence_data]

    # Calculate standard deviation
    try:
        std_dev = statistics.stdev(lengths)
        mean = statistics.mean(lengths)
    except statistics.StatisticsError:
        return 0

    # Good variety: std_dev between 6-12 for general writing
    # Score on a 1-10 scale
    if std_dev < 3:
        score = 3  # Very low variety
    elif std_dev < 5:
        score = 5  # Low variety
    elif std_dev < 7:
        score = 7  # Moderate variety
    elif std_dev < 10:
        score = 9  # Good variety
    elif std_dev < 15:
        score = 10  # Excellent variety
    else:
        score = 7  # Too much variety might be chaotic

    # Adjust for mean - very short or very long average reduces score
    if mean < 10 or mean > 30:
        score = max(1, score - 2)

    return min(10, max(1, score))

def format_histogram(buckets):
    """Format histogram as ASCII bar chart."""
    if not buckets:
        return ""

    max_count = max(buckets.values()) if buckets.values() else 0
    if max_count == 0:
        return "No data"

    lines = []
    bar_width = 40

    for bucket, count in buckets.items():
        if count > 0:
            bar_length = int((count / max_count) * bar_width)
            bar = '█' * bar_length
            lines.append(f"{bucket:>8} words: {bar} ({count})")
        else:
            lines.append(f"{bucket:>8} words: ({count})")

    return '\n'.join(lines)

def format_report(sentence_data):
    """Generate formatted analysis report."""
    if not sentence_data:
        return "No sentences found to analyze."

    lengths = [s['words'] for s in sentence_data]
    histogram = create_histogram(sentence_data)
    monotony = detect_monotony(sentence_data)
    variety_score = calculate_variety_score(sentence_data)

    # Calculate statistics
    avg_length = statistics.mean(lengths)
    median_length = statistics.median(lengths)
    try:
        std_dev = statistics.stdev(lengths)
    except statistics.StatisticsError:
        std_dev = 0

    # Build report
    report = []
    report.append("Sentence Variety Analysis")
    report.append("=" * 50)
    report.append("")

    report.append("Length Distribution:")
    report.append(format_histogram(histogram))
    report.append("")

    report.append("Statistics:")
    report.append(f"Total sentences: {len(sentence_data)}")
    report.append(f"Average: {avg_length:.1f} words")
    report.append(f"Median: {median_length:.1f} words")
    report.append(f"Std dev: {std_dev:.1f}")
    report.append(f"Shortest: {min(lengths)} words")
    report.append(f"Longest: {max(lengths)} words")
    report.append(f"Variety score: {variety_score}/10")
    report.append("")

    # Interpret variety score
    if variety_score >= 8:
        interpretation = "Excellent variety"
    elif variety_score >= 6:
        interpretation = "Good variety"
    elif variety_score >= 4:
        interpretation = "Moderate variety"
    else:
        interpretation = "Low variety"

    report.append(f"Overall: {interpretation}")
    report.append("")

    # Monotony warnings
    if monotony:
        report.append("RHYTHM ISSUES:")
        for pattern in monotony:
            report.append(f"⚠ Sentences {pattern['start']}-{pattern['end']}: "
                         f"{pattern['count']} consecutive sentences of {pattern['range']}")
        report.append("")
    else:
        report.append("✓ No monotonous patterns detected")
        report.append("")

    # Recommendations
    report.append("RECOMMENDATIONS:")

    if variety_score < 5:
        report.append("→ Low variety detected - vary sentence length deliberately")
        report.append("   • Add some very short sentences (3-5 words) for emphasis")
        report.append("   • Mix in longer, complex sentences for depth")

    if monotony:
        report.append("→ Break up monotonous patterns:")
        for pattern in monotony[:3]:  # Show first 3
            report.append(f"   • Vary length around sentences {pattern['start']}-{pattern['end']}")

    if avg_length > 25:
        report.append("→ Average sentence length is high")
        report.append("   • Break up some longer sentences")
        report.append("   • Add short punchy sentences for rhythm")

    if avg_length < 12:
        report.append("→ Average sentence length is low")
        report.append("   • Add some longer, more complex sentences")
        report.append("   • Combine related short sentences")

    if variety_score >= 7 and not monotony:
        report.append("✓ Good rhythm overall - keep it up!")

    return '\n'.join(report)

def main():
    """Main function."""
    # Read input from file or stdin
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"Error: File '{file_path}' not found", file=sys.stderr)
            sys.exit(1)
        try:
            text = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        text = sys.stdin.read()

    if not text.strip():
        print("Error: No text to analyze", file=sys.stderr)
        sys.exit(1)

    # Parse sentences
    sentence_data = parse_sentences(text)

    if not sentence_data:
        print("Error: No sentences found", file=sys.stderr)
        sys.exit(1)

    # Generate and print report
    report = format_report(sentence_data)
    print(report)

if __name__ == '__main__':
    main()
