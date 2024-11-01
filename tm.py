# from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance
# damerau_levenshtein_distance('smtih', 'smith')  # expected result: 1
# # print(damerau_levenshtein_distance('smtih', 'smthi') )
# normalized_damerau_levenshtein_distance('smtih', 'smith')  # expected result: 0.2
# # print(normalized_damerau_levenshtein_distance('smtih', 'smith') )
# s1=['now', 'the', 'rabbits', 'can', 'dump', 'the', 'sand', 'from', 'the', 'bucket', 'onto', 'the', 'sand', 'castle', '.']
# s2=['and', 'now', '(.)', 'the', 'rabbit', '(i)s', 'going', 'to', '[?]', 'dump', 'the', 'sand', 'from', 'the', 'bucket', 'onto', 'the', 'sand', 'castle', '.']

# a=damerau_levenshtein_distance(s1, s2)  # expected result: 7
# # print(a)
# from pyxdameraulevenshtein import damerau_levenshtein_distance_seqs, normalized_damerau_levenshtein_distance_seqs
# array = ['test1', 'test12', 'test123']
# damerau_levenshtein_distance_seqs('test', array)  # expected result: [1, 2, 3]
# normalized_damerau_levenshtein_distance_seqs('test', array)  # expected result: [0.2, 0.33333334, 0.42857143]

# reference = "this is test b a"
# hypothesis = "this is a test b"
# s1_words = reference.split()
# s2_words = hypothesis.split()
# #example
# print(normalized_damerau_levenshtein_distance(s1_words, s2_words) )

def highlight_edit_operations(s1, s2):
    """
    Highlight the operations (insert, delete, replace) needed to transform s2 into s1.
    - Replacement: <span style="color: green;"></span>
    - Insertion: <span style="color: blue;"></span>
    - Deletion: <span style="color: red;"></span>

    Args:
    s1 (list): Target sequence.
    s2 (list): Source sequence.

    Returns:
    str: A string representing the highlighted transformations.
    """
    import numpy as np

    m, n = len(s1), len(s2)
    dp = np.zeros((m + 1, n + 1), dtype=int)

    # Fill the dp array
    for i in range(1, m + 1):
        dp[i][0] = i
    for j in range(1, n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,   # Deletion
                               dp[i][j - 1] + 1,   # Insertion
                               dp[i - 1][j - 1] + 1)  # Replacement

    # Backtrack to determine operations
    i, j = m, n
    result = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # Replacement
            result.append(f"<span style=\"color: green;\">{s2[j - 1]} → {s1[i - 1]}</span>")
            i -= 1
            j -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            # Insertion
            result.append(f"<span style=\"color: blue;\">{s2[j - 1]}</span>")
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # Deletion
            result.append(f"<span style=\"color: red;\">{s1[i - 1]}</span>")
            i -= 1

    # Reverse the result since we built it backwards
    result.reverse()

    return ' '.join(result)

# Example usage
s1 = ['now', 'the', 'rabbits', 'can', 'dump', 'the', 'sand', 'from', 'the', 'bucket', 'onto', 'the', 'sand', 'castle', '.']
s2 = ['and', 'now', '(.)', 'the', 'rabbit', '(i)s', 'going', 'to', '[?]', 'dump', 'the', 'sand', 'from', 'the', 'bucket', 'onto', 'the', 'sand', 'castle', '.']

highlighted_output = highlight_edit_operations(s1, s2)
print(highlighted_output)