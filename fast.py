from pydoc import describe
from turtle import pen
from fastapi import FastAPI, File, UploadFile
from typing import List, Optional
from fastapi.responses import HTMLResponse, FileResponse
from starlette.routing import Host
import uvicorn
import random
import re, os, time, json
from uvicorn import config
from pydantic import BaseModel
from utils import *
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append("..")
# from relation_k.predict_per_para import AutoGenerate

root = os.path.abspath(os.path.dirname(__file__))
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"], )


# 主页
@app.get("/")
async def read_main():
    return {"msg": "欢迎来到军事装备知识图谱项目"}


# 数据上传：自动生成实体、关系
@app.get("/AutoGenerate", description='数据上传：自动生成实体、关系')
async def auto_generate(database_id: str):
    # name = FindDatabase(database_id)
    # texts = ReadDatabaseText(database_id)
    
    # AutoGenerate()
    # result_path = root + '/relation_k/output/result.json'
    # with open(result_path, 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    #     all_data_path = root + '/data/database/' + name + '/DataFiles/all_data.json'
    #     with open(all_data_path, 'w', encoding='utf-8') as ff:
    #         ff.write('')
    #     for i in range(len(texts)):
    #         a = {}
    #         a['id'] = {}
    #         a['id']['oid'] = str(random.randint(1000000000, 9999999999))
    #         a['id']['text'] = texts[i]
    #         a['id']['nodes'] = {}
    #         a['id']['nodes'] = data[str(i)]['nodes']
    #         for key, item in a['id']['nodes'].items():
    #             for ikey, iitem in item.items():
    #                 if ikey != 'label' and type(iitem) == list:
    #                     a['id']['nodes'][key][ikey] = iitem[0]

    #         a['id']['rels'] = {}
    #         a['id']['rels'] = data[str(i)]['rels']
    #         for key, item in a['id']['rels'].items():
    #             for ikey, iitem in item.items():
    #                 if type(iitem) == list:
    #                     a['id']['rels'][key][ikey] = iitem[0]
            
    #         with open(all_data_path, 'a', encoding='utf-8') as ff:
    #             ff.write(json.dumps(a, ensure_ascii=False))
    #             ff.write('\n')

    #         print(a)
    #         print(all_data_path, '输出成功')
      
    return {"msg": "自动抽取成功"}


# 数据上传：初始页面加载，返回以及渲染数据集列表及其基本信息
@app.get("/DatabaseList", description='数据上传：初始页面加载，返回以及渲染数据集列表及其基本信息')
async def database_list():
    database_info_list = DatabaseList()
    return database_info_list


# 数据融合：进行新标注的实体与Neo4j中的实体相似度比较
@app.post("/FindSimilarNode", description='数据融合：进行新标注的实体与Neo4j中的实体相似度比较')
async def find_similar_node(new_nodes: str):
    new_nodes = eval(new_nodes)
    data = {}
    for i in range(len(new_nodes)):
        data[str(i)] = {}
        data[str(i)]['nodes'] = {}
        data[str(i)]['nodes']['node1'] = new_nodes[i]

    ans = FindSimilarNode(data)
    print(ans)
    return ans

# 数据上传：“创建数据集”按钮触发
@app.get("/CreateDatabase", description='# 数据上传：“创建数据集”按钮触发')
async def create_database(name: str, remarks: str, datatype: str):
    CreateDatabase(name, remarks, datatype)
    data = {"msg": "数据集创建成功"}
    return data


# 数据上传：“删除”按钮触发，删除数据集
@app.get("/DeleteDatabase", description='数据上传：“删除”按钮触发，删除数据集')
async def delete_database(database_id: str):
    DeleteDatabase(database_id)
    database_info_list = DatabaseList()
    return database_info_list


# 数据标注：展示数据集的数据（包含文本、nodes、relationships）
@app.get("/Browse", description='数据标注：展示数据集的数据（包含文本、nodes、relationships）')
async def browse(database_id: str):
    data = Browse(database_id)
    print(data)
    return data


# 数据上传：“导入”操作触发，导入文本数据
@app.post("/UploadFiles/{database_id}", description='“导入”操作触发，导入文本数据')
async def create_upload_files(database_id: str, files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()
        contents = str(contents, 'utf-8')
        print(contents)
        contents = contents.replace('\n', '').replace(' ', '').split('}{')
        try:
            
            for i in range(len(contents)):
                if i == 0:
                    contents[0] = contents[0] + '}'
                elif i>= 1 and i<len(contents)-1:
                    contents[i] = '{'+ contents[i] + '}'
                else:
                    contents[-1] = '{'+ contents[-1]

                contents[i] = json.loads(contents[i]) 

            for i in range(len(contents)):
                print(i)
                print(type(i))
                if 'text' not in contents[i] and 'nodes' not in contents[i] and 'rels' not in contents[i]:
                    return {"msg": '数据格式错误'}
            print(contents)
            ans = DataUpload(contents, database_id, file.filename)
        except:
            return {"msg": '数据上传错误'}
    return {"msg": ans}


# 数据上传：“导出”操作触发，导出数据集压缩包
@app.get("/DataExport", description='数据上传：“导出”操作触发，导出数据集压缩包')
async def data_export(database_id: str):
    zipfile_path = FilesDownload(database_id)
    return zipfile_path


# 数据标注：“保存”按钮触发，保存修改和标注后的单条文本以及其nodes和relations
@app.get("/DataSave", description='数据标注：“保存”按钮触发，保存修改和标注后的单条文本以及其nodes和relations')
async def data_save(dataInput: str, database_id: str):
    # dataInput = dataInput.encode('utf-8').decode('utf-8')
    
    dataInput = eval(dataInput)
    print(dataInput[0])
    print(type(dataInput[0]))
    print('保存的data:', dataInput)
    DataSave(dataInput[0], database_id)
    # # dataInput[2] = eval(dataInput[2])
    # print(dataInput)

    # data = {}
    # data["id"] = {}
    # dataInput[0] = dataInput[0].split('\n')
    # data["id"]["oid"] = dataInput[0][0]
    # data["id"]["text"] = dataInput[0][1]
    # data["id"]["nodes"] = {}
    # count_node = 1
    # for key, item in dataInput[2].items():
    #     data["id"]["nodes"]['node' + str(count_node)] = {}
    #     data["id"]["nodes"]['node' + str(count_node)]['label'] = [re.findall("【(.+?)】", key)[0]]
    #     data["id"]["nodes"]['node' + str(count_node)]['名称'] = key.split('【')[0]
    #     data["id"]["nodes"]['node' + str(count_node)].update(item)
    #     count_node += 1

    # data["id"]["rels"] = {}
    # count_rel = 1
    # for i in dataInput[1]:
    #     if i[2] == '':
    #         continue
    #     print('这里是i：', i)
    #     print('这里是i：', type(i))
    #     if type(i) != 'str':
    #         print(type(i))

    #         rel = i[1].split('\n')
    #         print(rel)
    #         data["id"]["rels"]['rel' + str(count_rel)] = {}
    #         data["id"]["rels"]['rel' + str(count_rel)]['start'] = rel[0]
    #         data["id"]["rels"]['rel' + str(count_rel)]['end'] = rel[1]
    #         data["id"]["rels"]['rel' + str(count_rel)]['rel_name'] = i[2]
    #         count_rel += 1

    
    return {"msg": "数据保存成功"}


# 数据融合：“实体融合”的“确认融合”按钮触发，将实体融合到neo4j中
@app.post("/Fusion2Graph", description='数据融合：“实体融合”的“确认融合”按钮触发，将实体融合到neo4j中')
async def fusion2graph(dataInput_fusion: str, nodes: str):
    data = eval(dataInput_fusion)
    nodes = eval(nodes)
    node, pairs = Fusion2Graph(data, nodes)
    print(node, pairs)
    return {"msg": 'Fusion2Graph成功'}


# 数据融合：“生成新的实体与属性”的“确认融合”按钮触发，将新标注出的nodes保存到neo4j中
@app.post("/Nodes2Graph", description='数据融合：“生成新的实体与属性”的“确认融合”按钮触发，将新标注出的nodes保存到neo4j中')
async def nodes2graph(dataInput_node: str):
    data = eval(dataInput_node)
    nodes = {}
    nodes['nodes'] = {}
    for i in range(len(data)):
        del data[i]['isChoose']
        nodes['nodes']['node' + str(i)] = {}
        nodes['nodes']['node' + str(i)]['label'] = data[i]['label']
        nodes['nodes']['node' + str(i)]['properties'] = data[i]
        nodes['nodes']['node' + str(i)]['properties']['name'] = data[i]['名称']

    res = Nodes2Graph(nodes)
    return {"msg": res}


# 数据融合：“生成新的关系”的“确认融合”按钮触发，将新标注出的relationships保存到neo4j中
@app.post("/Rels2Graph", description='数据融合：“生成新的关系”的“确认融合”按钮触发，将新标注出的relationships保存到neo4j中')
async def rels2graph(dataInput_rel: str):
    dataInput_rel = eval(dataInput_rel)
    print(dataInput_rel)
    data = {}
    data['rels'] = {}
    for i in range(len(dataInput_rel)):
        if len(dataInput_rel[i]['start']) or len(dataInput_rel[i]['end']) == 1:
            continue
        data['rels']['rel' + str(i + 1)] = {}
        data['rels']['rel' + str(i + 1)]['start'] = {}
        data['rels']['rel' + str(i + 1)]['start']['label'] = dataInput_rel[i]['start'][1]
        data['rels']['rel' + str(i + 1)]['start']['name'] = dataInput_rel[i]['start'][0]

        data['rels']['rel' + str(i + 1)]['end'] = {}
        data['rels']['rel' + str(i + 1)]['end']['label'] = dataInput_rel[i]['end'][1]
        data['rels']['rel' + str(i + 1)]['end']['name'] = dataInput_rel[i]['end'][0]

        data['rels']['rel' + str(i + 1)]['rel_name'] = dataInput_rel[i]['rel_name']

    res = Rels2Graph(data)
    return res


# 知识问答：“发送”按钮触发，将Query传到后台生成答案
@app.get("/Query", description='')
async def query(question: str):
    ans = Query(question)
    return ans


# 词条检索：点击“放大镜”触发
@app.get("/DetailSearch", description='')
async def detail_search(aim: str):
    ans = DetailSearch(aim)
    return ans


# 数据融合：展示新标注的实体
@app.get("/NewItem", description='')
async def new_item(database_id: str):
    data = NewItem(database_id)
    return data


# # 数据融合：展示新标注的关系
# @app.get("/NewRel", description='')
# async def new_rel(database_id: str):
#     data = NewRel(database_id)
#     return data

# 数据融合：展示新标注的关系
@app.get("/GetNews", description='')
async def new_rel():
    data = GetNews()
    return data

# 数据处理：爬虫新闻片段
@app.get("/NewsCrawl", description='')
async def news_crawl(newsList: str):
    newsList = newsList.split(',')
    filePath = NewsCrawl(newsList)
    return filePath

if __name__ == '__main__':

    uvicorn.run(app='fast:app', host="0.0.0.0", port=8000, reload=True)
