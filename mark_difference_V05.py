# Python implementation for marking the changes between two strings based on word-level differences
def mark_word_changes(s1_words, s2_words):
    # s1_words = s1.split()
    # s2_words = s2.split()
    
    i, j = 0, 0
    result = []
    
    while i < len(s1_words) and j < len(s2_words):
        if s1_words[i] == s2_words[j]:
            # No change
            result.append(s1_words[i])
            i += 1
            j += 1
        elif s1_words[i] != s2_words[j]:
            if i + 1 < len(s1_words) and s1_words[i + 1] == s2_words[j]:
                # Deletion in s1
                result.append(f"-{s1_words[i]}-")
                i += 1
            elif j + 1 < len(s2_words) and s1_words[i] == s2_words[j + 1]:
                # Insertion in s2
                result.append(f"+{s2_words[j]}+")
                j += 1
            else:
                # Replacement
                result.append(f"*{s1_words[i]}*")
                i += 1
                j += 1
    
    # Handle remaining words in either s1 or s2
    while i < len(s1_words):
        result.append(f"-{s1_words[i]}-")
        i += 1
    
    while j < len(s2_words):
        result.append(f"+{s2_words[j]}+")
        j += 1
    
    return " ".join(result)

# Test case with provided strings
# s1 = "blood bit a dog"
# s2 = "bleed bit o big dog"
# s2 = ["<um>", "[/]", "a", "rabbit", "and", "his", "dog", "(.)", "are", "making", "a", "sandcastle", "."]
# s1 = ["&-um", "a", "cogb", "rabbit", "and", "his", "dog", "are", "making", "a", "sandcastle", "."]


# # Apply the function
# marked_result = mark_word_changes(s1, s2)
# print(marked_result)
