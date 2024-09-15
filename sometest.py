from utils.anotaion_utils import *
candidate_path = 'anotation/cha_files/758_2.cha'
lines=extract_lines_from_file(candidate_path, prefix='*CHI:')
for i in lines:
    print(i)