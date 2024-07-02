import torch
import jiwer
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import librosa
import nltk
import pandas as pd

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
        tokenizer=processor.tokenizer,
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

# Main function to process audio and get results
def process_audio(model_configs, audio_path, dictionary, ground_truth):
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
        sentences_per_second = num_sentences / duration
        
        num_words, num_verbs, num_nouns = count_words_verbs_nouns(transcribed_text)
        words_per_second = num_words / duration
        verbs_per_second = num_verbs / duration
        nouns_per_second = num_nouns / duration
        
        dictionary_count = count_words_from_dictionary(transcribed_text, dictionary)
        dictionary_words_per_second = dictionary_count / duration
        
        wer_list, cer_list, word_errors_list, character_errors_list = calculate_per_sentence_errors(transcribed_text, ground_truth)
        
        results.append([
            audio_path, config["model_path"],
            num_sentences, sentences_per_second,
            num_words, words_per_second,
            num_verbs, verbs_per_second,
            num_nouns, nouns_per_second,
            dictionary_count, dictionary_words_per_second,
            wer_list, cer_list, word_errors_list, character_errors_list
        ])

    return results

# Example usage
def main():
    # audio_path = load_sample_data()
    audio_path = r"audio_files/sample_0.wav"

    dictionary = ["example", "word", "list"]  # Replace with your dictionary words
    ground_truth = "Ground truth text corresponding to the sample audio."  # Replace with actual ground truth

    model_configs = {
        "whisper_large_v3": {
            "model_path": "openai/whisper-base",
            "local": False,  # Whether the model is local
            "task": "automatic-speech-recognition",
            "chunk_length_s": 25,
            "batch_size": 16,
            "max_new_tokens": 128
        },
        "local_whisper_large_v3": {
            "model_path": "openai/whisper-base",
            "local": False,  # Whether the model is local
            "task": "automatic-speech-recognition",
            "chunk_length_s": 25,
            "batch_size": 16,
            "max_new_tokens": 128
        },
        # Add other model configurations as needed
    }

    results = process_audio(model_configs, audio_path, dictionary, ground_truth)
    
    # Convert results to DataFrame
    columns = [
        "Audio Path", "Model Path",
        "# Sentences", "Sentences/sec",
        "# Words", "Words/sec",
        "# Verbs", "Verbs/sec",
        "# Nouns", "Nouns/sec",
        "# Dictionary Words", "Dictionary Words/sec",
        "WER List", "CER List", "Word Errors List", "Character Errors List"
    ]
    df = pd.DataFrame(results, columns=columns)
    
    # Print the DataFrame
    print(df)

if __name__ == "__main__":
    main()
