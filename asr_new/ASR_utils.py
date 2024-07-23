import argparse
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process audio files and analyze transcriptions.')
    parser.add_argument('--audio_path', type=str, help='Path to the audio file.')
    parser.add_argument('--dictionary_path', type=str, help='Path to the dictionary text file.')
    parser.add_argument('--ground_truth_path', type=str, help='Path to the ground truth text file.')
    parser.add_argument('--model_configs_path', type=str, help='Path to the model configurations JSON file.')
    parser.add_argument('--normalizer_path', type=str, help='Path to the normalizer JSON file.')
    parser.add_argument('--unit', type=str, choices=['second', 'minute'], default='second', help='Time unit for calculating metrics.')

    return parser.parse_args()

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().splitlines()
    return content

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = json.load(file)
    return content
