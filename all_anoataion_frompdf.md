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