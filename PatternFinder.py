import os
import pandas as pd
import numpy as np
import json
from collections import defaultdict, Counter
from tqdm import tqdm

def load_data(filepath, pattern_column="CLOSE", delimiter="|"):
    print(f"\nLoading data from file {filepath}...")
    data = pd.read_csv(filepath, delimiter=delimiter)
    pattern_values = data[pattern_column].tolist()
    close_values = data["CLOSE"].tolist()
    print(f"Loaded {len(pattern_values)} records from column {pattern_column}")
    return pattern_values, close_values

def normalize_pattern(pattern):
    min_val = min(pattern)
    max_val = max(pattern)
    return [(x - min_val) / (max_val - min_val) if max_val > min_val else 0 for x in pattern]

def calculate_similarity(pattern1, pattern2, tolerance=0.2):
    if len(pattern1) != len(pattern2):
        return False

    differences = [abs(a - b) for a, b in zip(pattern1, pattern2)]
    max_deviation = max(differences)

    return max_deviation <= tolerance

def find_patterns(data, close_data, min_length=3, max_length=8, tolerance=0.2):
    patterns = defaultdict(list)
    unique_patterns = {}

    total_iterations = len(data) * (max_length - min_length + 1)
    print("\nFinding patterns...")

    with tqdm(total=total_iterations) as pbar:
        for i in range(len(data)):
            for length in range(min_length, max_length + 1):
                if i + length < len(data):
                    pattern = data[i:i + length]
                    normalized_pattern = normalize_pattern(pattern)

                    found_similar = False
                    for existing_pattern, existing_info in unique_patterns.items():
                        if calculate_similarity(normalized_pattern, existing_pattern, tolerance):
                            unique_patterns[existing_pattern]['count'] += 1
                            found_similar = True

                            next_move = 1 if close_data[i + length] > close_data[i + length - 1] else 0
                            unique_patterns[existing_pattern]['moves'].append(next_move)
                            break

                    if not found_similar:
                        next_move = 1 if close_data[i + length] > close_data[i + length - 1] else 0
                        unique_patterns[tuple(normalized_pattern)] = {
                            'count': 1,
                            'moves': [next_move]
                        }

                pbar.update(1)

    print("\nProcessing found patterns...")
    for pattern, info in tqdm(unique_patterns.items()):
        next_moves = info['moves']
        next_move = 1 if next_moves.count(1) > next_moves.count(0) else 0
        patterns[f"Pattern_{hash(pattern) % 100000}"] = {
            "pattern": list(pattern),
            "count": info['count'],
            "next_move": next_move
        }

    return patterns

def get_most_frequent_patterns(patterns, top_n=20):
    print(f"\nSelecting top-{top_n} most frequent patterns...")
    sorted_patterns = sorted(patterns.items(), key=lambda x: x[1]['count'], reverse=True)

    result = {}
    for i, (key, pattern_info) in enumerate(tqdm(sorted_patterns[:top_n]), 1):
        result[key] = pattern_info
        print(f"{i}. Pattern: {pattern_info['pattern']} | Count: {pattern_info['count']} | Next Move: {'Up' if pattern_info['next_move'] == 1 else 'Down'}")

    return result

def save_patterns_to_json(patterns, output_file="patterns_found.json"):
    print(f"\nSaving results to file {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(patterns, f, indent=2, ensure_ascii=False)
    print("Done!")

if __name__ == "__main__":
    file_path = "prepared_delimiters_4.csv"
    exclude_columns = ["DATE", "TIME", "OPEN", "HIGH", "LOW"]

    print("Starting pattern analysis for all columns")
    print("-" * 50)

    data = pd.read_csv(file_path, delimiter="|")
    columns = [col for col in data.columns if col not in exclude_columns]

    for column in columns:
        output_file = f"patterns/{column}_patterns_found.json"

        if os.path.exists(output_file):
            print(f"\nFile {output_file} already exists. Skipping...")
            continue

        print(f"\nAnalyzing column {column}...")

        pattern_values, close_values = load_data(file_path, pattern_column=column)
        patterns = find_patterns(pattern_values, close_values, min_length=3, max_length=12, tolerance=0.2)
        frequent_patterns = get_most_frequent_patterns(patterns, top_n=5000)
        save_patterns_to_json(frequent_patterns, output_file=output_file)

    print("\nPattern analysis for all columns completed successfully!")
