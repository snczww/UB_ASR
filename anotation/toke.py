from transformers import AutoTokenizer

# 初始化tokenizer
tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)

# 添加 fixed_annotations 为特殊标记
tokenizer.add_tokens(fixed_annotations, special_tokens=True)

# 确保 fixed_annotations 在标记化过程中被优先考虑
# 使用 tokenizer.encode 和 tokenizer.decode 示例
def encode_with_fixed_annotations(text, fixed_annotations, tokenizer):
    # 遍历 fixed_annotations，检查它们是否在输入文本中
    for annotation in fixed_annotations:
        if annotation in text:
            text = text.replace(annotation, f" {annotation} ")
    
    # 使用 tokenizer 进行编码
    encoded = tokenizer.encode(text, add_special_tokens=True)
    return encoded

# 示例文本
text = "示例文本，包含fixed_annotations"

# 编码示例文本
encoded_output = encode_with_fixed_annotations(text, fixed_annotations, tokenizer)
print(encoded_output)

# 解码以验证结果
decoded_output = tokenizer.decode(encoded_output)
print(decoded_output)
