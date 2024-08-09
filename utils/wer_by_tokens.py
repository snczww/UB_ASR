def damerau_levenshtein_distance(s1, s2):
    '''
    Considers neighboring transpositions when calculating difference between two sentences.
    '''
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)

    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1

    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1

            d[(i, j)] = min(
                d[(i - 1, j)] + 1, 
                d[(i, j - 1)] + 1,  
                d[(i - 1, j - 1)] + cost,  
            )

            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  

    return d[lenstr1 - 1, lenstr2 - 1]

def word_error_rate(s1, s2):
    '''
    Calculates the WER percentage. 
    '''
    s1_words = s1.split()
    s2_words = s2.split()
    # print(s1_words)
    distance = damerau_levenshtein_distance(s1_words, s2_words)
    return distance / len(s1_words)
def word_list_error_rate(s1_words, s2_words):
    '''
    Calculates the WER percentage. 
    '''
    # s1_words = s1.split()
    # s2_words = s2.split()
    distance = damerau_levenshtein_distance(s1_words, s2_words)
    return distance / len(s1_words)
reference = "this is test a"
hypothesis = "this is a test"

#example
# wer = word_error_rate(reference, hypothesis)
# print(f"Word Error Rate: {wer * 100:.2f}%")