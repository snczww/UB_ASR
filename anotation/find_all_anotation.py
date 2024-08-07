import re

def find_annotations(text):
    # Define patterns for different types of annotations
    patterns = {
        'Retracing with brackets': r'(<[^>]+> \[//\])|(<[^>]+> \[/\])',
        'Single word retracing': r'(\b\w+\b \[/\])',
        'Retracing with fillers': r'(<[^>]+> \[/\] \(.*?\) &-[a-z]+ \[.*?\])',
        'Bracketed phrases': r'<[^>]+>',
        'Interposed words': r'&\*[A-Z]{3}:[a-zA-Z]+',
        'Overlap follows markers': r'<([^>]+)> \[>\]',
        'Overlap precedes markers': r'<([^>]+)> \[<\]',
        'Fillers': r'&-[a-zA-Z_]+',
        'Quotation Precedes markers': r'\+\”[^.]*',
        'Single quoted words': r'\b\w+@q\b',
        'Frozen phrases': r'\b\w+(?:_\w+)+\b',
        'Errors': r'\[\*\]',
        'Target Replacements': r'\[: [^\]]+\]',
        'Omitted words': r'\b0\w+\b',
        'Word fragments': r'&\+\w+',
        'Annotations': r'\b(?:yyy|xxx)\b \[=! [^\]]+\]',
        'Non-verbal activities': r'&=\w+(:\w+)?'
    }

    results = {key: re.findall(pattern, text) for key, pattern in patterns.items()}

    # Display the results
    for key, matches in results.items():
        print(f'{key}:')
        for match in matches:
            if isinstance(match, tuple):
                match = [m for m in match if m]  # Remove empty strings from tuple
                print(' '.join(match))
            else:
                print(match)
        print()

# Example transcript text
transcript_text = """
*CHI: <I wanted> [/] I wanted to invite Margie .
*CHI: it's [/] (.) &-um (.) it's [/] it's (.) a &-um (.) dog .
*CHI: apple [/] apple is good.
*CHI: <I wanted> [//] &-uh I thought I wanted to invite Margie .
*CHI: <the fish is> [//] the [/] the fish are swimming .
*CHI: <it was> [//] it is a sunny day. 
*PAR: it was really difficult &*INV:mhm when all of that was happening.
*CHI: I think &*MOT:yeah that it's a good idea.
*EXP: This is interesting &*PAR:uh-huh but could you explain more?
*INV: how did you communicate <with her> [>] ?
*PAR: <I just kept talking> [<] .
*CHI: <it was very> [>] interesting.
*EXP: <I thought> [<] it was too.
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

# Find all annotations in the transcript
find_annotations(transcript_text)
