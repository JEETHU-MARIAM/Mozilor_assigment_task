import csv
import google.generativeai as genai
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def load_keywords(filename="keywords.txt"):
    """Loads keywords from a text file."""
    try:
        with open(filename, 'r') as f:
            keywords = [line.strip() for line in f]
        return keywords
    except FileNotFoundError:
        print(f"Error: Keyword file '{filename}' not found.")
        return None


def get_relevance_score(text, keyword):
    """Uses Gemini to get a relevance score for a keyword in the text."""
    prompt = f"""
    You are an expert at analyzing text for keyword relevance.
    Given the following text: "{text}"
    And the keyword: "{keyword}"
    Provide a relevance score from 0 to 100 (inclusive). Only output the number.
    """
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        score = int(result)
        if 0 <= score <= 100:
            return score
        else:
            print(f"Warning: Gemini returned an invalid score '{score}'. Returning 0.")
            return 0
    except Exception as e:
        print(f"Error during Gemini API call for keyword '{keyword}': {e}")
        return 0


def analyze_website_data(input_csv="website_data.csv", keywords_file="keywords.txt", output_csv="website_approval.csv"):
    """Analyzes website data, scores keywords, and stores the decision."""

    keywords = load_keywords(keywords_file)
    if not keywords:
        print("No keywords loaded. Aborting.")
        return

    try:
        with open(input_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)

    except FileNotFoundError:
        print(f"Error: CSV file '{input_csv}' not found.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    results = []
    for row in data:
        url = row['URL']
        text = row['Text']
        email = row['email']
        keyword_scores = {}

        for keyword in keywords:
            score = get_relevance_score(text, keyword)
            keyword_scores[keyword] = score
            print(f"URL: {url}, Keyword: {keyword}, Score: {score}")

        approved = False
        if all(score >= 50 for score in keyword_scores.values()) or any(score >= 50 for score in keyword_scores.values()):
            approved = True

        approval_status = "Approved" if approved else "Rejected"

        results.append({
            'URL': url,
            'Email': email,
            'Approval': approval_status,
            **keyword_scores
        })

    try:
        fieldnames = ['URL', 'Email', 'Approval', *keywords]
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Analysis results saved to '{output_csv}'.")

    except Exception as e:
        print(f"Error writing to CSV file: {e}")


if __name__ == "__main__":
    analyze_website_data()  # Or specify input/output filenames