import json
import os

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Process audio files and analyze transcriptions.')
    parser.add_argument('--audio_path', type=str, help='Path to the audio file.')
    parser.add_argument('--audios_truth_path', type=str, help='Path to the directory containing audio files and ground truth.')
    parser.add_argument('--dictionary_path', type=str, default='dictionary.txt', help='Path to the dictionary text file.')
    parser.add_argument('--ground_truth_path', type=str, help='Path to the ground truth text file.')
    parser.add_argument('--model_configs_path', type=str, default='model.json', help='Path to the model configurations JSON file.')
    parser.add_argument('--normalizer_path', type=str, default='normalizer.json', help='Path to the normalizer JSON file.')
    parser.add_argument('--unit', type=str, choices=['second', 'minute'], default='minute', help='Time unit for calculating metrics.')
    parser.add_argument('--output_path', type=str, default='output/transcription_results.csv', help='Path to save the output CSV file.')
    return parser.parse_args()

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().splitlines()
    return content

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = json.load(file)
    return content

def find_files(directory, extension):
    """Recursively find all files with the given extension in the directory."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                files.append(os.path.join(root, filename))
    return files
