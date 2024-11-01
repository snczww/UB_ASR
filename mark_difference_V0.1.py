import logging
import difflib

# 配置日志级别和输出格式
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# 定义相似性阈值
SIMILARITY_THRESHOLD = 0.5  # difflib 通过相似度得分判断，值在 0~1 之间

def is_similar(word1, word2, threshold=SIMILARITY_THRESHOLD):
    """使用 difflib 计算两个词的相似性，得分大于 threshold 则认为相似"""
    similarity_score = difflib.SequenceMatcher(None, word1, word2).ratio()
    return similarity_score >= threshold

def find_insertion_index(L, s2, idx_in_s2):
    """
    寻找在 L 中插入多余词的合适位置，依据 s2 中的原始位置。
    如果可能，在前后词之间插入。如果没有前后词，插入到空位或末尾。
    """
    # 寻找前一个非 '0' 的词
    previous_idx = idx_in_s2 - 1
    while previous_idx >= 0 and L[previous_idx] == '0':
        previous_idx -= 1

    # 寻找后一个非 '0' 的词
    next_idx = idx_in_s2 + 1
    while next_idx < len(L) and L[next_idx] == '0':
        next_idx += 1

    # 确保在前后词之间插入
    if previous_idx >= 0 and next_idx < len(L):
        logging.debug(f"Inserting between '{L[previous_idx]}' and '{L[next_idx]}' in L.")
        return next_idx  # 插入到后词之前
    elif previous_idx >= 0:
        logging.debug(f"Inserting after '{L[previous_idx]}' in L.")
        return previous_idx + 1  # 插入到前词之后
    else:
        logging.debug(f"Inserting at the end of L.")
        return len(L)  # 插入到 L 的末尾

def compare_and_fill(s1, s2):
    # 初始化与 s1 长度相同的空容器 L
    L = ['0'] * len(s1)
    
    logging.info(f"Initial L: {L}")

    # 使用一个副本来跟踪 s2 中剩余未匹配的词
    s2_remaining = s2[:]

    # 逐词比较 s1 和 s2，直接匹配相同的词
    for i, word_s1 in enumerate(s1):
        if word_s1 in s2_remaining:
            L[i] = word_s1  # 将相同的词放入 L 中相应的位置
            s2_remaining.remove(word_s1)  # 从 s2_remaining 中移除已匹配的词
            logging.debug(f"Found matching word '{word_s1}' for s1[{i}], placed in L.")
        else:
            logging.debug(f"No exact match for s1[{i}]='{word_s1}'.")

    # 处理 s1 中剩余的空位，检查 s2 剩余词是否相似
    for i, word_s1 in enumerate(s1):
        if L[i] == '0':  # 该位置为空，尝试查找相似词
            for word_s2 in s2_remaining:
                if is_similar(word_s1, word_s2):
                    L[i] = f"*{word_s2}*"  # 标记为相似词
                    s2_remaining.remove(word_s2)  # 移除匹配的词
                    logging.debug(f"Similar word '{word_s2}' found for s1[{i}]='{word_s1}', placed in L as '*{word_s2}*'.")
                    break  # 找到相似词后，停止对当前空位的进一步比较

    # 创建新容器 New，将 L 的内容复制到 New 中，不限制长度
    New = L[:]

    # 处理 s2 中剩余的词，按照它们的原始位置插入到 New 中
    for word_s2 in s2_remaining:
        idx_in_s2 = s2.index(word_s2)  # 获取它在 s2 中的位置
        logging.debug(f"Attempting to insert extra word '{word_s2}' at its original position {idx_in_s2} in New.")

        # 寻找在 New 中的合适插入位置
        insert_idx = find_insertion_index(New, s2, idx_in_s2)

        # 确保 New 的长度可以容纳插入位置
        if insert_idx >= len(New):
            New.extend(['0'] * (insert_idx - len(New) + 1))

        # 将多余的词插入到 New 中
        New.insert(insert_idx, f"-{word_s2}-")
        logging.debug(f"Inserted extra word '{word_s2}' at position {insert_idx} in New.")

    return New


# 示例数据
s1 = ["<um>", "[/]", "a", "rabbit", "and", "his", "dog", "(.)", "are", "making", "a", "sandcastle", "."]
s2 = ["&-um", "a", "cogb", "rabbit", "and", "his", "dog", "are", "making", "a", "sandcastle", "."]

# 调用函数
result = compare_and_fill(s1, s2)

# 输出结果
print("s1:", s1)
print("New: ", result)
