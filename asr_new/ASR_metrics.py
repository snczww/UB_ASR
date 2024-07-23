import jiwer
import nltk

# Ensure the required NLTK data files are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def calculate_wer(candidate, ground_truth):
    wer = jiwer.wer(ground_truth, candidate)
    return wer

def calculate_cer(candidate, ground_truth):
    error = jiwer.cer(ground_truth, candidate)
    return error

def count_sentences(text):
    sentences = text.split('.')
    return len([s for s in sentences if s.strip()])

def count_words_verbs_nouns(text):
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    num_words = len(words)
    num_verbs = sum(1 for word, pos in pos_tags if pos.startswith('VB'))
    num_nouns = sum(1 for word, pos in pos_tags if pos.startswith('NN'))
    return num_words, num_verbs, num_nouns

def count_words_from_dictionary(text, dictionary):
    words = nltk.word_tokenize(text.lower())
    dictionary_set = set(dictionary)
    dictionary_count = sum(1 for word in words if word in dictionary_set)
    return dictionary_count

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

def calculate_per_time_unit(count, duration, unit='second'):
    if unit == 'minute':
        duration /= 60
    return count / duration
