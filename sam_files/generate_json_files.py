#!/usr/bin/env python

import argparse
import pandas as pd
import json
import os
import re
from collections import Counter
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import CountVectorizer
import nltk

# Download the 'wordnet' resource
nltk.download('wordnet')

# Initialize the lemmatizer
lemmatizer = nltk.WordNetLemmatizer()

def extract_ngrams(text, n):
    """
    Extract n-grams from a given text.

    Parameters:
    - text: A string of text.
    - n: The number of words in the n-gram.

    Returns:
    - A list of n-grams.
    """
    vectorizer = CountVectorizer(ngram_range=(n, n), stop_words=None)
    analyzer = vectorizer.build_analyzer()
    return analyzer(text)

def is_meaningful_phrase(phrase):
    """
    Check if a phrase is meaningful by verifying its components.

    Parameters:
    - phrase: A string representing the phrase.

    Returns:
    - True if the phrase is meaningful, False otherwise.
    """
    words = phrase.split()
    # Check if the individual words are meaningful and make sense together
    for word in words:
        if not wn.synsets(word):
            return False
    return True

def find_common_phrases(df, columns, min_count=5):
    """
    Find common phrases (bigrams and trigrams) in the specified columns of the dataframe.

    Parameters:
    - df: The input dataframe.
    - columns: List of column names to process.
    - min_count: Minimum count to consider a phrase as common.

    Returns:
    - A set of common phrases.
    """
    phrases = []
    for col in columns:
        for text in df[col].dropna():
            phrases.extend(extract_ngrams(text.lower(), 2))  # Bigrams
            phrases.extend(extract_ngrams(text.lower(), 3))  # Trigrams

    phrase_counts = Counter(phrases)
    common_phrases = {phrase for phrase, count in phrase_counts.items() if count >= min_count and is_meaningful_phrase(phrase)}
    return common_phrases

def process_keywords(row, columns, common_phrases):
    """
    Concatenate and process keywords from specified columns, splitting by newline characters.

    Parameters:
    - row: A pandas Series representing a row in the dataframe.
    - columns: List of column names to process.
    - common_phrases: Set of common phrases to preserve as composite keywords.

    Returns:
    - A string containing concatenated keywords.
    """
    exclude_keywords = {'main', 'title'}
    keywords = []
    composite_keywords = []

    for col in columns:
        if pd.notna(row[col]):
            words = row[col].replace('\n', ' ').lower().split()
            words = [word for word in words if word not in exclude_keywords and len(word) > 2]  # Exclude single chars and common keywords
            if words:
                # Identify and preserve composite keywords
                composite = {phrase for phrase in common_phrases if phrase in row[col].lower()}
                composite_keywords.extend(composite)
                for composite_kw in composite:
                    if composite_kw not in keywords:
                        keywords.append(composite_kw)

                # Add remaining single words
                for word in words:
                    if word not in keywords:
                        keywords.append(word)

    # Create a list of unique keywords and phrases
    unique_keywords = []
    for kw in composite_keywords:
        if all(kw not in other_kw for other_kw in unique_keywords):
            unique_keywords.append(kw)

    unique_keywords.extend([kw for kw in keywords if kw not in unique_keywords])

    # Select keywords by type, ensuring no overlap
    three_word_phrases = [kw for kw in unique_keywords if len(kw.split()) == 3][:4]
    two_word_phrases = [kw for kw in unique_keywords if len(kw.split()) == 2 and all(kw not in three_word for three_word in three_word_phrases)][:3]
    single_words = [kw for kw in unique_keywords if len(kw.split()) == 1 and all(kw not in two_word for two_word in two_word_phrases)][:8]

    # Combine all keywords and join into a single string
    final_keywords = three_word_phrases + two_word_phrases + single_words

    return ', '.join(final_keywords)

def sanitize_filename(name):
    """
    Sanitize the filename to remove or replace invalid characters.

    Parameters:
    - name: The original filename string.

    Returns:
    - A sanitized filename string.
    """
    # Replace invalid characters with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def create_json_files(csv_path, output_dir):
    """
    Create JSON files from a CSV dataset.

    Parameters:
    - csv_path: Path to the input CSV file.
    - output_dir: Directory where JSON files will be saved.
    """
    # Read CSV file
    df = pd.read_csv(csv_path)

    # Columns to process
    columns = ['Genre', 'Mood', 'Movement', 'Theme', 'Other keywords', 'Other keywords.1']

    # Find common phrases in the dataset
    common_phrases = find_common_phrases(df, columns)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each row and create JSON files
    for index, row in df.iterrows():
        prompt = process_keywords(row, columns, common_phrases)

        # Use the 'Title' column value as the filename, sanitize it for filesystem
        title = row.get('Title', f'file_{index+1}').strip()
        sanitized_title = sanitize_filename(title)
        file_name = f"{index+1}_{sanitized_title}.json"
        file_path = os.path.join(output_dir, file_name)

        # Prepare the data to be saved in JSON
        data = {"prompt": prompt}

        # Write JSON file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Created {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate JSON files from a CSV dataset.")
    parser.add_argument("csv_path", type=str, help="Path to the input CSV file.")
    parser.add_argument("output_dir", type=str, help="Directory where JSON files will be saved.")

    args = parser.parse_args()

    create_json_files(args.csv_path, args.output_dir)
