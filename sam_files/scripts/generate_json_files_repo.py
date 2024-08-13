'''
    # Script to be runned in github repo (specific paths)
    # Prompt for terminal, from /stable-audio-tools-sam:

    python sam_files/scripts/generate_json_files_repo.py \
        sam_files/dataframes/500_{genre}_tracks.csv \
        sam_files/json/json_{genre} \
        {type-the-genre}

    --overwrite : add this flag to automatically overwrite files without prompting
'''

import pandas as pd
import json
import os
import re
import argparse
from collections import Counter
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import CountVectorizer
import nltk

# Download the 'wordnet' resource
nltk.download('wordnet')

# Initialize the lemmatizer
lemmatizer = nltk.WordNetLemmatizer()

def extract_ngrams(text, n):
    vectorizer = CountVectorizer(ngram_range=(n, n), stop_words=None)
    analyzer = vectorizer.build_analyzer()
    return analyzer(text)

def is_meaningful_phrase(phrase):
    words = phrase.split()
    for word in words:
        if not wn.synsets(word):
            return False
    return True

def find_common_phrases(df, columns, min_count=5):
    phrases = []
    for col in columns:
        for text in df[col].dropna():
            phrases.extend(extract_ngrams(text.lower(), 2))
            phrases.extend(extract_ngrams(text.lower(), 3))

    phrase_counts = Counter(phrases)
    common_phrases = {phrase for phrase, count in phrase_counts.items() if count >= min_count and is_meaningful_phrase(phrase)}
    return common_phrases

def process_keywords(row, columns, common_phrases):
    exclude_keywords = {'main', 'title'}
    keywords = []
    composite_keywords = []

    for col in columns:
        if pd.notna(row[col]):
            words = row[col].replace('\n', ' ').lower().split()
            words = [word for word in words if word not in exclude_keywords and len(word) > 2]
            if words:
                composite = {phrase for phrase in common_phrases if phrase in row[col].lower()}
                composite_keywords.extend(composite)
                for composite_kw in composite:
                    if composite_kw not in keywords:
                        keywords.append(composite_kw)

                for word in words:
                    if word not in keywords:
                        keywords.append(word)

    unique_keywords = []
    for kw in composite_keywords:
        if all(kw not in other_kw for other_kw in unique_keywords):
            unique_keywords.append(kw)

    unique_keywords.extend([kw for kw in keywords if kw not in unique_keywords])

    three_word_phrases = [kw for kw in unique_keywords if len(kw.split()) == 3][:4]
    two_word_phrases = [kw for kw in unique_keywords if len(kw.split()) == 2 and all(kw not in three_word for three_word in three_word_phrases)][:3]
    single_words = [kw for kw in unique_keywords if len(kw.split()) == 1 and all(kw not in two_word for two_word in two_word_phrases)][:8]

    final_keywords = three_word_phrases + two_word_phrases + single_words

    return ', '.join(final_keywords)

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def create_json_files(csv_path, output_dir, overwrite=False):
    df = pd.read_csv(csv_path)
    columns = ['Genre', 'Mood', 'Movement', 'Theme', 'Other keywords', 'Other keywords.1']
    common_phrases = find_common_phrases(df, columns)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Confirmation prompt for overwriting files
    if not overwrite:
        existing_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
        if existing_files:
            prompt = input(f"Files will be overwritten in {output_dir}. Proceed? (y/n): ")
            if prompt.lower() != 'y':
                print("Operation cancelled.")
                return

    for index, row in df.iterrows():
        prompt = process_keywords(row, columns, common_phrases)
        title = row.get('Title', f'file_{index+1}').strip()
        sanitized_title = sanitize_filename(title)
        file_name = f"{index+1}_{sanitized_title}.json"
        file_path = os.path.join(output_dir, file_name)
        data = {"prompt": prompt}

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Created or overwritten {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate JSON files from CSV data.')
    parser.add_argument('csv_path', type=str, help='Path to the CSV file with placeholder {genre}.')
    parser.add_argument('output_dir', type=str, help='Directory to save JSON files with placeholder {genre}.')
    parser.add_argument('genre', type=str, help='Value to replace the placeholder {genre}.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files without confirmation.')
    args = parser.parse_args()

    # Replace placeholders with actual values
    csv_path = args.csv_path.replace('{genre}', args.genre)
    output_dir = args.output_dir.replace('{genre}', args.genre)

    create_json_files(csv_path, output_dir, args.overwrite)

if __name__ == '__main__':
    main()
