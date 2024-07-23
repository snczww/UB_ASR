from tokenizers import normalizers
from tokenizers.normalizers import Lowercase, NFC, StripAccents, Replace

def create_normalizer(normalizer_config):
    normalizer_list = []

    if normalizer_config.get("lowercase", False):
        normalizer_list.append(Lowercase())

    if normalizer_config.get("nfc", False):
        normalizer_list.append(NFC())

    if normalizer_config.get("strip_accents", False):
        normalizer_list.append(StripAccents())

    replace_dict = normalizer_config.get("replace", {})
    for target, replacement in replace_dict.items():
        normalizer_list.append(Replace(target, replacement))

    return normalizers.Sequence(normalizer_list)
