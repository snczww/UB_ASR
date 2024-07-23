import os
from ASR_utils import parse_arguments, read_file, read_json
from ASR_process import process_single_audio, process_mul_bypath, save_results
from datasets import load_dataset

def main():
    args = parse_arguments()

    dictionary = read_file(args.dictionary_path) if args.dictionary_path else []
    model_configs = read_json(args.model_configs_path)
    normalizer_config = read_json(args.normalizer_path)

    if args.audios_truth_path:
        results = process_mul_bypath(args.audios_truth_path, dictionary, model_configs, normalizer_config, args.unit)
    elif args.audio_path:
        results = process_single_audio(args.audio_path, dictionary, args.ground_truth_path, model_configs, normalizer_config, args.unit)
    else:
        dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
        audio_sample = dataset[0]["audio"]
        results = process_single_audio(audio_sample, dictionary, None, model_configs, normalizer_config, args.unit)

    save_results(results, args.output_path, args.unit)

if __name__ == "__main__":
    main()
