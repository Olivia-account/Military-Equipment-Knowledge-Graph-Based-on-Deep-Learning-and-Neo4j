import difflib
import json
def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
#
#
# print(string_similar('奥什科什M1070系列', '奥什科什M1070系列'))
# print(string_similar('奥什科什M1070系列', '象式坦克运输车'))
# print(string_similar('撒拉逊轮式输送车', '象式坦克运输车'))

def find_similar_node(result_file):
    all_subject = []
    with open(result_file, 'r',
              encoding='utf8')as fp:
        json_data = json.load(fp)
        for para in json_data:
            # print("第", para, "段文本中提取的三元组：")
            for _, node in json_data[para]['nodes'].items():
                subject = node['名称']
                all_subject.append(subject)
                # for n in node:
                #     if n != '名称':
                #         if n == 'label':
                #             print("subject:", subject, ", predicate:", "label", ", object:", node[n][0])
                #         else:
                #             print("subject:", subject, ", predicate:", n, ", object:", node[n][0])
    graph_data=[]
    f = open(r'F:\graduate_design\code\relation_k\datam\military.json', 'r', encoding='utf-8')
    for data in f:
        data=json.loads(data)
        graph_data.append(data['名称'])


    for sub in all_subject:
        similar_verb = {}
        for verb in graph_data:
            similar_ratio=string_similar(sub, verb)
            if similar_ratio>=0.7:
                similar_verb[verb]=similar_ratio
        if len(similar_verb)>1:
            # 进行相似度排序
            d_order = sorted(similar_verb.items(), key=lambda x: x[1], reverse=True)
            if len(similar_verb)<=3:
                new_dict = {}
                for i in d_order:
                    new_dict[i[0]] = i[1]
                similar_verb = new_dict
            else:
                new_dict={}
                for i in d_order[:3]:
                    new_dict[i[0]]=i[1]
                similar_verb=new_dict

        print("相似度高的实体：",similar_verb)


input_path=r'F:\graduate_design\code\relation_k\output\result.json'
find_similar_node(input_path)

