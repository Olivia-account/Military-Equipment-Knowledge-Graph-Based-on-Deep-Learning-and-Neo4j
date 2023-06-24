import json
f=open('./datam/duie.json','r',encoding='utf-8')
for data in f:
    json_data = json.loads(data)
    print("id:",json_data['id'])
    for spo in json_data['spo_list']:
        print("subject:",spo["object"]["@value"],", predicate:",spo["predicate"],", object:",spo['subject'])
print('=============================================')
with open('output/result.json','r',encoding='utf8')as fp:
    json_data = json.load(fp)
    for para in json_data:
        print(para)
        for _,node in json_data[para]['nodes'].items():
            subject= node['名称']
            for n in node:
                if n != '名称':
                    if n =='label':
                        print("subject:", subject, ", predicate:", "label", ", object:", node[n])
                    else:
                        print("subject:",subject,", predicate:",n,", object:",node[n][0])
    print('这是文件中的json数据：',json_data)
    print('这是读取到文件数据的数据类型：', type(json_data))