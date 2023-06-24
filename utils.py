# coding=utf-8
import datetime
import os
import random
import time
import re
import json
import difflib
import shutil
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
import sys
import requests
from lxml import etree as et
import urllib
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import json
import time
import random
import os

# graph = Graph("http://localhost:7474/", auth=("neo4j", "123456"))
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
# driver = GraphDatabase.driver(uri, auth=("neo4j", "123456"))  # 搭建驱动器

root = os.path.abspath(os.path.dirname(__file__))
database_root = root + '/data/database/'

openkgdata_root = root + '/data/openkg_data/military.json'
newsClips_root = root + '/data/'

# 改变json文件格式
def changeJsonFormat(contents):
    contents = contents.replace('\n', '').replace(' ', '').split('}{')
    print(contents)
    for i in range(len(contents)):
        if i == 0:
            contents[0] = contents[0] + '}'
        elif i>= 1 and i<len(contents)-1:
            contents[i] = '{'+ contents[i] + '}'
        else:
            contents[-1] = '{'+ contents[-1]
        
        contents[i] = json.loads(contents[i]) 
    # print(contents)
    return contents


# 根据database_id找到database名称
def FindDatabase(database_id):
    """
    作用：根据database_id找到database名称
    输入：database_id
    输出：database名称
    """
    database_list = []
    database = ''
    # 遍历database_root下的文件和文件夹
    for root, dirs, files in os.walk(database_root):
        database_list = dirs
        break
    for i in database_list:
        if database_id in i:
            database = i
            break
    return database


# 返回数据集下的Datafiles的所有文件
def DataPath(database_id):
    """
    作用：返回数据集下的Datafiles的所有文件
    输入：database_id
    输出：数据集下的Datafiles的所有文件列表
    """
    database = FindDatabase(database_id)
    # 生成数据集下的Datafiles的所有文件列表
    files_path = database_root + database + '/DataFiles/'
    for root, dirs, files in os.walk(files_path):
        for i in range(len(files)):
            files[i] = files_path + files[i]
        files_list = files
    return files_list


# 读取database中的文本数据到 datam/input.txt 里面
def ReadDatabaseText(database_id):
    """
    作用：读取database中的文本数据到 datam/input.txt 里面
    输入：数据集id
    输出：
    """
    files_list = DataPath(database_id)
    text_list = []
    # 遍历数据集中的DataFiles
    for f_path in files_list:
        print(f_path)
        os.path.basename(f_path)
        for data in open(f_path, 'r', encoding='utf-8'):

            for key, item in eval(data).items():
                text_list.append(item['text'])
    f_path = root + '/relation_k/datam/input.txt'
    with open(f_path, 'w', encoding='utf-8') as f:
        f.write('')
    for i in text_list:
        with open(f_path, 'a', encoding='utf-8') as f:
            f.write(i)
            f.write('\n')
    print('ReadDatabaseText', '成功')
    return text_list

# print(ReadDatabaseText('1003172907'))


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def FindSimilarNode(json_data):
    all_subject = []
    ans = []
    # 从这里输入字典
    for para in json_data:
        for _, node in json_data[para]['nodes'].items():
            if '名称' in node:
                subject = node['名称']
                all_subject.append(subject)
            else:
                subject = node['name']
                all_subject.append(subject)

    graph_data = []
    f = open(openkgdata_root, 'r', encoding='utf-8')
    for data in f:
        data = json.loads(data)
        label = []
        if '类型' in data:
            label.append(data['类型'])
        if '大类' in data:
            label.append(data['大类'])
        if 'label' in data:
            label.append(data['label'])
        if 'labels' in data:
            label.append(data['labels'])
        graph_data.append([data['名称'], label])
    for sub in all_subject:
        similar_verb = {}
        for verb in graph_data:
            similar_ratio = string_similar(sub, verb[0])
            if similar_ratio >= 0.77:
                similar_verb[verb[0]] = [str(round(similar_ratio * 100, 2)) + "%", sub, verb[1]]
        if len(similar_verb) > 1:
            # 进行相似度排序
            d_order = sorted(similar_verb.items(), key=lambda x: x[1], reverse=True)
            for i in d_order:
                ans.append([{i[0]: i[1]}, i[1][1]])
    return ans

# data1 = {'0': {'nodes': {'node1': {'label': ['飞行器'], '名称': '歼-11BS战斗机', '产国': '中国', '研发单位与厂商': '中国', 'isChoose': 'true'}}}, '1': {'nodes': {'node1': {'label': ['主战坦克', '坦克装甲车辆'], '名称': 'J-16 multirole fighter', '产国': '中国', '研发单位与厂商': '中国', 'isChoose': 'true'}}}, '2': {'nodes': {'node1': {'label': ['主战坦克', '坦克装甲车辆'], '名称': '苏-', '产国': '中国', 'isChoose': 'true'}}}, '3': {'nodes': {'node1': {'label': ['飞行器'], '名称': '歼-11BS战斗机（测试）', '研发单位与产商': '中国沈阳飞机公司', 'isChoose': 'true'}}}, '4': {'nodes': {'node1': {'label': ['生产研发厂商'], '名称': '中国沈阳飞机公司', 'isChoose': 'true'}}}, '5': {'nodes': {'node1': {'label': ['生产研发厂商'], '名称': '前卫仪表厂', 'isChoose': 'true'}}}, '6': {'nodes': {'node1': {'label': ['国家'], '名称': '中国', 'isChoose': 'true'}}}, '7': {'nodes': {'node1': {'label': ['生产研发单位'], '名称': '中国沈阳飞机公司', 'isChoose': 'true'}}}}
# print(FindSimilarNode(data1))


# 返回数据集列表及其基本信息
def DatabaseList():
    """
    作用：返回数据集列表及其基本信息
    输入：
    输出：数据集列表及其基本信息
    """
    database_info_list = []
    for root, dirs, files in os.walk(database_root):
        database_list = dirs
        print(database_list)
        for i in range(len(database_list)):
            with open(database_root + database_list[i] + '/基本信息.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                data['location'] = 'top:' + str(111 + i * 179) + 'px;'
                database_info_list.append(data)
        print('DatabaseList', '成功')
        break

    return database_info_list

# print(DatabaseList())


# 根据database_id删除数据集
def DeleteDatabase(database_id):
    """
    作用：根据database_id删除数据集
    输入：database_id
    输出：
    """
    path = database_root + FindDatabase(database_id)
    shutil.rmtree(path)
    print('删除的路径:', path)
    print('DeleteDatabase', '成功')

# DeleteDatabase('567646')


# 创建数据集
def CreateDatabase(name, remarks, datatype):
    """
    作用：创建数据集的相应信息与路径
    输入：数据集名称、备注、上传的数据类型
    输出：随机生成的数据集ID、名称、创建时间、导入状态、数据类型、标注进度、备注
    """
    basic_data = {}
    basic_data['database_id'] = time.strftime('%m%d%H%M%S', time.localtime(time.time()))
    basic_data['name'] = name  # 名称
    basic_data['version'] = 1.0  # 版本
    basic_data['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d')  # 创建时间
    basic_data['input_state'] = '成功'  # 导入状态
    basic_data['datatype'] = datatype  # 数据类型
    basic_data['label_progress'] = '0%'  # 标注进度
    basic_data['remarks'] = remarks  # 备注

    # 创建数据集路径
    os.mkdir(database_root + str(basic_data['database_id']) + '-' + datatype + '-' + name)
    os.mkdir(database_root + str(basic_data['database_id']) + '-' + datatype + '-' + name + '/DataFiles')

    with open(database_root + str(basic_data['database_id']) + '-' + datatype + '-' + name + '/基本信息.json', 'w',
              encoding="utf-8") as f:
        json.dump(basic_data, f, ensure_ascii=False)

    print('CreateDatabase', '成功')
    return basic_data


# 数据集文件打包为zip，返回zip路径
def FilesDownload(database_id):
    """
    作用：数据集文件打包为zip，返回zip路径
    输入：database_id
    输出：zip路径
    """
    database = FindDatabase(database_id)
    files_path = database_root + database + '/DataFiles/'
    zipFolder = files_path
    zipfile_path = database_root + database + '/' + database
    shutil.make_archive(zipfile_path, 'zip', zipFolder)
    abspath = os.path.abspath(zipfile_path + '.zip')
    print('FilesDownload', '成功')
    return abspath

# print(FilesDownload(database_id = '100244'))


# 上传文件
def DataUpload(content, database_id, file_name):
    """
    作用：上传文件
    输入：content, database_id, file_name
    输出：
    """
    try:
        database_list = []
        database = ''
        for root, dirs, files in os.walk(database_root):
            database_list = dirs
            break
        for i in database_list:
            if database_id in i:
                database = i
                break
        file_path = database_root + database + '/DataFiles/all_data.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('')
        for d in content:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(d, ensure_ascii=False))
                f.write('\n')
        print('DataUpload', '成功')
        if len(content) == 0:
            return file_name + "文件上传失败，请检查数据是否符合格式。"
        return file_name + "文件上传成功"
    except:
        return file_name + "文件上传失败"


# 创建数据集文件下载路径
def DataExport(database_id):
    """
    作用：返回数据集下的Datafiles的所有文件
    输入：database_id
    输出：数据集下的Datafiles的所有文件列表
    """
    files_list = []
    database = ''
    for root, dirs, files in os.walk(database_root):
        database_list = dirs
        break
    for i in database_list:
        if database_id in i:
            database = i
            break
    files_path = database_root + database + '/DataFiles/'

    for root, dirs, files in os.walk(files_path):
        for i in range(len(files)):
            files[i] = files_path + files[i]
        files_list = files
    print('DataExport', '成功')
    return files_list


# 读取数据库下DataFiles的所有文件数据
def Browse(database_id):
    """
    作用：读取数据库下DataFiles的所有文件数据
    输入：database_id
    输出：数据库下DataFiles的所有文件数据
    """
    data_list = []
    data = ''
    files_list = DataExport(database_id)

    name = FindDatabase(database_id)
    for f_path in files_list:
        c = ''
        for f in open(f_path, 'r', encoding='utf-8'):
            c += f
        # print(c)
        data_list.append(changeJsonFormat(c))
    if len(data_list) == 0:
        return '数据为空'

    print('Browse', '成功')
    return data_list

# print(Browse(database_id = '1003172907'))
# print(Browse(database_id = '1003172859'))


# 搜索所有数据集
def SelectDatabase():
    """
    作用：搜索所有数据集
    输入：
    输出：数据集列表
    """
    for root, dirs, files in os.walk(database_root):
        database_list = dirs
        break
    print('SelectDatabase', '成功')
    return database_list


# 比较两端字符串的相似度
def similar_diff_qk_ratio(str1, str2):
    """
    作用：比较两端字符串的相似度
    输入：字符串1、字符串2
    输出：相似度数值
    """
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


# 保存前端标注的数据，每次保存一个段落（即一页）的数据
def DataSave(dataInput, database_id):
    """
    作用：保存前端标注的数据
    输入：前端传来的标注数据、数据集id
    输出：
    """
    files_list = DataPath(database_id)
    # 遍历数据集中的DataFiles,只有一个
    for f_path in files_list:
        # 清空原文件
        with open(f_path, 'w', encoding='utf-8') as f:
            f.write('')
        # 写入新内容
        for i in dataInput:
            with open(f_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(i, ensure_ascii=False))
                f.write('\n')
    print('DataSave', '成功')
    # # 读取段落数据的key（“id”）和value
    # for key, item in dataInput.items():
    #     # 遍历数据集中的DataFiles
    #     for f_path in files_list:
    #         data_list = []
    #         # # 遍历file里的data（按行读取）
    #         # for f in open(f_path, 'r', encoding='utf-8'):
    #         #     data_list.append(eval(f))
    #         # for i in data_list:
    #         #     data = i
    #             # for original_key, original_item in i.items():
    #             #     # 匹配输入数据的文本与数据集中的文本，匹配相似率大于0.95，则用新数据覆盖旧文本中的"nodes"和"rels"数据
    #             #     if item['oid'] == original_item['oid']:
    #             #         data_list.remove(i)
    #             #         data['id']['text'] = item['text']
    #             #         data['id']['nodes'] = item['nodes']
    #             #         data['id']['rels'] = item['rels']
    #             #         data_list = [data] + data_list
    #         # 清空原文件
    #         with open(f_path, 'w', encoding='utf-8') as f:
    #             f.write('')
    #         # 写入新内容
    #         for i in data_list:
    #             with open(f_path, 'a', encoding='utf-8') as f:
    #                 f.write(json.dumps(i, ensure_ascii=False))
    #                 f.write('\n')
    

# dataInput = [{'text': '中国沈阳飞机公司在歼-11BS战斗机基础上发展研制的四代半双座双发多用途战斗机。该机外形参考俄式苏-30MKK多用途战斗机。歼-16装备主动电子扫描相控阵雷达（AESA），可同时识别攻击多个目标，具备远距离超视距空战能力和强大的对地、对海打击能力。与歼轰-7比较歼-16的机体更大，最大载弹量12吨，可以发射霹雳-10、霹雳-15空对空导弹，鹰击-83、鹰击-91，空地-88等空对面导弹。该机装备中国产的涡扇-10“太行”发动机，其性能与美国最新的F-15EX多用途战斗机相当。', 'nodes': {'node1': {'label': ['飞行器'], '名称': '歼-11BS战斗机', '研发单位与产商': '中国沈阳飞 机公司'}, 'node2': {'label': ['战斗机'], '名称': 'F-15EX多用途战斗机', '研发单位与产商': '中国沈阳飞机公司'}}, 'rels': {'rel1': {'start': '中国沈阳飞机', 'end': '歼-11BS战斗机', 'rel_name': '生产研发'}}}, {'text': '歼-16是中国沈阳飞机公司在歼-11BS战斗机基础上发展研制的四代半双座双发多用途战斗机。该机外形参考俄式苏-30MKK多用途战斗机。歼-16装备主动电子扫描相控阵雷达（AESA），可同时识别攻击多个目标，具备远距离超视距空战能力和强大的对地、对海打击能力。与歼轰-7比较歼-16的机体更大，最大载弹量12吨，可以发射霹雳-10、霹雳-15空对空导弹，鹰击-83、鹰击-91，空地-88等空对面导弹。该机装备中国产的涡扇-10“太行”发动机，其性能与美国最新的F-15EX多用途战斗机相当。', 'nodes': {'node1': {'label': ['飞行器'], '名称': '歼-11BS战斗机', '研发单位与产商': '中国沈阳飞机公司'}, 'node2': {'label': ['生产制造厂商'], '名称': '中国沈阳飞机公司'}}, 'rels': {'rel1': {'start': '中国沈阳飞机', 'end': '歼-11BS战斗机', 'rel_name': '生产研发'}, 'rel2': {'start': '中国沈阳飞机', 'end': '歼-11BS战斗机', 'rel_name': '生产研发'}}}, {'text': '这里是文本段落', 'nodes': {}, 'rels': {}}]
# DataSave(dataInput, database_id='1003172859')


# 输出数据集中的实体与属性与关系
def NewItem(database_id):
    """
    作用：输出数据集中的实体与属性与关系
    输入：数据集id
    输出：实体、关系信息的列表
    """
    files_list = DataPath(database_id)
    new_item = []
    new_node = []
    new_rel = []
    # 遍历数据集中的DataFiles
    for f_path in files_list:
        for data in open(f_path, 'r', encoding='utf-8'):
            tmp = eval(data)
            print(tmp)
            if len(tmp['nodes']) != 0:
                for key, item in tmp['nodes'].items():
                    item['Choose'] = True
                    new_node.append(item)
            if len(tmp['rels']) != 0:
                for key, item in tmp['rels'].items():
                    item['Choose'] = True
                    new_rel.append(item) 
    new_item = [new_node, new_rel]
    if len(new_item) == 0:
        return '数据为空'
    print('NewItem', '成功')
    return new_item

# print(NewItem('1003172936'))


# # 输出数据集中的关系
# def NewRel(database_id):
#     """
#     作用：输出数据集中的关系
#     输入：数据集id
#     输出：实体间关系信息的列表
#     """
#     files_list = DataPath(database_id)
#     new_rel_list = []
#     # 遍历数据集中的DataFiles
#     for f_path in files_list:
#         for data in open(f_path, 'r', encoding='utf-8'):

#             for key, item in eval(data).items():
#                 new_rel_list.append(item['rels'])

#     print('NewRel', '成功')
#     return new_rel_list

# print(NewRel('1003172859'))


# 建立一个节点
def create_node(graph, label, attrs):
    """
    作用：建立一个节点
    输入：graph, label, attrs
    输出：
    """
    oid = ''
    n = "_.name=" + "\"" + attrs["name"] + "\""
    matcher = NodeMatcher(graph)
    # 查询是否已经存在，若存在则返回节点，否则返回None
    value = matcher.match(label).where(n).first()
    # 如果要创建的节点不存在则创建
    if value is None:
        # 生成随机10位原始ID
        oid = 'n' + str(random.randint(1000000000, 9999999999))
        attrs['oid'] = oid
        node = Node(*label, **attrs)
        n = graph.create(node)
        print('oid1',oid)
    print('oid2',oid)
    return value, oid


# 查询节点
def match_node(graph, label, attrs):
    """
    作用：查询节点
    输入：graph, label, attrs
    输出：
    """
    n = "_.name=" + "\"" + attrs["name"] + "\""
    matcher = NodeMatcher(graph)
    data = matcher.match(label).where(n).first()
    print(data)
    return data


# 建立两个节点之间的关系
def create_relationship(graph, label1, attrs1, label2, attrs2, r_name):
    """
    作用：建立两个节点之间的关系
    输入：graph, label1, attrs1, label2, attrs2, r_name
    输出：
    """
    value1 = match_node(graph, label1, attrs1)
    value2 = match_node(graph, label2, attrs2)
    if value1 is None or value2 is None:
        return False
    r = Relationship(value1, r_name, value2)
    graph.create(r)
    print('create_relationship', '成功')
    return True

# create_relationship(graph, ('生产研发单位',), {"name": "中国沈阳飞机公司"}, ('国家',), {'name': "德国"}, '属于')


# 将fusion数据保存到图谱中
def Fusion2Graph(node, nodes):
    """
    原理：1.匹配旧实体、2.修改名称、update属性
    作用：将fusion数据保存到图谱中
    输入：fusion的数据
    输出：
    """
    pairs = []
    for i in node:
        for num in range(len(nodes)):
            if i[0][1] == nodes[num]['名称']:
                for key in i[0][0]:
                    # 原实体，新的label，新属性，新name
                    pairs.append([key, i[0][0][key][2], nodes[num], i[1]])

    for i in range(len(pairs)):
        for label in pairs[i][1]:
            attrs2 = {}
            attrs2['name'] = pairs[i][2]['名称']
            node = match_node(graph, label, attrs2)  # 找到对应的结点
            if node != None:
                break
        if 'label' in pairs[i][2]:
            del [pairs[i][2]['label']]
        pairs[i][2]['name'] = pairs[i][3]
        pairs[i][2]['名称'] = pairs[i][3]
        node.update(pairs[i][2])  # 修改结点的属性
        graph.push(node)  # 更新结点
    all_data = []
    f = open(openkgdata_root, 'r', encoding='utf-8')
    for data in f:
        data = json.loads(data)
        all_data.append(data)

    with open(openkgdata_root, 'w', encoding='utf-8') as fw:
        fw.write('')
    print(sys.getsizeof(all_data))
    for data in all_data:
        for pair in pairs:
            if pair[0] == data['名称']:
                for key, item in pair[2].items():
                    data[key] = item
                data['label'] = pair[1]
                print('yes!!!')
        with open(openkgdata_root, 'a', encoding='utf-8') as fa:
            fa.write(json.dumps(data, ensure_ascii=False))
            fa.write('\n')

    return node, pairs

# data1 = [[[{'歼-11BS战斗机': ['94.74%', '歼-11BS战斗机', ['战斗机', '飞行器']]}, '歼-11BS战斗机'], '歼-11BS战斗机（测试）']]
# data1 = [[[{'歼-11BS战斗机（测试）': ['94.74%', '歼-11BS战斗机', ['战斗机', '飞行器']]}, '歼-11BS战斗机（测试）'], '歼-11BS战斗机']]
# data2 = [{'label': ['主战坦克', '坦克装甲车辆'], '名称': '歼-16', '产国': '中国', '研发单位与厂商': '中国', 'isChoose': 'true'},
#          {'label': ['主战坦克', '坦克装甲车辆'], '名称': 'J-16 multirole fighter', '产国': '中国', '研发单位与厂商': '中国', 'isChoose': 'true'},
#          {'label': ['主战坦克', '坦克装甲车辆'], '名称': '苏-', '产国': '中国', 'isChoose': 'true'},
#          {'label': ['飞行器'], '名称': '歼-11BS战斗机（测试）', '研发单位与产商': '中国沈阳飞机公司', 'isChoose': 'true'},
#          {'label': ['生产研发厂商'], '名称': '中国沈阳飞机公司', 'isChoose': 'true'},
#          {'label': ['生产研发厂商'], '名称': '前卫仪表厂', 'isChoose': 'true'}, {'label': ['国家'], '名称': '中国', 'isChoose': 'true'},
#          {'label': ['生产研发单位'], '名称': '中国沈阳飞机公司', 'isChoose': 'true'}]
# print(Fusion2Graph(data1, data2))


# 将json文件中的nodes创建到图谱中
def Nodes2Graph(dataInput):
    """
    作用：将json文件中的nodes创建到图谱中
    输入：nodes的数据
    输出：
    """
    data = {}
    data['_id'] = {}

    o_data = []
    f = open(openkgdata_root, 'r', encoding='utf-8')
    for d in f:
        d = json.loads(d)
        o_data.append(d['名称'])

    for key, item in dataInput['nodes'].items():
        # 生成随机10位原始ID
        if item['properties']['name'] not in o_data:
            ans, oid = create_node(graph, tuple(item['label']), item['properties'])
            if ans == None:
                data['_id']['oid'] = oid
                for key, item in item['properties'].items():
                    data[key] = item
                data['名称'] = data['name']
                with open(openkgdata_root, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(data, ensure_ascii=False))
                    f.write('\n')
                print('nodes创建成功')
                print('Nodes2Graph', '成功')

    return 'nodes创建成功'


# 将json文件中的rels创建到图谱中
def Rels2Graph(dataInput):
    """
    作用：将json文件中的rels创建到图谱中
    输入：rels的数据
    输出：
    """
    ans = True
    for key, item in dataInput['rels'].items():
        # 生成随机10位原始ID
        item['oid'] = 'r' + str(random.randint(1000000000, 9999999999))
        ans = create_relationship(graph, tuple(item['start']['label']), {'name': item['start']['name']},
                                  tuple(item['end']['label']), {'name': item['end']['name']}, item['rel_name'])
    if ans == True:
        print('关系数据保存成功')
        print('Rels2Graph', '成功')
        return {'msg': '关系数据保存成功'}
    else:
        print('关系数据保存失败')
        return {'msg': '关系数据保存失败'}


# 将query进行处理，进行neo4j查询
def Query(query):
    """
    作用：将query进行处理，进行neo4j查询
    输入：问答的query
    输出：neo4j查询后返回的答案
    """
    query = query.replace('生产研发于', '产国').split()
    with driver.session() as session:

        # 返回query1的答案
        if len(query) == 2:
            try:
                q = session.run("""MATCH (a {name:\"""" + query[0] + """\"}) RETURN a.""" + query[1])
                result = ''
                for i, r in enumerate(q):
                    for j, k in enumerate(r):
                        result+= k +'，'
                if len(result) == 0:
                    return ['Oops，我也不知道。。。']
                return result[:-1]
            except:
                return ['Oops，我也不知道。。。']

        # 返回query2的答案
        elif len(query) == 4:
            try:
                q = session.run("""MATCH (a {name:\"""" + query[0] + """\"})-[r:`生产研发`]->(b) RETURN b.name""")
                result = ''
                for i, r in enumerate(q):
                    for j, k in enumerate(r):
                        result+= k +'，'
                if len(result) == 0:
                    return ['Oops，我也不知道。。。']
                return result[:-1]
            except:
                return 'Oops，我也不知道。。。'

        # 返回query3、4的答案
        elif len(query) == 3:
            try:
                q = session.run(
                    """MATCH (a)-[r:`""" + query[1] + """`]->(b {name:\"""" + query[
                        2] + """\"}) RETURN a.name LIMIT 5""")
                result = ''
                for i, r in enumerate(q):
                    for j, k in enumerate(r):
                        result+= k +'，'
                if len(result) == 0:
                    return ['Oops，我也不知道。。。']
                return result[:-1]
            except:
                return 'Oops，我也不知道。。。'

        else:
            return "请按照标准格式提问，名称也要写完整哦。"

# print(Query('中国沈阳飞机公司 生产研发 了 什么武器'))


# 匹配搜索目标和数据库，进行名称相似度比对，输出相似度实体最高的所有信息
def DetailSearch(node_name):
    """
    作用：匹配搜索目标和数据库，进行名称相似度比对，输出相似度实体最高的所有信息
    输入：搜索目标名称
    输出：数据库中匹配到的实体的所有信息与对应图片的路径
    """
    possible_node = {}
    tmp = 0
    for data in open(openkgdata_root, encoding='utf-8'):
        data_json = json.loads(data)
        similar_ratio = string_similar(node_name, data_json['名称'])
        if similar_ratio >= 0.5 and similar_ratio > tmp:
            tmp = similar_ratio
            # 替换名称的符号是因为在爬取图片时因为路径问题所以将名称中的‘/’全部替换为‘-’，所以这里也做相应的改动
            # data_json['pic_path'] = '@/assets/pic/' + data_json['名称'].replace('/', '-') + '.jpg'
            data_json['pic_path'] = data_json['名称'].replace('/', '-') + '.jpg'
            possible_node = data_json
    if len(possible_node) == 0:
        print('DetailSearch', '成功')
        return '该词条暂未收录'
    else:
        print('DetailSearch', '成功')
        return possible_node

# print(DetailSearch(node_name = '苏-27战斗机'))
# print(DetailSearch(node_name = '苏-27战斗'))


# 比较新实体与原数据库中的实体相似性，并返回相似性大于0.7且排名前三的实体列表
def EntityFusion(database_id):
    """
    作用：比较新实体与原数据库中的实体相似性，并返回相似性大于0.7且排名前三的实体列表
    输入：数据集id
    输出：实体列表
    """
    original_name = []
    for data in open(openkgdata_root, encoding='utf-8'):
        data_json = json.loads(data)
        original_name.append(data_json['名称'])

    new_name = []
    for data in NewNode(database_id):
        for key, item in data.items():
            new_name.append(item['名称'])

    entity_list = []
    for i in new_name:
        entity = {}
        similar_entity = []
        for j in original_name:
            similarity = similar_diff_qk_ratio(i, j)
            if similarity > 0.7:
                similar_entity.append([j, similar_diff_qk_ratio(i, j)])
        similar_entity.sort(key=lambda x: x[1], reverse=True)
        entity[i] = similar_entity[0:3]
        entity_list.append(entity)
    print('EntityFusion', '成功')
    return entity_list



headers = {
    # 用户代理
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    # 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
    'User-Agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"'
}

USER_AGENT_LIST = [
    'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
    'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
    'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
    'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
    'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
    'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
    'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
    'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
]

# s = requests.session()
# s.keep_alive = False
# home_page = 'http://military.china.com.cn/'

def download(url, user_agent='wswp', num_retries=2):
    print('downloading: %', url)
    # 防止对方禁用Python的代理，导致forbidden错误
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.error.URLError as e:
        print('download error:', e.reason)
        html = None
        if num_retries > 0:
            # URLError是一个上层的类，因此HttpERROR是可以被捕获到的。code是HttpError里面的一个字段
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries - 1)
    return html

# 获得页面内容


def get_content(page_url):
    html_result = download(page_url)

    if html_result is None:
        print('is None')
        exit(1)
    else:
        pass

    # 分析得到的结果，从中找到需要访问的内容
    soup = BeautifulSoup(html_result, 'html.parser')
    return soup

# 获取新闻头条

def GetNews():
    allNews = []

    # 中国军事网
    second_html = get_content('http://military.china.com.cn/')
    pairs = []
    num_list = second_html.find('div', attrs={'class': "layout_news"})
    num_list = num_list.find_all('div', attrs={'class': "plist1"})

    for i in num_list[:10]:
        pairs.append([i.find('a').text, i.find('a')['href']])
    # print(pairs)
    allNews.append(pairs)

    # 中国军网
    second_html = get_content('http://www.81.cn/bq_208581/index.html')
    pairs = []
    num_list = second_html.find('ul', attrs={'id': "main-news-list"})
    
    num_list = num_list.find_all('li')
    for i in num_list[:10]:
        pairs.append([i.find('img')['alt'],i.find('a')['href']])
    # print(pairs)
    allNews.append(pairs)

    # 央广军事网
    second_html = get_content('https://military.cnr.cn/zdgz/')
    pairs = []
    num_list = second_html.find('div', attrs={'class': "articleList"})
    num_list = num_list.find_all('div', attrs={'class': 'item url_http'})
    for i in num_list:
        pairs.append([i.find('strong').text,i.find('a')['href']])
    print(pairs)
    allNews.append(pairs)

    return allNews
# print(GetNews())


# 环球网
# HQurl = 'https://mil.huanqiu.com/article/4C68oDmLz1H'
def GetHQNews(url):
    second_html = get_content(url)
    pairs = []
    num_list = second_html.find('article')
    num_list = num_list.find_all('p')

    for i in num_list:
        c = i.text.replace('\xa0', ' ')
        if c != '':
            pairs.append(c)
    return pairs
   
# GetHQNews('https://mil.huanqiu.com/article/4C7gdudPDdI')
# GetHQNews('https://mil.huanqiu.com/article/4C7g93f4deM')

# 参考消息
# CKXXurl = 'http://www.cankaoxiaoxi.com/mil/20230228/2505825.shtml'
def GetCKXXNews(url):
   
    second_html = get_content(url)
    pairs = []
    num_list = second_html.find('div', attrs={'class': "articleContent"})
    num_list = num_list.find_all('p')

    for i in num_list:
        c = i.text.replace('\xa0', ' ')
        if c != '':
            pairs.append(c)
    return pairs
# GetCKXXNews(CKXXurl)  


# 新华网
# XHurl = 'http://www.news.cn/mil/2023-03/16/c_1211738298.htm'
def GetXHNews(url):
   
    second_html = get_content(url)
    pairs = []
    num_list = second_html.find('div', attrs={'id': "detail"})
    num_list = num_list.find_all('p')

    for i in num_list:
        c = i.text.replace('\xa0', ' ')
        if c != '':
            pairs.append(c)
    # print(pairs)
    return pairs
# GetXHNews(XHurl) 



# 新闻爬虫
def NewsCrawl(newsList):
    NewsClips=[]
    fileName = newsClips_root + r'NewsClips.json'
    for i in newsList:
        if 'cankaoxiaoxi' in i :
            NewsClips+=GetCKXXNews(i)
        if 'huanqiu' in i :
            NewsClips+=GetHQNews(i)
        if 'www.news.cn' in i :
            NewsClips+=GetXHNews(i)
    with open(fileName, 'w') as f:
        f.write('')

    for i in NewsClips:
        dic = {}
        dic['text'] = i
        dic['nodes'] = {}
        dic['rels'] = []
        with open(fileName, 'a') as f:
            f.write(json.dumps(dic, ensure_ascii=False))
            f.write('\n')
    return fileName
       

# print(NewsCrawl(newsList))
# NewsClips = NewsCrawl(newsList)
# NewsClipsPath = '../../data/NewsClips.json'


