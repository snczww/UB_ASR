import unittest
from unittest.mock import patch, MagicMock
import json
import tempfile
import os
import pandas as pd
from transcription import process_audio, read_file, read_json, create_normalizer

class TestAudioProcessing(unittest.TestCase):

    @patch('transcription.load_model')
    @patch('transcription.load_processor')
    @patch('transcription.pipeline')
    @patch('transcription.calculate_audio_duration', return_value=60.0)  # Mocking duration to be 60 seconds
    def test_process_audio(self, mock_duration, mock_pipeline, mock_processor, mock_model):
        # Mocking the pipeline result
        mock_pipe_instance = MagicMock()
        mock_pipe_instance.return_value = {"text": "This is a transcribed sentence."}
        mock_pipeline.return_value = mock_pipe_instance
        
        # Create a temporary directory to store temporary files
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Create temporary dictionary file
            dictionary_path = os.path.join(tmpdirname, 'dictionary.txt')
            with open(dictionary_path, 'w') as f:
                f.write('word1\nword2\n')

            # Create temporary ground truth file
            ground_truth_path = os.path.join(tmpdirname, 'ground_truth.txt')
            with open(ground_truth_path, 'w') as f:
                f.write('This is a ground truth sentence.')

            # Create temporary normalizer configuration file
            normalizer_path = os.path.join(tmpdirname, 'normalizer.json')
            normalizer_config = {
                "lowercase": True,
                "replace": {
                    "ain't": "is not",
                    "can't": "cannot",
                    "won't": "will not"
                }
            }
            with open(normalizer_path, 'w') as f:
                json.dump(normalizer_config, f)

            # Sample model configuration
            model_configs_path = os.path.join(tmpdirname, 'model_configs.json')
            model_configs = {
                "test_model": {
                    "model_path": "openai/whisper-large-v2",
                    "processor_path": "openai/whisper-large-v2",
                    "tokenizer": "openai/whisper-large-v2",
                    "local": False,
                    "task": "automatic-speech-recognition",
                    "chunk_length_s": 25,
                    "batch_size": 16,
                    "max_new_tokens": 128
                }
            }
            with open(model_configs_path, 'w') as f:
                json.dump(model_configs, f)

            audio_path = os.path.join(tmpdirname, 'audio.wav')
            # Create a temporary audio file (empty for mock purposes)
            with open(audio_path, 'wb') as f:
                f.write(b'\0' * 1000)

            dictionary = read_file(dictionary_path)
            ground_truth = ' '.join(read_file(ground_truth_path))
            normalizer_config = read_json(normalizer_path)
            model_configs = read_json(model_configs_path)

            # Process the audio
            results = process_audio(model_configs, audio_path, dictionary, ground_truth, normalizer_config, unit='second')

            # Convert results to DataFrame for assertion
            columns = [
                "Audio Path", "Model Path",
                "# Sentences", "Sentences/second",
                "# Words", "Words/second",
                "# Verbs", "Verbs/second",
                "# Nouns", "Nouns/second",
                "# Dictionary Words", "Dictionary Words/second",
                "WER List", "CER List", "Word Errors List", "Character Errors List"
            ]
            df = pd.DataFrame(results, columns=columns)

            # Check the DataFrame content
            self.assertEqual(df.loc[0, "Audio Path"], audio_path)
            self.assertEqual(df.loc[0, "Model Path"], model_configs["test_model"]["model_path"])
            self.assertEqual(df.loc[0, "# Sentences"], 1)
            self.assertEqual(df.loc[0, "Sentences/second"], 1/60.0)
            self.assertEqual(df.loc[0, "# Words"], 5)
            self.assertEqual(df.loc[0, "Words/second"], 5/60.0)
            self.assertEqual(df.loc[0, "# Verbs"], 1)
            self.assertEqual(df.loc[0, "Verbs/second"], 1/60.0)
            self.assertEqual(df.loc[0, "# Nouns"], 1)
            self.assertEqual(df.loc[0, "Nouns/second"], 1/60.0)
            self.assertEqual(df.loc[0, "# Dictionary Words"], 0)
            self.assertEqual(df.loc[0, "Dictionary Words/second"], 0)
            self.assertEqual(df.loc[0, "WER List"], [0.8])
            self.assertEqual(df.loc[0, "CER List"], [0.6])
            self.assertEqual(df.loc[0, "Word Errors List"], [4])
            self.assertEqual(df.loc[0, "Character Errors List"], [3])

if __name__ == '__main__':
    unittest.main()
