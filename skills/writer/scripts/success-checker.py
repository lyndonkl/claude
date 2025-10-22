#!/usr/bin/env python3
"""
Interactive SUCCESs model stickiness assessment.

Usage:
    python success-checker.py
    python success-checker.py input.txt
"""

import sys
from pathlib import Path

# SUCCESs elements with questions
SUCCESS_ELEMENTS = {
    'S': {
        'name': 'Simple',
        'questions': [
            'What is your core message in 12 words or less?',
            'Is this the single most important idea? (y/n)',
            'Can this guide decision-making like a commander\'s intent? (y/n)'
        ]
    },
    'U': {
        'name': 'Unexpected',
        'questions': [
            'What will surprise your reader?',
            'Where do you violate expectations or create a curiosity gap?',
            'Does your opening hook readers immediately? (y/n)'
        ]
    },
    'C1': {
        'name': 'Concrete',
        'questions': [
            'Can readers visualize this? Give a specific sensory detail:',
            'Are you using specific numbers instead of vague "many"? (y/n)',
            'Do you focus on individuals rather than masses? (y/n)'
        ]
    },
    'C2': {
        'name': 'Credible',
        'questions': [
            'What evidence supports your message?',
            'Can readers test this themselves ("try it yourself")? (y/n)',
            'Do you include vivid details that ring true? (y/n)'
        ]
    },
    'E': {
        'name': 'Emotional',
        'questions': [
            'Why should readers care emotionally?',
            'What\'s in it for them personally (WIIFY)?',
            'Does this connect to their identity or values? (y/n)'
        ]
    },
    'S2': {
        'name': 'Stories',
        'questions': [
            'What specific story demonstrates your message?',
            'Does it show a challenge, connection, or creativity plot? (y/n)',
            'Can readers mentally simulate the experience? (y/n)'
        ]
    }
}

def ask_question(question):
    """Ask a question and get user input."""
    print(f"\n{question}")
    response = input("> ").strip()
    return response

def score_response(response, question_type='text'):
    """Score a response (simple scoring)."""
    if question_type == 'yes_no':
        return 1 if response.lower() in ['y', 'yes'] else 0
    else:
        # Text response - check if meaningful
        if len(response) > 5:  # More than just a few characters
            return 1
        return 0

def assess_element(element_key, element_data):
    """Assess one SUCCESs element."""
    print(f"\n{'='*50}")
    print(f"[{element_key}] {element_data['name'].upper()}")
    print(f"{'='*50}")

    scores = []
    responses = []

    for i, question in enumerate(element_data['questions'], 1):
        response = ask_question(f"{i}. {question}")
        responses.append(response)

        # Determine question type
        if '(y/n)' in question:
            score = score_response(response, 'yes_no')
        else:
            score = score_response(response, 'text')

        scores.append(score)

    total_score = sum(scores)
    max_score = len(scores)

    print(f"\n{element_data['name']} Score: {total_score}/{max_score}", end="")
    if total_score == max_score:
        print(" ✓")
    elif total_score >= max_score * 0.7:
        print(" ⚠")
    else:
        print(" ✗")

    return total_score, max_score, responses

def generate_recommendations(element_scores):
    """Generate specific recommendations based on scores."""
    recommendations = []

    for element_key, (score, max_score) in element_scores.items():
        if score < max_score * 0.7:  # Less than 70%
            element_name = SUCCESS_ELEMENTS[element_key]['name']

            if element_key == 'S':
                recommendations.append(
                    f"→ Strengthen [S]imple: State your core message in ≤12 words at the start"
                )
            elif element_key == 'U':
                recommendations.append(
                    f"→ Strengthen [U]nexpected: Add a surprising fact or create a curiosity gap in the first paragraph"
                )
            elif element_key == 'C1':
                recommendations.append(
                    f"→ Strengthen [C]oncrete: Add specific sensory details - what can readers see, hear, feel?"
                )
            elif element_key == 'C2':
                recommendations.append(
                    f"→ Strengthen [C]redible: Include specific evidence, statistics, or 'try it yourself' elements"
                )
            elif element_key == 'E':
                recommendations.append(
                    f"→ Strengthen [E]motional: Show personal benefit - answer 'What's in it for me?'"
                )
            elif element_key == 'S2':
                recommendations.append(
                    f"→ Strengthen [S]tories: Add a specific story with real people and concrete details"
                )

    return recommendations

def format_final_report(element_scores, all_responses):
    """Generate final assessment report."""
    total_score = sum(score for score, _ in element_scores.values())
    max_total = sum(max_score for _, max_score in element_scores.values())

    report = []
    report.append("\n" + "=" * 50)
    report.append("SUCCESs Stickiness Assessment - Final Report")
    report.append("=" * 50)
    report.append("")

    # Individual scores
    report.append("Element Scores:")
    for key in ['S', 'U', 'C1', 'C2', 'E', 'S2']:
        score, max_score = element_scores[key]
        name = SUCCESS_ELEMENTS[key]['name']
        percentage = (score / max_score * 100) if max_score > 0 else 0

        status = "✓" if score == max_score else "⚠" if score >= max_score * 0.7 else "✗"
        report.append(f"  [{key}] {name:12s}: {score}/{max_score} ({percentage:.0f}%) {status}")

    report.append("")
    report.append(f"TOTAL SCORE: {total_score}/{max_total}")
    report.append("")

    # Overall assessment
    percentage = (total_score / max_total * 100) if max_total > 0 else 0

    if percentage >= 85:
        assessment = "Highly Sticky"
        message = "Excellent! Your message hits all the key elements."
    elif percentage >= 70:
        assessment = "Good Stickiness"
        message = "Good work! A few tweaks will make it even stickier."
    elif percentage >= 50:
        assessment = "Moderate Stickiness"
        message = "You're on the right track. Focus on weak elements below."
    else:
        assessment = "Needs Work"
        message = "Significant revision needed to make this message stick."

    report.append(f"OVERALL: {assessment} ({percentage:.0f}%)")
    report.append(f"{message}")
    report.append("")

    # Recommendations
    recommendations = generate_recommendations(element_scores)

    if recommendations:
        report.append("RECOMMENDATIONS:")
        for rec in recommendations:
            report.append(rec)
    else:
        report.append("✓ All elements are strong - your message is sticky!")

    report.append("")
    report.append("Remember: The six principles work together.")
    report.append("A message doesn't need perfect scores on all elements,")
    report.append("but should be strong on at least 4-5 of them.")

    return '\n'.join(report)

def main():
    """Main function."""
    print("=" * 50)
    print("SUCCESs Stickiness Checker")
    print("=" * 50)
    print("")
    print("Let's evaluate your message against the SUCCESs model.")
    print("This will take about 5-10 minutes.")
    print("")

    # Optional: read file first if provided
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if file_path.exists():
            try:
                text = file_path.read_text(encoding='utf-8')
                print("Content loaded from file:")
                print("-" * 50)
                # Show first 500 chars
                preview = text[:500] + "..." if len(text) > 500 else text
                print(preview)
                print("-" * 50)
                print("")
            except Exception as e:
                print(f"Note: Could not read file: {e}")
                print("Continuing with interactive assessment...")
                print("")
        else:
            print(f"Note: File '{file_path}' not found.")
            print("Continuing with interactive assessment...")
            print("")

    element_scores = {}
    all_responses = {}

    # Assess each element
    for element_key in ['S', 'U', 'C1', 'C2', 'E', 'S2']:
        element_data = SUCCESS_ELEMENTS[element_key]
        score, max_score, responses = assess_element(element_key, element_data)
        element_scores[element_key] = (score, max_score)
        all_responses[element_key] = responses

    # Generate and display final report
    report = format_final_report(element_scores, all_responses)
    print(report)

    # Offer to save
    print("\nWould you like to save this report? (y/n)")
    save_response = input("> ").strip().lower()

    if save_response in ['y', 'yes']:
        output_file = "success-assessment.txt"
        print(f"\nFilename (default: {output_file}):")
        filename = input("> ").strip()
        if filename:
            output_file = filename

        try:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"\n✓ Report saved to {output_file}")
        except Exception as e:
            print(f"\n✗ Error saving file: {e}")

    print("\nThank you for using the SUCCESs checker!")

if __name__ == '__main__':
    main()
