def damerau_levenshtein_distance_with_operations(s1_words, s2_words):
    """
    Calculate the Damerau-Levenshtein distance and return the list of operations to transform s2_words into s1_words.
    s1_words is treated as the fixed target.
    """
    d = {}
    lenstr1 = len(s1_words)
    lenstr2 = len(s2_words)

    # Initialize the table with base cases for insertion and deletion
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1

    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    operations = []  # Store the operations (insert, delete, replace, transpose)

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1_words[i] == s2_words[j]:
                cost = 0
            else:
                cost = 1

            # Initialize the table cell if not already set
            if (i - 1, j - 1) not in d:
                d[(i - 1, j - 1)] = float('inf')
            if (i - 1, j) not in d:
                d[(i - 1, j)] = float('inf')
            if (i, j - 1) not in d:
                d[(i, j - 1)] = float('inf')

            # Calculate the minimum cost for substitution, insertion, and deletion
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,    # Deletion
                d[(i, j - 1)] + 1,    # Insertion
                d[(i - 1, j - 1)] + cost  # Substitution
            )

            # Determine the operation based on minimum cost
            if d[(i, j)] == d[(i - 1, j)] + 1:
                operations.append(('delete', i, s1_words[i]))
            elif d[(i, j)] == d[(i, j - 1)] + 1:
                operations.append(('insert', j, s2_words[j]))
            elif d[(i, j)] == d[(i - 1, j - 1)] + cost and cost == 1:
                operations.append(('replace', i, s1_words[i], s2_words[j]))

            # Check for transposition
            if i > 0 and j > 0 and s1_words[i] == s2_words[j - 1] and s1_words[i - 1] == s2_words[j]:
                if d[(i, j)] > d[(i - 2, j - 2)] + 1:  # If transposition is better
                    operations.append(('transpose', i - 1, s1_words[i - 1], s1_words[i]))
                    i += 1
                    j += 1

    # Handle any remaining insertions
    while j < lenstr2:
        operations.append(('insert', j, s2_words[j]))
        j += 1

    # Handle any remaining deletions
    while i < lenstr1:
        operations.append(('delete', i, s1_words[i]))
        i += 1

    return operations


def edit_s2_to_s1_list(s1_words, s2_words):
    """
    Use Damerau-Levenshtein algorithm to show how to transform s2_words into s1_words.
    This function assumes both inputs are already tokenized lists.
    """
    # 获取将 s2_words 编辑成 s1_words 的操作列表
    operations = damerau_levenshtein_distance_with_operations(s1_words, s2_words)

    # 去重操作：确保每个操作只应用一次，并避免冗余的删除或插入操作
    filtered_operations = []
    seen = set()

    for op in operations:
        # 基于操作和索引进行去重
        if op not in seen:
            filtered_operations.append(op)
            seen.add(op)

    # 初始化结果列表为 s2_words 的副本
    result = s2_words[:]

    print("编辑操作：")
    last_action = None  # 用于避免连续的相同操作
    for op in filtered_operations:
        if last_action != op:  # 避免连续的相同操作
            if op[0] == 'insert':
                print(f"插入 '{op[2]}' 在 S2 中")
            elif op[0] == 'delete':
                print(f"删除 '{op[2]}' 在 S1 中")
            elif op[0] == 'replace':
                print(f"替换 '{op[3]}' 为 '{op[2]}'")
            elif op[0] == 'transpose':
                print(f"交换 '{op[2]}' 和 '{op[3]}'")
            last_action = op

    # 打印出S2与S1不同的部分，使用 `-` 标记S2中不同的部分
    print("\nS2 和 S1 不同的部分：")
    s2_marked = []
    s2_index = 0

    for i in range(len(s1_words)):
        if s2_index < len(s2_words) and s1_words[i] == s2_words[s2_index]:
            s2_marked.append(s2_words[s2_index])
        else:
            if s2_index < len(s2_words):
                s2_marked.append(f"-{s2_words[s2_index]}-")  # 用 `-` 标记 S2 中不同的部分
            else:
                s2_marked.append("-")  # 如果 S2 缺少对应单词，用 `-` 标记
        s2_index += 1

    print("S1:", ' '.join(s1_words))
    print("S2:", ' '.join(s2_marked))

    return filtered_operations


# 示例调用
s1_list = ["<um>", "[/]", "a", "rabbit", "and", "his", "dog", "(.)", "are", "making", "a", "sandcastle", "."]
s2_list = ["&-um", "a", "rabbit", "and", "his", "dog", "are", "making", "a", "sandcastle", "."]

# 调用函数，显示如何将 s2_list 编辑成 s1_list
edit_operations = edit_s2_to_s1_list(s1_list, s2_list)
