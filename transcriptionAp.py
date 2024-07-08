import torch
import jiwer
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import librosa
import nltk
import pandas as pd
import argparse

# Ensure the required NLTK data files are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Configure device and data type
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Load model
def load_model(config):
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        config["model_path"], torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    return model

# Load processor
def load_processor(config):
    processor = AutoProcessor.from_pretrained(config["model_path"])
    return processor

# Create pipeline
def create_pipeline(model, processor, config):
    pipe = pipeline(
        config["task"],
        model=model,
        tokenizer=config["tokenizer"],
        feature_extractor=processor.feature_extractor,
        max_new_tokens=config["max_new_tokens"],
        chunk_length_s=config["chunk_length_s"],
        batch_size=config["batch_size"],
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe

# Load dataset
def load_sample_data():
    dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
    return dataset[0]["audio"]

# Calculate audio duration using librosa
def calculate_audio_duration(audio):
    y, sr = librosa.load(audio, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)
    return duration

# Calculate WER
def calculate_wer(candidate, ground_truth):
    wer = jiwer.wer(ground_truth, candidate)
    return wer

# Calculate CER
def calculate_cer(candidate, ground_truth):
    error = jiwer.cer(ground_truth, candidate)
    return error

# Count the number of sentences in the transcribed text
def count_sentences(text):
    sentences = text.split('.')
    return len([s for s in sentences if s.strip()])

# Count words, verbs, and nouns in the transcribed text
def count_words_verbs_nouns(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    num_words = len(words)
    num_verbs = sum(1 for word, pos in pos_tags if pos.startswith('VB'))
    num_nouns = sum(1 for word, pos in pos_tags if pos.startswith('NN'))
    return num_words, num_verbs, num_nouns

# Count occurrences of words from a given dictionary in the text
def count_words_from_dictionary(text, dictionary):
    words = nltk.word_tokenize(text.lower())
    dictionary_set = set(dictionary)
    dictionary_count = sum(1 for word in words if word in dictionary_set)
    return dictionary_count

# Calculate per sentence WER and CER, as well as word and character errors
def calculate_per_sentence_errors(candidate, ground_truth):
    candidate_sentences = [s.strip() for s in candidate.split('.') if s.strip()]
    ground_truth_sentences = [s.strip() for s in ground_truth.split('.') if s.strip()]

    wer_list = []
    cer_list = []
    word_errors_list = []
    character_errors_list = []

    for cand_sentence, gt_sentence in zip(candidate_sentences, ground_truth_sentences):
        wer = calculate_wer(cand_sentence, gt_sentence)
        cer = calculate_cer(cand_sentence, gt_sentence)
        word_errors = int(wer * len(gt_sentence.split()))
        character_errors = int(cer * len(gt_sentence))

        wer_list.append(wer)
        cer_list.append(cer)
        word_errors_list.append(word_errors)
        character_errors_list.append(character_errors)

    return wer_list, cer_list, word_errors_list, character_errors_list

# Utility function to calculate per-second and per-minute metrics
def calculate_per_time_unit(count, duration, unit='second'):
    if unit == 'minute':
        duration /= 60  # Convert seconds to minutes
    return count / duration

# Main function to process audio and get results
def process_audio(model_configs, audio_path, dictionary, ground_truth, unit='second'):
    results = []

    duration = calculate_audio_duration(audio_path)

    for name, config in model_configs.items():
        print(f"Processing with {name}...")

        model = load_model(config)
        processor = load_processor(config)
        pipe = create_pipeline(model, processor, config)
        
        result = pipe(audio_path)
        transcribed_text = result["text"]
        print(f'Results for {name}:')
        print(transcribed_text)

        num_sentences = count_sentences(transcribed_text)
        sentences_per_unit = calculate_per_time_unit(num_sentences, duration, unit=unit)
        
        num_words, num_verbs, num_nouns = count_words_verbs_nouns(transcribed_text)
        words_per_unit = calculate_per_time_unit(num_words, duration, unit=unit)
        verbs_per_unit = calculate_per_time_unit(num_verbs, duration, unit=unit)
        nouns_per_unit = calculate_per_time_unit(num_nouns, duration, unit=unit)
        
        dictionary_count = count_words_from_dictionary(transcribed_text, dictionary)
        dictionary_words_per_unit = calculate_per_time_unit(dictionary_count, duration, unit=unit)
        
        wer_list, cer_list, word_errors_list, character_errors_list = calculate_per_sentence_errors(transcribed_text, ground_truth)
        
        results.append([
            audio_path, config["model_path"],
            num_sentences, sentences_per_unit,
            num_words, words_per_unit,
            num_verbs, verbs_per_unit,
            num_nouns, nouns_per_unit,
            dictionary_count, dictionary_words_per_unit,
            wer_list, cer_list, word_errors_list, character_errors_list
        ])

    return results

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process audio files and analyze transcriptions.')
    parser.add_argument('--audio_path', type=str, required=True, help='Path to the audio file.')
    parser.add_argument('--dictionary_path', type=str, required=True, help='Path to the dictionary text file.')
    parser.add_argument('--ground_truth_path', type=str, required=True, help='Path to the ground truth text file.')
    parser.add_argument('--unit', type=str, choices=['second', 'minute'], default='second', help='Time unit for calculating metrics.')

    return parser.parse_args()

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().splitlines()
    return content

def main():
    args = parse_arguments()

    dictionary = read_file(args.dictionary_path)
    ground_truth = ' '.join(read_file(args.ground_truth_path))

    model_configs = {
        "whisper_large_v3": {
            "model_path": "openai/whisper-base",
            "tokenizer": "openai/whisper-base",  # Specify the tokenizer here
            "local": False,  # Whether the model is local
            "task": "automatic-speech-recognition",
            "chunk_length_s": 25,
            "batch_size": 16,
            "max_new_tokens": 128
        },
        "local_whisper_large_v3": {
            "model_path": "local_model",
            "tokenizer": "local_tokenizer",  # Specify the tokenizer here
            "local": True,  # Whether the model is local
            "task": "automatic-speech-recognition",
            "chunk_length_s": 25,
            "batch_size": 16,
            "max_new_tokens": 128
        },
        # Add other model configurations as needed
    }

    results = process_audio(model_configs, args.audio_path, dictionary, ground_truth, unit=args.unit)
    
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
    
    # Print the DataFrame
    print(df)

if __name__ == "__main__":
    main()
