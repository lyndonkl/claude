#!/usr/bin/env python3
"""
Analyze text for basic statistics and readability.

Usage:
    python analyze-text.py input.txt
    cat input.txt | python analyze-text.py
"""

import sys
import re
from pathlib import Path

def count_words(text):
    """Count words in text."""
    return len(text.split())

def count_sentences(text):
    """Count sentences in text."""
    # Split on sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def count_paragraphs(text):
    """Count paragraphs in text."""
    paragraphs = text.split('\n\n')
    return len([p for p in paragraphs if p.strip()])

def analyze_sentences(text):
    """Analyze sentence lengths and identify outliers."""
    # Split into sentences with their text
    sentences = re.split(r'([.!?]+)', text)

    # Combine sentence with its punctuation
    combined = []
    for i in range(0, len(sentences)-1, 2):
        if sentences[i].strip():
            combined.append(sentences[i].strip())

    # Analyze each sentence
    sentence_data = []
    for sent in combined:
        word_count = len(sent.split())
        sentence_data.append({
            'text': sent[:50] + '...' if len(sent) > 50 else sent,
            'words': word_count
        })

    return sentence_data

def calculate_readability(text):
    """Calculate approximate reading level using Flesch-Kincaid formula."""
    words = count_words(text)
    sentences = count_sentences(text)

    if sentences == 0 or words == 0:
        return 0, "N/A"

    # Count syllables (approximation)
    syllables = sum(count_syllables(word) for word in text.split())

    # Flesch Reading Ease: 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
    if words > 0 and sentences > 0:
        reading_ease = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

        # Flesch-Kincaid Grade Level: 0.39(words/sentences) + 11.8(syllables/words) - 15.59
        grade_level = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59

        # Interpret reading ease
        if reading_ease >= 90:
            ease_desc = "very easy (5th grade)"
        elif reading_ease >= 80:
            ease_desc = "easy (6th grade)"
        elif reading_ease >= 70:
            ease_desc = "fairly easy (7th grade)"
        elif reading_ease >= 60:
            ease_desc = "standard (8th-9th grade)"
        elif reading_ease >= 50:
            ease_desc = "fairly difficult (10th-12th grade)"
        elif reading_ease >= 30:
            ease_desc = "difficult (college)"
        else:
            ease_desc = "very difficult (college graduate)"

        return round(grade_level, 1), f"{round(reading_ease, 1)} ({ease_desc})"

    return 0, "N/A"

def count_syllables(word):
    """Count syllables in a word (approximation)."""
    word = word.lower().strip(".,!?;:")
    if len(word) <= 3:
        return 1

    # Count vowel groups
    vowels = "aeiouy"
    syllables = 0
    previous_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllables += 1
        previous_was_vowel = is_vowel

    # Adjust for silent e
    if word.endswith('e'):
        syllables -= 1

    # Ensure at least 1 syllable
    if syllables == 0:
        syllables = 1

    return syllables

def format_report(text):
    """Generate formatted analysis report."""
    words = count_words(text)
    sentences = count_sentences(text)
    paragraphs = count_paragraphs(text)
    sentence_data = analyze_sentences(text)
    grade_level, reading_ease = calculate_readability(text)

    # Calculate averages
    avg_words_per_sentence = words / sentences if sentences > 0 else 0

    # Find longest and shortest sentences
    if sentence_data:
        longest = max(sentence_data, key=lambda x: x['words'])
        shortest = min(sentence_data, key=lambda x: x['words'])
        long_sentences = [s for s in sentence_data if s['words'] > 30]
    else:
        longest = {'text': 'N/A', 'words': 0}
        shortest = {'text': 'N/A', 'words': 0}
        long_sentences = []

    # Build report
    report = []
    report.append("Text Analysis Report")
    report.append("=" * 50)
    report.append(f"Words: {words:,}")
    report.append(f"Sentences: {sentences}")
    report.append(f"Paragraphs: {paragraphs}")
    report.append(f"Avg words per sentence: {avg_words_per_sentence:.1f}")
    report.append(f"Longest sentence: {longest['words']} words")
    report.append(f"Shortest sentence: {shortest['words']} words")
    report.append(f"Reading level: Grade {grade_level}")
    report.append(f"Reading ease: {reading_ease}")
    report.append("")

    if long_sentences:
        report.append(f"Long sentences (>30 words): {len(long_sentences)} found")
        for i, sent in enumerate(long_sentences[:5], 1):  # Show first 5
            report.append(f"  {i}. {sent['words']} words: \"{sent['text']}\"")
        if len(long_sentences) > 5:
            report.append(f"  ... and {len(long_sentences) - 5} more")
        report.append("")

    # Recommendations
    report.append("Recommendations:")
    if avg_words_per_sentence > 25:
        report.append("⚠ Average sentence length is high - consider breaking up longer sentences")
    elif avg_words_per_sentence < 10:
        report.append("⚠ Average sentence length is very low - consider varying rhythm")
    else:
        report.append("✓ Good average sentence length")

    if len(long_sentences) > 3:
        report.append(f"⚠ {len(long_sentences)} sentences exceed 30 words - consider breaking them up")
    else:
        report.append("✓ Long sentences are minimal")

    if grade_level > 12:
        report.append("⚠ Reading level is high - consider simplifying for broader audience")
    elif grade_level < 6:
        report.append("⚠ Reading level is very low - verify this matches your intent")
    else:
        report.append(f"✓ Reading level (Grade {grade_level}) is appropriate for general audience")

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

    # Generate and print report
    report = format_report(text)
    print(report)

if __name__ == '__main__':
    main()
