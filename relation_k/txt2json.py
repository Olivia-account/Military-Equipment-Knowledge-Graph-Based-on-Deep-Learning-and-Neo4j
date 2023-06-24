import codecs
import json
import re

input_txt = r'C:\Users\zhour\PycharmProjects\PD_env\relation_extraction\datam\input.txt'   # 文件路径

para_id=0
with open(input_txt, "r", encoding='utf-8') as f:
    for line in f.readlines():  # 打开后逐行读取
        # sentence = re.split('。', line.strip())
        # for s in sentence:
        #     if s !='':
        #         str = {"text": s,"id":para_id}
        #         with codecs.open("test_label.json", 'a', 'utf-8') as f:
        #             str = json.dumps(str, ensure_ascii=False)
        #             f.write(str)
        #             f.write('\n')
        s = line.strip()
        if s !='':
            str = {"text": s,"id":para_id}
            with codecs.open("test_label.json", 'a', 'utf-8') as f:
                str = json.dumps(str, ensure_ascii=False)
                f.write(str)
                f.write('\n')
        para_id+=1