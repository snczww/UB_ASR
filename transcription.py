import torch,jiwer
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset

# Configure device and data type
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Model configuration
model_configs = {
    "whisper_large_v3": {
        "model_path": "openai/whisper-large-v3",
        "local": False,  # Whether the model is local
        "task": "automatic-speech-recognition",
        "chunk_length_s": 25,
        "batch_size": 16,
        "max_new_tokens": 128
    },
    "local_whisper_large_v3": {
        "model_path": "./local_model",
        "local": True,  # Whether the model is local
        "task": "automatic-speech-recognition",
        "chunk_length_s": 25,
        "batch_size": 16,
        "max_new_tokens": 128
    },
    # Add other model configurations as needed
}

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


def wer_metric(text1, ground_truth):
    

# caculate wer
def calculate_wer(candidate,group_truth):
    wer = jiwer.wer(group_truth, candidate)

    return wer

def calculate_cer(candidate,group_truth ):
    error = jiwer.cer(group_truth, candidate)
    # if you also want the alignment
    # output = jiwer.process_characters(reference, hypothesis)
    # error = output.cer

    return error


# Main function
def main():
    samples = load_sample_data()
    
    for name, config in model_configs.items():
        print(f"Processing with {name}...")

        model = load_model(config)
        processor = load_processor(config)
        pipe = create_pipeline(model, processor, config)
        
        result = pipe(samples)
        print(f'Results for {name}:')
        print(result["text"])

if __name__ == "__main__":
    main()
