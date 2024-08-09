import re

def find_retracing_markers(text):
    retracing_with_brackets_pattern = r'(<[^>]+> \[//\])|(<[^>]+> \[/\])'
    retracing_single_word_pattern = r'(\b\w+\b \[/\])'
    retracing_with_fillers_pattern = r'(<[^>]+> \[/\] \(.*?\) &-[a-z]+ \[.*?\])'

    retracing_with_brackets_matches = re.findall(retracing_with_brackets_pattern, text)
    retracing_single_word_matches = re.findall(retracing_single_word_pattern, text)
    retracing_with_fillers_matches = re.findall(retracing_with_fillers_pattern, text)

    retracing_with_brackets_matches = [match[0] if match[0] else match[1] for match in retracing_with_brackets_matches]

    return retracing_with_brackets_matches + retracing_single_word_matches + retracing_with_fillers_matches

def find_interposed_words(text):
    interposed_pattern = r'&\*[A-Z]{3}:[a-zA-Z]+'
    matches = re.findall(interposed_pattern, text)
    return matches

def find_overlap_markers(text):
    overlap_follows_pattern = r'<[a-zA-Z ]+> \[>\]'
    overlap_precedes_pattern = r'<[a-zA-Z ]+> \[<\]'
    overlap_follows_matches = re.findall(overlap_follows_pattern, text)
    overlap_precedes_matches = re.findall(overlap_precedes_pattern, text)
    return overlap_follows_matches + overlap_precedes_matches

def find_fillers(text):
    fillers_pattern = r'&-[a-zA-Z_]+'
    matches = re.findall(fillers_pattern, text)
    return matches

# def find_quotation_markers(text):
#     quotation_precedes_pattern = r'\+\”[^.]*'
#     single_quoted_words_pattern = r'\b\w+@q\b'
    # quotation_precedes_matches = re.findall(quotation_precedes_pattern, text)
    # single_quoted_words_matches = re.findall(single_quoted_words_pattern, text)
#     return quotation_precedes_matches + single_quoted_words_matches

def find_shortened_words(text):
    # 首先按空格分割文本
    words = text.split()
    
    # 定义正则表达式来匹配缩写形式的单词
    shortened_pattern = r'\(?\w*\(?\w+\)?\w*\)?'
    
    matches = []
    for word in words:
        match = re.fullmatch(shortened_pattern, word)
        if match:
            # 只保留包含括号的匹配项
            if '(' in match.group() or ')' in match.group():
                matches.append(match.group())
    
    return matches


def find_frozen_phrases(text):
    frozen_phrases_pattern = r'\b\w+(?:_\w+)+\b'
    matches = re.findall(frozen_phrases_pattern, text)
    return matches

# def find_errors_and_replacements(text):
#     error_pattern = r'\[\*\]'
#     replacement_pattern = r'\[: [^\]]+\]'
#     error_matches = re.findall(error_pattern, text)
#     replacement_matches = re.findall(replacement_pattern, text)
#     return error_matches + replacement_matches

def find_errors_and_replacements(text):
    # error_pattern = r'\[\*\]'
    replacement_pattern = r'\[: [^\]]+\]'
    # error_matches = re.findall(error_pattern, text)
    replacement_matches = re.findall(replacement_pattern, text)
    return  replacement_matches

def find_omitted_words(text):
    omitted_word_pattern = r'\b0\w+\b'
    matches = re.findall(omitted_word_pattern, text)
    return matches

def find_word_fragments(text):
    word_fragment_pattern = r'&\+\w+'
    matches = re.findall(word_fragment_pattern, text)
    return matches

def find_annotations(text):
    annotation_pattern = r'\b(?:yyy|xxx)\b \[=! [^\]]+\]'
    matches = re.findall(annotation_pattern, text)
    annotations = [re.search(r'\[=! [^\]]+\]', match).group() for match in matches]
    return annotations

def find_nonverbal_activities(text):
    nonverbal_pattern = r'&=\w+(:\w+)?'
    matches = re.findall(nonverbal_pattern, text)
    return matches

def collect_all_matches(text):
    all_matches = []
    all_matches += find_retracing_markers(text)
    all_matches += find_interposed_words(text)
    all_matches += find_overlap_markers(text)
    all_matches += find_fillers(text)
    # all_matches += find_quotation_markers(text)
    all_matches += find_frozen_phrases(text)
    all_matches += find_errors_and_replacements(text)
    all_matches += find_omitted_words(text)
    all_matches += find_word_fragments(text)
    all_matches += find_annotations(text)
    all_matches += find_nonverbal_activities(text)
    all_matches += find_shortened_words(text)

    # Remove duplicates and empty values
    all_matches = list(set(filter(None, all_matches)))
    return all_matches

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
(a)bout don('t) (h)is (re)frigerator
an(d) (e)nough (h)isself (re)member
(a)n(d) (e)spress(o) -in(g) sec(ond)
(a)fraid (e)spresso nothin(g) s(up)pose
(a)gain (es)presso (i)n (th)e
(a)nother (ex)cept (in)stead (th)em
(a)round (ex)cuse Jag(uar) (th)emselves
ave(nue) (ex)cused lib(r)ary (th)ere
(a)way (e)xcuse Mass(achusetts) (th)ese
(be)cause (e)xcused micro(phone) (th)ey
(be)fore (h)e (pa)jamas (to)gether
(be)hind (h)er (o)k (to)mato
b(e)long (h)ere o(v)er (to)morrow
b(e)longs (h)erself (po)tato (to)night
Cad(illac) doc(tor) (h)im (h)imself prob(ab)ly (re)corder (un)til
"""

# Run the function to collect all matches and print the result
# all_matches = collect_all_matches(transcript_text)
# print(all_matches)
print(find_shortened_words(transcript_text))
