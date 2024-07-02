# TODO import


'''
ASR module

'''

def load_model_from_huggingface(model_name,credentials):
    pass

def load_model_from_local(model_path):
    pass

# add more arguments if you want
# automatic speech recognition
def asr(model,audio):
    pass


'''
Transcription reliability module
'''
def wer_metric(text1, ground_truth):
    pass

def cer_metric(text1, ground_truth):
    pass

# maybe split to many functions, 1 each for stats
def text_stats(text1):
    pass

def compute_metric(text1, ground_truth, metrics=[]):
    pass

'''
Annotation reliability module
'''

# TODO

