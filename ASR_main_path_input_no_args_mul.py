import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from utils.ASR_utils import read_file, read_json, find_files
from utils.ASR_process import process_single_audio, save_results

# Define your parameters here
audios_truth_path = "/home/jovyan/work/asr_new/audio_files/out"
dictionary_path = "dictionary.txt"
model_configs_path = "model.json"
normalizer_path = "normalizer.json"
unit = "minute"
output_path = "output/transcription_results.csv"
max_workers = 6

def process_pair(audio_file, ground_truth_file, dictionary, model_configs, normalizer_config, unit):
    try:
        print(f"Processing {audio_file} and {ground_truth_file}...")
        return process_single_audio(audio_file, dictionary, ground_truth_file, model_configs, normalizer_config, unit)
    except Exception as e:
        print(f"Error processing {audio_file} and {ground_truth_file}: {e}")
        return []

def process_mul_bypath(audios_truth_path, dictionary, model_configs, normalizer_config, unit, max_workers=None):
    audio_files = find_files(audios_truth_path, ".mp3")
    ground_truth_files = find_files(audios_truth_path, ".txt")

    file_pairs = {}
    for audio_file in audio_files:
        base_name = os.path.splitext(audio_file)[0]
        corresponding_txt = base_name + ".txt"
        if corresponding_txt in ground_truth_files:
            file_pairs[audio_file] = corresponding_txt

    all_results = []
    if max_workers is None:
        max_workers = os.cpu_count() * 2  # Default to the number of CPU cores times 2

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_pair, audio_file, ground_truth_file, dictionary, model_configs, normalizer_config, unit) for audio_file, ground_truth_file in file_pairs.items()]

        for future in as_completed(futures):
            try:
                result = future.result()
                all_results.extend(result)
            except Exception as e:
                print(f"Error in future result: {e}")

    return all_results

def main():
    dictionary = read_file(dictionary_path) if dictionary_path else []
    model_configs = read_json(model_configs_path)
    normalizer_config = read_json(normalizer_path)

    cpu_count = os.cpu_count()
    
    print(f"Using {max_workers} workers based on {cpu_count} CPU cores.")

    results = process_mul_bypath(audios_truth_path, dictionary, model_configs, normalizer_config, unit, max_workers=max_workers)
    if results:
        save_results(results, output_path, unit)
    else:
        print("No results to save.")

if __name__ == "__main__":
    main()
