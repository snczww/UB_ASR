from utils.ASR_utils import read_file,read_json
from utils.ASR_process import process_mul_bypath,save_results

# Define your parameters here
audios_truth_path = "/home/jovyan/work/audio_files/out"
dictionary_path = "dictionary.txt"
model_configs_path = "model.json"
normalizer_path = "normalizer.json"
unit = "minute"
output_path = "output/transcription_results.csv"

def main():
    dictionary = read_file(dictionary_path) if dictionary_path else []
    model_configs = read_json(model_configs_path)
    normalizer_config = read_json(normalizer_path)

    results = process_mul_bypath(audios_truth_path, dictionary, model_configs, normalizer_config, unit)
    save_results(results, output_path, unit)

if __name__ == "__main__":
    main()
