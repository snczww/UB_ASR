## Automatic Speech Recognition (ASR) Pipeline

This repository contains a pipeline for processing audio files and analyzing transcriptions using models from the Hugging Face Transformers library.

Table of Contents:
- Installation
- Usage
- File Structure
- Arguments
- Example Commands
- License

## Installation:
1. Clone the repository:
    git clone https://github.com/your_username/asr_pipeline.git
    cd asr_pipeline

2. Install the required dependencies:
    pip install -r requirements.txt

## Usage:
To run the ASR pipeline, use the following command:
    python ASR_main.py --audio_path path/to/your/audio/file.wav \
                       --dictionary_path dictionary.txt \
                       --ground_truth_path ground_truth.txt \
                       --model_configs_path model.json \
                       --normalizer_path normalizer.json \
                       --unit minute \
                       --output_path output/transcription_results.csv

## File Structure:
    your_project_directory/
    ├── ASR_main.py
    ├── ASR_audio_duration.py
    ├── ASR_model_process.py
    ├── ASR_metrics.py
    ├── ASR_normalizer.py
    ├── ASR_utils.py
    ├── model.json
    ├── normalizer.json
    ├── dictionary.txt (optional)
    └── ground_truth.txt (optional)

## Arguments:
- --audio_path: Path to the audio file to be processed.
- --dictionary_path: Path to the dictionary text file.
- --ground_truth_path: Path to the ground truth text file.
- --model_configs_path: Path to the model configurations JSON file (default: model.json).
- --normalizer_path: Path to the normalizer JSON file (default: normalizer.json).
- --unit: Time unit for calculating metrics (second or minute, default: minute).
- --output_path: Path to save the output CSV file.

## Example Commands:

Using All Parameters:
    python ASR_main.py --audio_path path/to/your/audio/file.wav \
                       --dictionary_path dictionary.txt \
                       --ground_truth_path ground_truth.txt \
                       --model_configs_path custom_model.json \
                       --normalizer_path custom_normalizer.json \
                       --unit second \
                       --output_path path/to/your/output/file.csv

Using Default `unit` and Default Config Files:
    python ASR_main.py --audio_path path/to/your/audio/file.wav \
                       --dictionary_path dictionary.txt \
                       --ground_truth_path ground_truth.txt \
                       --model_configs_path custom_model.json \
                       --normalizer_path custom_normalizer.json \
                       --output_path path/to/your/output/file.csv

Using All Default Values for `unit`, `model_configs_path`, and `normalizer_path`:
    python ASR_main.py --audio_path path/to/your/audio/file.wav \
                       --dictionary_path dictionary.txt \
                       --ground_truth_path ground_truth.txt

In the absence of `output_path`, the results will be saved to output/transcription_results.csv.

License:
This project is licensed under the MIT License.

