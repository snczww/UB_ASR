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

def identify_markers(text):
    # Patterns for different markers
    trailing_off_pattern = r'\+\.\.\.'
    trailing_off_question_pattern = r'\+\.\.\?'
    interruption_pattern = r'\+\./\.'
    self_interruption_pattern = r'\+\./\.'

    # Finding all occurrences of each pattern
    trailing_off_matches = re.findall(trailing_off_pattern, text)
    trailing_off_question_matches = re.findall(trailing_off_question_pattern, text)
    interruption_matches = re.findall(interruption_pattern, text)
    self_interruption_matches = re.findall(self_interruption_pattern, text)

    # Count occurrences
    trailing_off_count = len(trailing_off_matches)
    trailing_off_question_count = len(trailing_off_question_matches)
    interruption_count = len(interruption_matches)
    self_interruption_count = len(self_interruption_matches)

    # Display the results
    print(f'Trailing Off (+...): {trailing_off_count}')
    print(f'Trailing Off Question (+..?): {trailing_off_question_count}')
    print(f'Interruption (+/.): {interruption_count}')
    print(f'Self Interruption (+//.): {self_interruption_count}')

# Example transcript text
transcript_text = """
*CHI: smells good enough for +...
*MOT: what were you saying ?
*EXP: so do you have any of these toys at home or +..?
*EXP: what did you do +/.
*CHI: mommy .
*EXP: +, with your spoon .
*MOT: well we haven’t started to +//.
*MOT: Alex put that down !
"""

# Identify markers in the transcript
identify_markers(transcript_text)

```




```
(.)
(?)
(!)
+...
+/.
+//.
[/]
```