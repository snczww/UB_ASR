import pandas as pd
import os
from ASR_utils import read_file, read_json, parse_arguments
from ASR_model_process import process_audio
from datasets import load_dataset

def main():
    args = parse_arguments()

    # Load dictionary and ground truth if provided
    dictionary = read_file(args.dictionary_path) if args.dictionary_path else []
    ground_truth = ' '.join(read_file(args.ground_truth_path)) if args.ground_truth_path else ""

    # Load model configurations
    model_configs = read_json(args.model_configs_path)

    # Load normalizer configuration
    normalizer_config = read_json(args.normalizer_path)

    # Use sample data if audio path is not provided
    if not args.audio_path:
        dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
        audio_sample = dataset[0]["audio"]
    else:
        audio_sample = args.audio_path

    results = process_audio(model_configs, audio_sample, dictionary, ground_truth, normalizer_config, unit=args.unit)

    # Define columns based on the unit
    columns = [
        "Audio Path", "Model Path",
        f"# Sentences", f"Sentences/{args.unit}",
        f"# Words", f"Words/{args.unit}",
        f"# Verbs", f"Verbs/{args.unit}",
        f"# Nouns", f"Nouns/{args.unit}",
        f"# Dictionary Words", f"Dictionary Words/{args.unit}",
        "WER List", "CER List", "Word Errors List", "Character Errors List"
    ]
    
    # Convert results to DataFrame
    df = pd.DataFrame(results, columns=columns)
    
    # Define output path
    output_path = args.output_path if args.output_path else os.path.join('output', 'transcription_results.csv')

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the DataFrame as a CSV file
    df.to_csv(output_path, index=False)
    print(f'Results saved to {output_path}')

if __name__ == "__main__":
    main()
