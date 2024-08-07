### Punctuation
- period (.) question mark (?) or exclamation point (!)
- Trailing Off +...
- Interruption +/.
```
*EXP: what did you do +/.
*CHI: mommy .
*EXP: +, with your spoon .
```
- Self Interruption +//.

- Retracing Without Correction [/] (also in fluency codes, Appendix 7)

the material being retraced is enclosed in angle
brackets. In a retracing without correction, it is necessarily the case that the material in angle
brackets is the same as the material immediately following the [/] symbol.
```
*CHI: <I wanted> [/] I wanted to invite Margie .
```
``` python
import re

import re

def find_retracing_markers(text):
    # Define patterns for different types of retracing markers
    retracing_with_brackets_pattern = r'(<[^>]+> \[//\])|(<[^>]+> \[/\])'
    retracing_single_word_pattern = r'(\b\w+\b \[/\])'
    retracing_with_fillers_pattern = r'(<[^>]+> \[/\] \(.*?\) &-[a-z]+ \[.*?\])'

    # Finding all occurrences of each pattern
    retracing_with_brackets_matches = re.findall(retracing_with_brackets_pattern, text)
    retracing_single_word_matches = re.findall(retracing_single_word_pattern, text)
    retracing_with_fillers_matches = re.findall(retracing_with_fillers_pattern, text)

    # Extract only the matched group that is not empty (re.findall with multiple groups can return tuples with empty strings)
    retracing_with_brackets_matches = [match[0] if match[0] else match[1] for match in retracing_with_brackets_matches]

    # Display the results
    print('Retracing with brackets:')
    for match in retracing_with_brackets_matches:
        print(match)
''' don't need

    print('\nSingle word retracing:')
    for match in retracing_single_word_matches:
        print(match)
    
    print('\nRetracing with fillers:')
    for match in retracing_with_fillers_matches:
        print(match)
'''
# Example transcript text
transcript_text = """
*CHI: <I wanted> [/] I wanted to invite Margie .
*CHI: it's [/] (.) &-um (.) it's [/] it's (.) a &-um (.) dog .
*CHI: apple [/] apple is good.
"""

# Find retracing markers in the transcript
find_retracing_markers(transcript_text)


```
- Retracing with Correction [//]

``` python
import re

def find_bracketed_phrases(text):
    # Define the pattern to match phrases inside <>
    bracketed_pattern = r'<[^>]+>'

    # Find all occurrences of the pattern
    matches = re.findall(bracketed_pattern, text)

    # Display the results
    print('Bracketed phrases:')
    for match in matches:
        print(match)

# Example transcript text
transcript_text = """
*CHI: <I wanted> [//] &-uh I thought I wanted to invite Margie .
*CHI: <the fish is> [//] the [/] the fish are swimming .
*CHI: <it was> [//] it is a sunny day. 
"""

# Find bracketed phrases in the transcript
find_bracketed_phrases(transcript_text)
```

all synbol
```
(.)
(?)
(!)
+...
+/.
+//.
[/]
[//]
```

### Overlaps
- Interposed word &*
``` python
import re

def find_interposed_words(text):
    # Define the pattern for interposed words
    interposed_pattern = r'&\*[A-Z]{3}:[a-zA-Z]+'

    # Find all occurrences of the pattern
    matches = re.findall(interposed_pattern, text)

    # Display the results
    print('Interposed words:')
    for match in matches:
        print(match)

# Example transcript text
transcript_text = """
*PAR: it was really difficult &*INV:mhm when all of that was happening.
*CHI: I think &*MOT:yeah that it's a good idea.
*EXP: This is interesting &*PAR:uh-huh but could you explain more?
"""

# Find interposed words in the transcript
find_interposed_words(transcript_text)
```

- Lazy overlap +<
- Overlap follows [>]
``` python
import re

def find_overlap_markers(text):
    # Define the patterns for overlap markers
    overlap_follows_pattern = r'<([^>]+)> \[>\]'
    overlap_precedes_pattern = r'<([^>]+)> \[<\]'

    # Find all occurrences of each pattern
    overlap_follows_matches = re.findall(overlap_follows_pattern, text)
    overlap_precedes_matches = re.findall(overlap_precedes_pattern, text)

    # Display the results
    print('Overlap follows markers:')
    for match in overlap_follows_matches:
        print(f"<{match}> [>]")
    
    print('\nOverlap precedes markers:')
    for match in overlap_precedes_matches:
        print(f"<{match}> [<]")

# Example transcript text
transcript_text = """
*INV: how did you communicate <with her> [>] ?
*PAR: <I just kept talking> [<] .
*CHI: <it was very> [>] interesting.
*EXP: <I thought> [<] it was too.
"""

# Find overlap markers in the transcript
find_overlap_markers(transcript_text)

```
all synbol
```
+<
```
### FLUENCY codes
- Unfilled pauses

```
(.)
(..)
(...)
```
- Filled pauses

``` python
import re

def find_fillers(text):
    # Define the pattern for fillers marked with &-
    fillers_pattern = r'&-[a-zA-Z_]+'

    # Find all occurrences of the pattern
    matches = re.findall(fillers_pattern, text)

    # Display the results
    print('Fillers:')
    for match in matches:
        print(match)

# Example transcript text
transcript_text = """
*CHI: I was like &-um going to the store &-you_know to buy some &-stuff.
*INV: So, &-like, what do you think about that?
*PAR: Well, &-you_know, it's kind of &-um complicated.
"""

# Find fillers in the transcript
find_fillers(transcript_text)

```
- Quotation on Next Line +”/.
- Quotation Precedes +”





``` python
import re

def find_quotation_markers(text):
    # Define the pattern for "Quotation Precedes" and single quoted words
    quotation_precedes_pattern = r'\+\”[^.]*'
    single_quoted_words_pattern = r'\b\w+@q\b'

    # Find all occurrences of each pattern
    quotation_precedes_matches = re.findall(quotation_precedes_pattern, text)
    single_quoted_words_matches = re.findall(single_quoted_words_pattern, text)

    # Display the results
    # print('Quotation Precedes markers:')
    # for match in quotation_precedes_matches:
    #     print(match)
    
    print('\nSingle quoted words:')
    for match in single_quoted_words_matches:
        print(match)

# Example transcript text
transcript_text = """
*CHI: +” please give me all of your honey .
*CHI: the little bear said +”.
*CHI: and the boy said shh@q .
"""

# Find quotation markers in the transcript
find_quotation_markers(transcript_text)

```
- Multiple words that should hang together
``` python
import re

def find_frozen_phrases(text):
    # Define the pattern for frozen phrases linked with underscores
    frozen_phrases_pattern = r'\b\w+(?:_\w+)+\b'

    # Find all occurrences of the pattern
    matches = re.findall(frozen_phrases_pattern, text)

    # Display the results
    print('Frozen phrases:')
    for match in matches:
        print(match)

# Example transcript text
transcript_text = """
*CHI: I think you_know that patty_cake is a fun game.
*INV: What do you think about Nan_Bernstein_Ratner's work?
*PAR: Well, Mister_Spock was a character in Star Trek.
*CHI: We went to the merry_go_round yesterday.
"""

# Find frozen phrases in the transcript
find_frozen_phrases(transcript_text)
```
- Other Coding Conventions: ERRORS!
``` python
import re

def find_errors_and_replacements(text):
    # Define the patterns for errors and target replacements
    error_pattern = r'\[\*\]'
    replacement_pattern = r'\[: [^\]]+\]'

    # Find all occurrences of each pattern
    error_matches = re.findall(error_pattern, text)
    replacement_matches = re.findall(replacement_pattern, text)

    # Display the results
    # print('Errors:')
    # for match in error_matches:
    #     print(match)
    
    print('\nTarget Replacements:')
    for match in replacement_matches:
        print(match)

# Example transcript text
transcript_text = """
*CHI: he had two mouses [: mice] [*] .
*CHI: two cookie [*].
*CHI: to [*] home.
*CHI: he going to the store.
"""

# Find errors and replacements in the transcript
find_errors_and_replacements(transcript_text)

```
- Missing words: 0
``` python
import re

def find_omitted_words(text):
    # Define the pattern for omitted words marked with the zero symbol
    omitted_word_pattern = r'\b0\w+\b'

    # Find all occurrences of the pattern
    matches = re.findall(omitted_word_pattern, text)

    # Display the results
    print('Omitted words:')
    for match in matches:
        print(match)

# Example transcript text
transcript_text = """
*CHI: 0does he like it?
*PAR: 0mod he like it?
*CHI: 0is she going?
*PAR: 0has he done it?
"""

# Find omitted words in the transcript
find_omitted_words(transcript_text)

```
- Phonological Fragments &+fr
``` python
import re

def find_word_fragments(text):
    # Define the pattern for word fragments marked with &+
    word_fragment_pattern = r'&\+\w+'

    # Find all occurrences of the pattern
    matches = re.findall(word_fragment_pattern, text)

    # Display the results
    print('Word fragments:')
    for match in matches:
        print(match)

# Example transcript text
transcript_text = """
*CHI: he had a &+fr friend.
*CHI: I really wanted to &+vi visit the zoo.
*CHI: she is &+un unbelievable.
"""

# Find word fragments in the transcript
find_word_fragments(transcript_text)

```
- Unintelligible words xxx
- Pauses (.)
- Babbling and Jargon (from kids or patients)
``` python
import re

def find_annotations(text):
    # Define the pattern to match annotations [=! ...] following yyy or xxx
    annotation_pattern = r'\b(?:yyy|xxx)\b \[=! [^\]]+\]'

    # Find all occurrences of the pattern
    matches = re.findall(annotation_pattern, text)

    # Extract and display the annotations
    print('Annotations:')
    for match in matches:
        # Extract the [=! ...] part
        annotation = re.search(r'\[=! [^\]]+\]', match).group()
        print(annotation)

# Example transcript text
transcript_text = """
*CHI: yyy [=! dada] .
*CHI: xxx [=! vocalizes/laughs/whines, etc] .
*PAR: I probably got xxx and things like that .
"""

# Find annotations in the transcript
find_annotations(transcript_text)

```

- Tables for Other Communicative Behaviors and Words



all synbol
```
+”/.
+”
[*]
xxx
yyy
(.)
```
~~## Simple Events (not required [could replace to same words])~~
``` python
import re

def find_nonverbal_activities(text):
    # Define the pattern for non-verbal activities marked with &=
    nonverbal_pattern = r'&=\w+(:\w+)?'

    # Find all occurrences of the pattern
    matches = re.findall(nonverbal_pattern, text)

    # Display the results
    print('Non-verbal activities:')
    for match in matches:
        print(match)

# Example transcript text
transcript_text = """
*CHI: he had a &+fr friend.
*CHI: I really wanted to &+vi visit the zoo.
*CHI: she is &+un unbelievable.
*CHI: &=moans loudly.
*CHI: &=laughs and &=coughs.
*CHI: makes a noise &=imit:plane.
*CHI: gestures with frustration &=ges:frustration.
*CHI: moves the doll &=moves:doll.
*CHI: shows pictures &=shows:pictures.
*CHI: points to the picture &=points:picture.
*CHI: opens mouth &=opens:mouth.
"""

# Find non-verbal activities in the transcript
find_nonverbal_activities(transcript_text)

```




``` python

```
``` python

```