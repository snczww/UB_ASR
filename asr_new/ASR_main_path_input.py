import os
from ASR_utils import parse_arguments, read_file, read_json
from ASR_process import process_mul_bypath, save_results

def main():
    args = parse_arguments()

    audios_truth_path = args.audios_truth_path
    dictionary_path = args.dictionary_path if args.dictionary_path else "dictionary.txt"
    model_configs_path = args.model_configs_path if args.model_configs_path else "model.json"
    normalizer_path = args.normalizer_path if args.normalizer_path else "normalizer.json"
    unit = args.unit if args.unit else "minute"
    output_path = args.output_path if args.output_path else "output/transcription_results.csv"

    dictionary = read_file(dictionary_path)
    model_configs = read_json(model_configs_path)
    normalizer_config = read_json(normalizer_path)

    results = process_mul_bypath(audios_truth_path, dictionary, model_configs, normalizer_config, unit)
    save_results(results, output_path, unit)

if __name__ == "__main__":
    main()
