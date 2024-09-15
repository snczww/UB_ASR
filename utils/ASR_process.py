import pandas as pd
import os

from utils.ASR_utils import read_file, read_json, find_files
from utils.ASR_model_process import process_audio
from datasets import load_dataset

def process_single_audio(audio_path, dictionary, ground_truth, model_configs, normalizer_config, unit):
    ground_truth_text = ' '.join(read_file(ground_truth)) if ground_truth else ""
    return process_audio(model_configs, audio_path, dictionary, ground_truth_text, normalizer_config, unit)

def process_mul_bypath(audios_truth_path, dictionary, model_configs, normalizer_config, unit):
    audio_files = find_files(audios_truth_path, ".mp3")
    ground_truth_files = find_files(audios_truth_path, ".txt")

    file_pairs = {}
    for audio_file in audio_files:
        base_name = os.path.splitext(audio_file)[0]
        corresponding_txt = base_name + ".txt"
        if corresponding_txt in ground_truth_files:
            file_pairs[audio_file] = corresponding_txt

    all_results = []
    for audio_file, ground_truth_file in file_pairs.items():
        print(f"Processing {audio_file} and {ground_truth_file}...")
        results = process_single_audio(audio_file, dictionary, ground_truth_file, model_configs, normalizer_config, unit)
        all_results.extend(results)

    return all_results

def save_results(results, output_path, unit):
    columns = [
        "Audio Path", "Model Path",
        f"# Sentences", f"Sentences/{unit}",
        f"# Words", f"Words/{unit}",
        f"# Verbs", f"Verbs/{unit}",
        f"# Nouns", f"Nouns/{unit}",
        f"# Dictionary Words", f"Dictionary Words/{unit}",
        "WER List", "CER List", "Word Errors List", "Character Errors List"
    ]
    
    df = pd.DataFrame(results, columns=columns)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f'Results saved to {output_path}')
    