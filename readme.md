# Automatic Speech Recognition (ASR) System

This project provides a comprehensive Automatic Speech Recognition (ASR) system using the Whisper model from the `transformers` library. The system can process single or multiple audio files, analyze transcriptions, and calculate various metrics.

## Features

- Process individual audio files or directories containing multiple audio files and their corresponding ground truth.
- Analyze transcriptions using custom dictionaries and normalizers.
- Calculate metrics like Word Error Rate (WER), Character Error Rate (CER), word counts, verb counts, noun counts, and dictionary word counts.
- Save results to a CSV file.

## Requirements

- Python 3.7+
- `transformers` library
- `datasets` library
- `pandas` library
- `torch` library
- `nltk` library
- `librosa` library

## Installation

1. Clone the repository:
```
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
```

2. Install the required Python packages:
```
    pip install torch transformers datasets pandas nltk librosa
```

3. Download required NLTK data:
```
    python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

## Usage

### 1. Process Single Audio File

To process a single audio file and generate the transcription results, use the following command:

```
python ASR_main.py --audio_path path/to/your/audio/file.wav \\
                   --dictionary_path path/to/dictionary.txt \\
                   --ground_truth_path path/to/ground_truth.txt \\
                   --model_configs_path path/to/model.json \\
                   --normalizer_path path/to/normalizer.json \\
                   --unit minute \\
                   --output_path path/to/output/transcription_results.csv
```

### 2. Process Multiple Audio Files in a Directory

To process all `.mp3` audio files in a directory along with their corresponding ground truth `.txt` files, use the following command:

```
python ASR_main_path_input.py --audios_truth_path path/to/your/directory \\
                              --dictionary_path path/to/dictionary.txt \\
                              --model_configs_path path/to/model.json \\
                              --normalizer_path path/to/normalizer.json \\
                              --unit minute \\
                              --output_path path/to/output/transcription_results.csv
```

### 3. Process Single Audio File without Arguments

You can also process a single audio file by setting the parameters directly in the script:

```
python ASR_main_no_args.py
```
### 4. Process Multiple Audio Files in a Directory without Arguments

You can also process multiple audio files by setting the parameters directly in the script:

```
python ASR_main_path_input_no_args.py
```

## File Structure

- `ASR_utils.py`: Contains utility functions for reading files, parsing arguments, and finding files in directories.
- `ASR_model_process.py`: Contains functions for loading models, creating pipelines, and processing audio files.
- `ASR_process.py`: Contains functions for processing single and multiple audio files, and saving results.
- `ASR_main.py`: Main script to process single audio file using command-line arguments.
- `ASR_main_no_args.py`: Main script to process single audio file without command-line arguments.
- `ASR_main_path_input.py`: Main script to process multiple audio files in a directory.
- `dictionary.txt`: Example dictionary file with common words.
- `model.json`: Configuration file for models.
- `normalizer.json`: Configuration file for text normalization.

## Examples

### `dictionary.txt`
```plaintext
hello
world
example
test
audio
speech
recognition
transcription
automatic
learning
deep
neural
network
machine
data
science
research
education
development
artificial
intelligence
processing
language
model
algorithm
```

### `model.json`
```json
{
    "whisper_large_v3": {
        "model_path": "openai/whisper-large-v3",
        "processor_path": "openai/whisper-large-v3",
        "tokenizer": "openai/whisper-large-v3",
        "local": false,
        "task": "automatic-speech-recognition",
        "chunk_length_s": 30,
        "batch_size": 16,
        "max_new_tokens": 128
    },
    "local_whisper_large_v3": {
        "model_path": "local_model",
        "processor_path": "local_model_processor",
        "tokenizer": "local_model_tokenizer",
        "local": true,
        "task": "automatic-speech-recognition",
        "chunk_length_s": 25,
        "batch_size": 16,
        "max_new_tokens": 128
    }
}
```

### `normalizer.json`
```json
{
    "lowercase": true,
    "nfc": true,
    "strip_accents": true,
    "replace": {
        "colour": "color",
        "favourite": "favorite"
    }
}
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
