# Speech Recognition Analysis

This repository contains a Python script for performing speech recognition on audio files using various models, calculating various metrics related to the transcribed text, and outputting the results in a structured format using pandas.

## Features

- Load and process audio files using pre-trained speech recognition models.
- Calculate and output metrics such as:
  - Number of sentences, words, verbs, and nouns.
  - Frequency of these elements per second.
  - Number of occurrences of words from a given dictionary.
  - Per sentence WER (Word Error Rate) and CER (Character Error Rate).
  - Per sentence word and character errors.
- Output results in a structured format using pandas.

## Dependencies

To run this script, you need the following Python libraries:

- `torch`
- `jiwer`
- `transformers`
- `datasets`
- `librosa`
- `nltk`
- `pandas`

You can install these dependencies using pip:

```bash
pip install torch jiwer transformers datasets librosa nltk pandas
