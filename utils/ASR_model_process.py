import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from utils.ASR_normalizer import create_normalizer
from utils.ASR_metrics import calculate_per_time_unit, calculate_per_sentence_errors, count_sentences, count_words_verbs_nouns, count_words_from_dictionary
from utils.ASR_audio_duration import calculate_audio_duration

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

def load_model(config):
    model = AutoModelForSpeechSeq2Seq.from_pretrained(config["model_path"], torch_dtype=torch_dtype, low_cpu_mem_usage=True)
    model.to(device)
    return model

def load_processor(config):
    processor = AutoProcessor.from_pretrained(config["processor_path"])
    return processor

def create_pipeline(model, processor, config):
    pipe = pipeline(
        config["task"],
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=config["max_new_tokens"],
        chunk_length_s=config["chunk_length_s"],
        batch_size=config["batch_size"],
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe

def process_audio(model_configs, audio_path, dictionary, ground_truth, normalizer_config, unit='second'):
    results = []

    if isinstance(audio_path, str) and audio_path.startswith("http"):
        duration = 30  # Placeholder for remote audio duration, needs proper handling
    else:
        duration = calculate_audio_duration(audio_path)

    normalizer = create_normalizer(normalizer_config)

    for name, config in model_configs.items():
        print(f"Processing with {name}...")

        model = load_model(config)
        processor = load_processor(config)
        pipe = create_pipeline(model, processor, config)
        
        result = pipe(audio_path)
        transcribed_text = result["text"]
        print(f'Results for {name}:')
        print(transcribed_text)

        # Apply normalization to the transcribed text
        transcribed_text = normalizer.normalize_str(transcribed_text)

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