from collections import defaultdict

# def damerau_levenshtein_distance(s1, s2):
#     '''
#     Considers neighboring transpositions when calculating difference between two sentences.
#     '''
#     s1 = [word.replace("Ġ", "").strip() for word in s1 if word not in ['<s>', '</s>'] and word.strip()]
#     s2 = [word.replace("Ġ", "").strip() for word in s2 if word not in ['<s>', '</s>'] and word.strip()]
#     s1 = list(filter(None, s1))
#     s2 = list(filter(None, s2))
#     d = {}
#     lenstr1 = len(s1)
#     lenstr2 = len(s2)

#     for i in range(-1, lenstr1 + 1):
#         d[(i, -1)] = i + 1

#     for j in range(-1, lenstr2 + 1):
#         d[(-1, j)] = j + 1

#     for i in range(lenstr1):
#         for j in range(lenstr2):
#             if s1[i] == s2[j]:
#                 cost = 0
#             else:
#                 cost = 1

#             d[(i, j)] = min(
#                 d[(i - 1, j)] + 1, 
#                 d[(i, j - 1)] + 1,  
#                 d[(i - 1, j - 1)] + cost,  
#             )

#             if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
#                 d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  

#     return d[lenstr1 - 1, lenstr2 - 1]

# def damerau_levenshtein_distance(s1, s2):


#     len1 = len(s1)
#     len2 = len(s2)
#     infinite = len1 + len2

#     # character array
#     da = defaultdict(int)

#     # distance matrix
#     score = [[0] * (len2 + 2) for x in range(len1 + 2)]

#     score[0][0] = infinite
#     for i in range(0, len1 + 1):
#         score[i + 1][0] = infinite
#         score[i + 1][1] = i
#     for i in range(0, len2 + 1):
#         score[0][i + 1] = infinite
#         score[1][i + 1] = i

#     for i in range(1, len1 + 1):
#         db = 0
#         for j in range(1, len2 + 1):
#             i1 = da[s2[j - 1]]
#             j1 = db
#             cost = 1
#             if s1[i - 1] == s2[j - 1]:
#                 cost = 0
#                 db = j

#             score[i + 1][j + 1] = min(
#                 score[i][j] + cost,
#                 score[i + 1][j] + 1,
#                 score[i][j + 1] + 1,
#                 score[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1),
#             )
#         da[s1[i - 1]] = i

#     return score[len1 + 1][len2 + 1]

# def damerau_levenshtein_distance(seq1, seq2):
#     """
#         Return the edit distance. This implementation runs in O(N*M) time using O(M) space.
#         This code implements the "optimal string alignment distance" algorithm.

#         Note that `seq1` and `seq2` can be any sequence type. This not only includes `str` but also includes `list`,
#         `tuple`, `range`, and more.

#         Examples:

#         >>> damerau_levenshtein_distance('smtih', 'smith')
#         1
#         >>> damerau_levenshtein_distance('saturday', 'sunday')
#         3
#         >>> damerau_levenshtein_distance('orange', 'pumpkin')
#         7
#         >>> damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4])
#         7
#     """
#     # possible short-circuit if sequences have a lot in common at the beginning (or are identical)
#     first_differing_index = 0
#     while first_differing_index < len(seq1) and \
#           first_differing_index < len(seq2) and \
#           seq1[first_differing_index] == seq2[first_differing_index]:
#         first_differing_index += 1

#     seq1 = seq1[first_differing_index:]
#     seq2 = seq2[first_differing_index:]

#     if not seq1:
#         return len(seq2)
#     if not seq2:
#         return len(seq1)

#     # Fix bug where the second sequence is one shorter than the first (#22).
#     if len(seq2) < len(seq1):
#         seq1, seq2 = seq2, seq1

#     m, n = len(seq1), len(seq2)
#     offset = n + 1
#     delete_cost, add_cost, subtract_cost = 0, 0, 0

#     # storage is a 3 x (len(seq2) + 1) array that stores TWO_AGO, ONE_AGO, and THIS_ROW
#     storage = [[0] * (n + 1) for _ in range(3)]

#     # initialize THIS_ROW
#     for i in range(1, offset):
#         storage[2][i - 1] = i

#     for i in range(m):
#         # swap/initialize vectors
#         storage[0], storage[1], storage[2] = storage[1], storage[2], [0] * (n + 1)
#         storage[2][n] = i + 1

#         # now compute costs
#         for j in range(n):
#             delete_cost = storage[1][j] + 1
#             add_cost = storage[2][j - 1] + 1 if j > 0 else i + 2
#             subtract_cost = storage[1][j - 1] + (seq1[i] != seq2[j]) if j > 0 else i + (seq1[i] != seq2[j])
#             storage[2][j] = min(delete_cost, add_cost, subtract_cost)
#             # deal with transpositions
#             if i > 0 and j > 0 and seq1[i] == seq2[j - 1] and seq1[i - 1] == seq2[j]:
#                 storage[2][j] = min(storage[2][j], storage[0][j - 1] + 1)

#     # compute and return the final edit distance
#     return storage[2][n - 1]
def damerau_levenshtein_distance(seq1, seq2):
    """
        Return the edit distance. This implementation runs in O(N*M) time using O(M) space.
        This code implements the "optimal string alignment distance" algorithm.

        Note that `seq1` and `seq2` can be any sequence type. This not only includes `str` but also includes `list`,
        `tuple`, `range`, and more.

        Examples:

        >>> damerau_levenshtein_distance('smtih', 'smith')
        1
        >>> damerau_levenshtein_distance('saturday', 'sunday')
        3
        >>> damerau_levenshtein_distance('orange', 'pumpkin')
        7
        >>> damerau_levenshtein_distance([1, 2, 3, 4, 5, 6], [7, 8, 9, 7, 10, 11, 4])
        7
    """
    # possible short-circuit if sequences have a lot in common at the beginning (or are identical)
    first_differing_index = 0
    while first_differing_index < len(seq1) and \
          first_differing_index < len(seq2) and \
          seq1[first_differing_index] == seq2[first_differing_index]:
        first_differing_index += 1

    seq1 = seq1[first_differing_index:]
    seq2 = seq2[first_differing_index:]

    # possible short-circuit if sequences have a lot in common at the end
    last_differing_index_seq1 = len(seq1) - 1
    last_differing_index_seq2 = len(seq2) - 1
    while last_differing_index_seq1 >= 0 and last_differing_index_seq2 >= 0 and \
          seq1[last_differing_index_seq1] == seq2[last_differing_index_seq2]:
        last_differing_index_seq1 -= 1
        last_differing_index_seq2 -= 1

    seq1 = seq1[:last_differing_index_seq1 + 1]
    seq2 = seq2[:last_differing_index_seq2 + 1]

    if not seq1:
        return len(seq2)
    if not seq2:
        return len(seq1)

    # Fix bug where the second sequence is one shorter than the first (#22).
    if len(seq2) < len(seq1):
        seq1, seq2 = seq2, seq1

    m, n = len(seq1), len(seq2)
    offset = n + 1
    delete_cost, add_cost, subtract_cost = 0, 0, 0

    # storage is a 3 x (len(seq2) + 1) array that stores TWO_AGO, ONE_AGO, and THIS_ROW
    storage = [[0] * (n + 1) for _ in range(3)]

    # initialize THIS_ROW
    for i in range(1, offset):
        storage[2][i - 1] = i

    for i in range(m):
        # swap/initialize vectors
        storage[0], storage[1], storage[2] = storage[1], storage[2], [0] * (n + 1)
        storage[2][n] = i + 1

        # now compute costs
        for j in range(n):
            delete_cost = storage[1][j] + 1
            add_cost = storage[2][j - 1] + 1 if j > 0 else i + 2
            subtract_cost = storage[1][j - 1] + (seq1[i] != seq2[j]) if j > 0 else i + (seq1[i] != seq2[j])
            storage[2][j] = min(delete_cost, add_cost, subtract_cost)
            # deal with transpositions
            if i > 0 and j > 0 and seq1[i] == seq2[j - 1] and seq1[i - 1] == seq2[j]:
                storage[2][j] = min(storage[2][j], storage[0][j - 1] + 1)

    # compute and return the final edit distance
    return storage[2][n - 1]

def word_error_rate(s1, s2):
    '''
    Calculates the WER percentage. 
    '''
    s1_words = s1.split()
    s2_words = s2.split()
    # print(s1_words)
    
    distance = damerau_levenshtein_distance(s1_words, s2_words)
    print(distance)
    return distance / len(s1_words)
def word_list_error_rate(s1_words, s2_words):
    '''
    Calculates the WER percentage. 
    '''
    # s1_words = s1.split()
    # s2_words = s2.split()
    distance = damerau_levenshtein_distance(s1_words, s2_words)
    
    return distance / len(s1_words)
reference = "this is test b a"
hypothesis = "this is a test b"

#example
# wer = word_error_rate(reference, hypothesis)
# print(f"Word Error Rate: {wer * 100:.2f}%")

s1=['now', 'the', 'rabbits', 'can', 'dump', 'the', 'sand', 'from', 'the', 'bucket', 'onto', 'the', 'sand', 'castle', '.']
s2=['and', 'now', '(.)', 'the', 'rabbit', '(i)s', 'going', 'to', '[?]', 'dump', 'the', 'sand', 'from', 'the', 'bucket', 'onto', 'the', 'sand', 'castle', '.']
a=damerau_levenshtein_distance(s1, s2)  # expected result: 7
print(a)