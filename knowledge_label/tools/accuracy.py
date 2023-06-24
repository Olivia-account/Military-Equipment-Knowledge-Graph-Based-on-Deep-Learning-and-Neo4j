import json
f=open('./datam/duie.json','r',encoding='utf-8')
for data in f:
    json_data = json.loads(data)
    #print("id:",json_data['id'])
    for spo in json_data['spo_list']:
        print("subject:",spo["object"]["@value"],", predicate:",spo["predicate"],", object:",spo['subject'])
with open('output/result.json','r',encoding='utf8')as fp:
    json_data = json.load(fp)
    print('这是文件中的json数据：',json_data)
    print('这是读取到文件数据的数据类型：', type(json_data))