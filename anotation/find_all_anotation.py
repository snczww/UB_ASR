import re

def find_retracing_markers(text):
    retracing_with_brackets_pattern = r'(<[^>]+> \[//\])|(<[^>]+> \[/\])'
    retracing_single_word_pattern = r'(\b\w+\b \[/\])'
    retracing_with_fillers_pattern = r'(<[^>]+> \[/\] \(.*?\) &-[a-z]+ \[.*?\])'

    retracing_with_brackets_matches = re.findall(retracing_with_brackets_pattern, text)
    retracing_single_word_matches = re.findall(retracing_single_word_pattern, text)
    retracing_with_fillers_matches = re.findall(retracing_with_fillers_pattern, text)

    retracing_with_brackets_matches = [match[0] if match[0] else match[1] for match in retracing_with_brackets_matches]

    print('Retracing with brackets:')
    for match in retracing_with_brackets_matches:
        print(match)



def find_interposed_words(text):
    interposed_pattern = r'&\*[A-Z]{3}:[a-zA-Z]+'
    matches = re.findall(interposed_pattern, text)
    print('Interposed words:')
    for match in matches:
        print(match)

def find_overlap_markers(text):
    overlap_follows_pattern = r'<[a-zA-Z ]+> \[>\]'
    overlap_precedes_pattern = r'<[a-zA-Z ]+> \[<\]'
    overlap_follows_matches = re.findall(overlap_follows_pattern, text)
    overlap_precedes_matches = re.findall(overlap_precedes_pattern, text)
    print('Overlap follows markers:')
    for match in overlap_follows_matches:
        print(match)
    print('\nOverlap precedes markers:')
    for match in overlap_precedes_matches:
        print(match)

def find_fillers(text):
    fillers_pattern = r'&-[a-zA-Z_]+'
    matches = re.findall(fillers_pattern, text)
    print('Fillers:')
    for match in matches:
        print(match)

def find_quotation_markers(text):
    quotation_precedes_pattern = r'\+\”[^.]*'
    single_quoted_words_pattern = r'\b\w+@q\b'
    quotation_precedes_matches = re.findall(quotation_precedes_pattern, text)
    single_quoted_words_matches = re.findall(single_quoted_words_pattern, text)
    print('Quotation Precedes markers:')
    for match in quotation_precedes_matches:
        print(match)
    print('\nSingle quoted words:')
    for match in single_quoted_words_matches:
        print(match)

def find_frozen_phrases(text):
    frozen_phrases_pattern = r'\b\w+(?:_\w+)+\b'
    matches = re.findall(frozen_phrases_pattern, text)
    print('Frozen phrases:')
    for match in matches:
        print(match)

def find_errors_and_replacements(text):
    error_pattern = r'\[\*\]'
    replacement_pattern = r'\[: [^\]]+\]'
    error_matches = re.findall(error_pattern, text)
    replacement_matches = re.findall(replacement_pattern, text)
    print('Errors:')
    for match in error_matches:
        print(match)
    print('\nTarget Replacements:')
    for match in replacement_matches:
        print(match)

def find_omitted_words(text):
    omitted_word_pattern = r'\b0\w+\b'
    matches = re.findall(omitted_word_pattern, text)
    print('Omitted words:')
    for match in matches:
        print(match)

def find_word_fragments(text):
    word_fragment_pattern = r'&\+\w+'
    matches = re.findall(word_fragment_pattern, text)
    print('Word fragments:')
    for match in matches:
        print(match)

def find_annotations(text):
    annotation_pattern = r'\b(?:yyy|xxx)\b \[=! [^\]]+\]'
    matches = re.findall(annotation_pattern, text)
    print('Annotations:')
    for match in matches:
        annotation = re.search(r'\[=! [^\]]+\]', match).group()
        print(annotation)

def find_nonverbal_activities(text):
    nonverbal_pattern = r'&=\w+(:\w+)?'
    matches = re.findall(nonverbal_pattern, text) 
    print('Non-verbal activities:')
    for match in matches:
        print(match)

# Example transcript text
transcript_text = """
*CHI: <I wanted> [/] I wanted to invite Margie .
*CHI: it's [/] (.) &-um (.) it's [/] it's (.) a &-um (.) dog .
*CHI: apple [/] apple is good.
*CHI: <I wanted> [//] &-uh I thought I wanted to invite Margie .
*CHI: <the fish is> [//] the [/] the fish are swimming .
*CHI: <it was> [//] it is a sunny day.
*INV: how did you communicate <with her> [>] ?
*PAR: <I just kept talking> [<] .
*CHI: <it was very> [>] interesting.
*EXP: <I thought> [<] it was too.
*PAR: it was really difficult &*INV:mhm when all of that was happening.
*CHI: I think &*MOT:yeah that it's a good idea.
*EXP: This is interesting &*PAR:uh-huh but could you explain more?
*CHI: I was like &-um going to the store &-you_know to buy some &-stuff.
*INV: So, &-like, what do you think about that?
*PAR: Well, &-you_know, it's kind of &-um complicated.
*CHI: +” please give me all of your honey .
*CHI: the little bear said +”.
*CHI: and the boy said shh@q .
*CHI: I think you_know that patty_cake is a fun game.
*INV: What do you think about Nan_Bernstein_Ratner's work?
*PAR: Well, Mister_Spock was a character in Star Trek.
*CHI: We went to the merry_go_round yesterday.
*CHI: he had two mouses [: mice] [*] .
*CHI: two cookie [*].
*CHI: to [*] home.
*CHI: he going to the store.
*CHI: 0does he like it?
*PAR: 0mod he like it?
*CHI: 0is she going?
*PAR: 0has he done it?
*CHI: he had a &+fr friend.
*CHI: I really wanted to &+vi visit the zoo.
*CHI: she is &+un unbelievable.
*CHI: yyy [=! dada] .
*CHI: xxx [=! vocalizes/laughs/whines, etc] .
*PAR: I probably got xxx and things like that .
*CHI: &=moans loudly.
*CHI: &=laughs and &=coughs.
*CHI: makes a noise &=imit:plane.
*CHI: gestures with frustration &=ges:frustration.
*CHI: moves the doll &=moves:doll.
*CHI: shows pictures &=shows:pictures.
*CHI: points to the picture &=points:picture.
*CHI: opens mouth &=opens:mouth.
"""

# Run all functions on the transcript text
find_retracing_markers(transcript_text)
find_interposed_words(transcript_text)
find_overlap_markers(transcript_text)
find_fillers(transcript_text)
find_quotation_markers(transcript_text)
find_frozen_phrases(transcript_text)
find_errors_and_replacements(transcript_text)
find_omitted_words(transcript_text)
find_word_fragments(transcript_text)
find_annotations(transcript_text)
find_nonverbal_activities(transcript_text)
