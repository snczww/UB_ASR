from utils.ASR_utils import read_file, read_json
from utils.ASR_process import process_single_audio, save_results
from datasets import load_dataset

# Define your parameters here
audio_path = "audio_files/758.mp3"
dictionary_path = "dictionary.txt"
ground_truth_path = "audio_files/758.txt"
model_configs_path = "model.json"
normalizer_path = "normalizer.json"
unit = "minute"
output_path = "output/transcription_results.csv"

def main():
    dictionary = read_file(dictionary_path) if dictionary_path else []
    model_configs = read_json(model_configs_path)
    normalizer_config = read_json(normalizer_path)

    if not audio_path:
        dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
        audio_sample = dataset[0]["audio"]
    else:
        audio_sample = audio_path

    results = process_single_audio(audio_sample, dictionary, ground_truth_path, model_configs, normalizer_config, unit)
    save_results(results, output_path, unit)

if __name__ == "__main__":
    main()