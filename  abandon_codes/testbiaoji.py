def compare_strings(s1, s2):
    # 定义颜色代码
    red_start = "\033[91m"   # 红色用于替换部分
    orange_start = "\033[93m" # 橙色用于缺少部分
    green_start = "\033[92m" # 绿色用于增加部分
    color_end = "\033[0m"    # 颜色结束

    result_s2 = ""  # 用于保存标记后的S2

    # 定义变量存储两个字符串的指针
    i, j = 0, 0
    while i < len(s1) and j < len(s2):
        if s1[i] == s2[j]:  # 如果字符相同，直接添加到result_s2
            result_s2 += s2[j]
            i += 1
            j += 1
        else:
            # 处理S1中存在但S2中不存在的部分（缺少）
            if s1[i] == '<' or s1[i] == '[' or s1[i] == '(':
                # 找到S1中的缺少部分，直到结束标记
                end_char = '>'
                if s1[i] == '[':
                    end_char = ']'
                elif s1[i] == '(':
                    end_char = ')'
                missing_part = ""
                while i < len(s1) and s1[i] != end_char:
                    missing_part += s1[i]
                    i += 1
                missing_part += end_char  # 添加结束字符
                i += 1  # 跳过结束字符
                result_s2 += orange_start + f"(缺少 {missing_part})" + color_end  # 标记为缺少
            else:
                # S1和S2字符不同，标记S2中的替换部分
                result_s2 += red_start + s2[j] + color_end
                i += 1
                j += 1

    # 处理剩余的S2部分（S2 比 S1 长时）
    while j < len(s2):
        result_s2 += green_start + s2[j] + color_end  # 标记增加的部分
        j += 1

    # 处理剩余的S1部分（S1 比 S2 长时，缺失的部分）
    while i < len(s1):
        result_s2 += orange_start + f"(缺少 {s1[i]})" + color_end
        i += 1

    return result_s2


# 示例字符串
s1 = "<um> [/] a rabbit and his dog (.) are making a sandcastle."
s2 = "&-um a rabbit and his dog are making a sandcastle."

# 调用函数进行对比
# result = compare_strings(s1, s2)

# # 输出对比结果
# print("标记后的S2：")
# print(result)
