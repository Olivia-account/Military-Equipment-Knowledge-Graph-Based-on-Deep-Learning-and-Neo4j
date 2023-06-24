import csv
import json
#import re
import math
from jieba import posseg
import jieba.analyse
import os
import codecs
import logging
import optparse
import dedupe
# from text2vec import Similarity
# 对要进行比较的str1和str2进行计算，并返回相似度


def simicos(str1, str2):
    # 对两个要计算的字符串进行分词, 使用隐马尔科夫模型(也可不用)
    # 由于不同的分词算法, 所以分出来的结果可能不一样
    # 也会导致相似度会有所误差, 但是一般影响不大
    # 如果想把所有的词性都计算，那么把if及其后面的全部删除掉即可
    # print('=======================================')
    # print(str1,str2)
    cut_str1 = [w for w, t in posseg.lcut(str1) ]#if 'n' in t or 'v' in t
    cut_str2 = [w for w, t in posseg.lcut(str2[0]) ]#if 'n' in t or 'v' in t

    # 列出所有词
    all_words = set(cut_str1 + cut_str2)
    # 计算词频
    freq_str1 = [cut_str1.count(x) for x in all_words]
    freq_str2 = [cut_str2.count(x) for x in all_words]
    # 计算相似度
    sum_all = sum(map(lambda z, y: z * y, freq_str1, freq_str2))
    sqrt_str1 = math.sqrt(sum(x ** 2 for x in freq_str1))
    sqrt_str2 = math.sqrt(sum(x ** 2 for x in freq_str2))
    return sum_all / (sqrt_str1 * sqrt_str2+0.0001)


def simicos_con(str1, str2):
    cut_str1 = [w for w in str1 ]#if 'n' in t or 'v' in t
    cut_str2 = [w for w in str2 ]#if 'n' in t or 'v' in t

    # 列出所有词
    all_words = set(cut_str1 + cut_str2)
    # 计算词频
    freq_str1 = [cut_str1.count(x) for x in all_words]
    freq_str2 = [cut_str2.count(x) for x in all_words]
    # 计算相似度
    sum_all = sum(map(lambda z, y: z * y, freq_str1, freq_str2))
    sqrt_str1 = math.sqrt(sum(x ** 2 for x in freq_str1))
    sqrt_str2 = math.sqrt(sum(x ** 2 for x in freq_str2))
    return sum_all / (sqrt_str1 * sqrt_str2)


# def vote_value(spo_list,pred):
#     list_key = []
#     pred_frequecy = dict()
#     for spo in spo_list:
#         if spo[1] == pred:
#             if spo[0] not in pred_frequecy:
#                 pred_frequecy[spo[0]] = 1
#             else:
#                 pred_frequecy[spo[0]] = pred_frequecy[spo[0]]+1
#     for i in range(len(list(pred_frequecy.keys()))):
#         if list(pred_frequecy.values())[i] == max(list(pred_frequecy.values())):
#             list_key.append(list(pred_frequecy.keys())[i])
#     if len(list_key)==1:
#         return list_key
#     else:
#         new_list=[]
#         scores=[]
#         for v in list_key:
#             for w in list_key:
#                 if v!=w: # 对于不相同的值
#                     scores.append([simicos(v,w),v,w])
#         for s in scores:
#             if s[0]>=0.5:
#                 if s[1] in new_list or s[2] in new_list:
#                     continue
#                 print("left one of them:",s[1],s[2])
#                 new_list.append(s[1] if len(s[1])>=len(s[2]) else s[2])
#             elif s[0]<0.5:
#                 print("keep both of them")
#                 new_list.append(s[1])
#                 new_list.append(s[2])
#         #         elif simicos(v,w) < 0.3:
#         #             print(v,'!=====',w)
#         #             new_list.append(v)
#         #             new_list.append(w)
#         new_list = list(set(new_list))
#     return new_list

def vote_value(cluster,key):
    type_count={}
    #key=3
    for item in cluster:
        if item[key] not in type_count:
            type_count[item[key]]=1
        else:
            type_count[item[key]]=type_count[item[key]]+1

    return max(type_count, key=type_count.get)




def getKey(dic,value):
    if value not in dic.values():
        return None
    result=set()
    for key in dic:
        if dic[key] == value:
            result.add(key)
    return result


reg = r'<p>(.*?)</p>'


def readData(filename):
    """
    Remap columns for the following cases:
    - Lat and Long are mapped into a single LatLong tuple
    - Class and Coauthor are stored as delimited strings but mapped into
      tuples
    """
    data_d = {}
    with open(filename, 'r',encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            row = dict((k, v.lower()) for k, v in row.items())
            data_d[idx] = row
    return data_d


def find_key(key_dict,key):
    key_dict[key]=-1
    k=max(key_dict, key=key_dict.get)
    return k


def find_name(subject_name):
    if len(subject_name)==0:
        return None
    else:
        return max(subject_name, key=subject_name.get)


# These generators will give us the corpora setting up the Set
# distance metrics
def names(data):
    for record in data.values():
        yield record['subject']


def types(data):
    for record in data.values():
        yield record['type']


def cluster(input_file,output_file):
    # ## Logging
    # Dedupe uses Python logging to show or suppress verbose output. Added
    # for convenience.  To enable verbose logging, run `python
    # patent_example.py -v`

    optp = optparse.OptionParser()
    optp.add_option('-v', '--verbose', dest='verbose', action='count',
                    help='Increase verbosity (specify multiple times for more)'
                    )
    (opts, args) = optp.parse_args()
    log_level = logging.WARNING

    if opts.verbose:
        if opts.verbose == 1:
            log_level = logging.INFO
        elif opts.verbose > 1:
            log_level = logging.DEBUG
    logging.getLogger().setLevel(log_level)

    settings_file = 'F:/graduate_design/code/knowledge_label/resource_all_settings.json'
    training_file = 'F:/graduate_design/code/knowledge_label/resource_all_training.json'
    print('importing data ...')
    input_file='F:/graduate_design/code/knowledge_label/'+input_file
    output_file='F:/graduate_design/code/knowledge_label/'+output_file
    data_d = readData(input_file)

    if os.path.exists(settings_file):
        print('reading from', settings_file)
        with open(settings_file, 'rb') as sf:
            deduper = dedupe.StaticDedupe(sf, num_cores=0)
    else:
        # Define the fields dedupe will pay attention to
        '''
            {'field': 'type',
             'variable name': 'type',
             'type': 'Text',
             'corpus': types(data_d),
             'has missing': False},
        '''
        fields = [
            {'field': 'subject',
             'variable name': 'name Text',
             'type': 'Text',
             # 'corpus': names(data_d),
             'has missing': False},
            {'field': 'predicate',
             'variable name': 'name Text',
             'type': 'Text',
             # 'corpus': names(data_d),
             'has missing': False},
            {'field': 'object',
             'variable name': 'name Text',
             'type': 'Text',
             # 'corpus': names(data_d),
             'has missing': False},
        ]

        # Create a new deduper object and pass our data model to it.
        deduper = dedupe.Dedupe(fields, num_cores=2)
        # If we have training data saved from a previous run of dedupe,
        # look for it an load it in.
        if os.path.exists(training_file):
            print('reading labeled examples from ', training_file)
            with open(training_file) as tf:
                deduper.prepare_training(data_d, training_file=tf)
        else:
            deduper.prepare_training(data_d)
        # ## Active learning

        # Starts the training loop. Dedupe will find the next pair of records
        # it is least certain about and ask you to label them as duplicates
        # or not.

        # use 'y', 'n' and 'u' keys to flag duplicates
        # press 'f' when you are finished
        print('starting active labeling...')
        dedupe.console_label(deduper)

        deduper.train()

        # When finished, save our training away to disk
        with open(training_file, 'w') as tf:
            deduper.write_training(tf)

        # Save our weights and predicates to disk.  If the settings file
        # exists, we will skip all the training and learning next time we run
        # this file.
        with open(settings_file, 'wb') as sf:
            deduper.write_settings(sf)
    clustered_dupes = deduper.partition(data_d, 0.5)
    import time
    time.sleep(20)
    print('# duplicate sets', len(clustered_dupes))

    # ## Writing Results

    # Write our original data back out to a CSV with a new column called
    # 'Cluster ID' which indicates which records refer to each other.

    cluster_membership = {}
    for cluster_id, (records, scores) in enumerate(clustered_dupes):
        for record_id, score in zip(records, scores):
            cluster_membership[record_id] = {
                "Cluster ID": cluster_id,
                "confidence_score": score
            }

    with open(output_file, 'w',encoding='utf-8',newline='') as f_output, open(input_file,encoding='utf-8') as f_input:
        reader = csv.DictReader(f_input)
        fieldnames = ['Cluster ID', 'confidence_score'] + reader.fieldnames
        writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        writer.writeheader()

        for row_id, row in enumerate(reader):
            row.update(cluster_membership[row_id])
            writer.writerow(row)


if __name__ == '__main__':
    input_path = 'F:/graduate_design/code/relation_k/datam/duie.json'
    final_path = "F:/graduate_design/code/knowledge_label/output/result.json"
    f = open(input_path, 'r', encoding='utf-8')
    # with open("spo_in_para.csv", 'w', encoding='utf-8', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(["index", "subject", "predicate", "object", "label"])
    para_dict = {}  # 段落映射：段落id->段落内容，段落的句子集合
    for data in f:
        data=data.replace('} {','}SPLIT{')
    f=data.split('SPLIT')
    
    for data in f:

        data = json.loads(data)
        if str(data['id']) not in para_dict:
            para_dict[str(data['id'])]= {
                "content": '',
                "sentences": []
            }
        para_dict[str(data['id'])]["content"] = para_dict[str(data['id'])]["content"]+data['text']
        para_dict[str(data['id'])]["sentences"].append(data)

    ALL_DATA = {}  # 包含所有数据的字典
    for pa_id, info in para_dict.items():   # 给每个段落在ALL_DATA中创建一个集合
        ALL_DATA[pa_id] = {
            "nodes_zone": [],               # 原始的三元组集合
            "nodes": {},                    # 段落中的实体集合
            "rels": {},                     # 段落中的关系集合
            "sentences": info["sentences"]  # 段落的句子集合
        }

    # ############################预定义集合########################### #
    # 小类
    classes = ['战斗机', '攻击机', '轰炸机', '教练机', '预警机', '侦察机', '反潜机', '电子战机', '无人机', '运输机', '飞艇', '试验机', '加油机', '通用飞机', '干线',
             '支线', '运输直升机', '武装直升机', '多用途直升机', '航空母舰', '战列舰', '巡洋舰', '驱逐舰', '护卫舰', '两栖作战舰艇', '核潜艇', '常规潜艇', '水雷战舰艇',
             '导弹艇', '巡逻舰/艇', '保障辅助舰艇', '气垫艇/气垫船', '其他', '非自动步枪', '自动步枪', '冲锋枪', '狙击枪', '手枪', '机枪', '霰弹枪', '火箭筒',
             '榴弹发射器', '附件', '刀具', '迷彩服', '步兵战车', '主战坦克', '特种坦克', '装甲运兵车', '装甲侦察车', '装甲指挥车', '救护车', '工程抢修车', '布/扫雷车',
             '越野车', '其他特种装甲车辆', '榴弹炮', '加农炮', '加农榴弹炮', '迫击炮', '火箭炮', '高射炮', '坦克炮', '反坦克炮', '无后坐炮', '装甲车载炮', '舰炮', '航空炮',
             '自行火炮', '弹炮结合系统', '反弹道导弹', '地地导弹', '舰地（潜地）导弹', '地空导弹', '舰空导弹', '空空导弹', '空地导弹', '潜舰导弹', '空舰导弹', '岸舰导弹',
             '舰舰导弹', '航天机构', '运载火箭', '航天基地', '技术试验卫星', '军事卫星', '科学卫星', '应用卫星', '空间探测器', '航天飞机', '宇宙飞船', '地雷', '水雷',
             '手榴弹', '炸弹', '鱼雷', '火箭弹', '原子弹', '氢弹', '中子弹']
    # 大类
    big = ['飞行器', '舰船舰艇', '枪械与单兵', '坦克装甲车辆', '火炮', '导弹武器', '太空装备', '爆炸物']
    # 小类到大类的映射
    small2big = {
        "战斗机":'飞行器', "攻击机":'飞行器', "轰炸机":'飞行器', "教练机":'飞行器', "预警机":'飞行器', "侦察机":'飞行器', "反潜机":'飞行器', "电子战机":'飞行器', "无人机":'飞行器', "运输机":'飞行器', "飞艇":'飞行器', "试验机":'飞行器', "加油机":'飞行器', "通用飞机":'飞行器', "干线":'飞行器',
        "支线":'飞行器', "运输直升机":'飞行器', "武装直升机":'飞行器', "多用途直升机":'飞行器', "航空母舰":'舰船舰艇', "战列舰":'舰船舰艇', "巡洋舰":'舰船舰艇', "驱逐舰":'舰船舰艇', "护卫舰":'舰船舰艇', "两栖作战舰艇":'舰船舰艇', "核潜艇":'舰船舰艇', "常规潜艇":'舰船舰艇', "水雷战舰艇":'舰船舰艇',
        "导弹艇":'舰船舰艇', "巡逻舰/艇":'舰船舰艇', "保障辅助舰艇":'舰船舰艇', "气垫艇/气垫船":'舰船舰艇', "其他":"其他", "非自动步枪":'枪械与单兵', "自动步枪":'枪械与单兵', "冲锋枪":'枪械与单兵', "狙击枪":'枪械与单兵', "手枪":'枪械与单兵', "机枪":'枪械与单兵', "霰弹枪":'枪械与单兵', "火箭筒":'枪械与单兵',
        "榴弹发射器":'枪械与单兵', "附件":'枪械与单兵', "刀具":'枪械与单兵', "迷彩服":'枪械与单兵', "步兵战车":'坦克装甲车辆', "主战坦克":'坦克装甲车辆', "特种坦克":'坦克装甲车辆', "装甲运兵车":'坦克装甲车辆', "装甲侦察车":'坦克装甲车辆', "装甲指挥车":'坦克装甲车辆', "救护车":'坦克装甲车辆', "工程抢修车":'坦克装甲车辆', "布/扫雷车":'坦克装甲车辆',
        "越野车":'坦克装甲车辆', "其他特种装甲车辆":'坦克装甲车辆', "榴弹炮":'火炮', "加农炮":'火炮', "加农榴弹炮":'火炮', "迫击炮":'火炮', "火箭炮":'火炮', "高射炮":'火炮', "坦克炮":'火炮', "反坦克炮":'火炮', "无后坐炮":'火炮', "装甲车载炮":'火炮', "舰炮":'火炮', "航空炮":'火炮',
        "自行火炮":'火炮', "弹炮结合系统":'导弹武器', "反弹道导弹":'导弹武器', "地地导弹":'导弹武器', "舰地（潜地）导弹":'导弹武器', "地空导弹":'导弹武器', "舰空导弹":'导弹武器', "空空导弹":'导弹武器', "空地导弹":'导弹武器', "潜舰导弹":'导弹武器', "空舰导弹":'导弹武器', "岸舰导弹":'导弹武器',
        "舰舰导弹":'导弹武器', "航天机构":'太空装备', "运载火箭":'太空装备', "航天基地":'太空装备', "技术试验卫星":'太空装备', "军事卫星":'太空装备', "科学卫星":'太空装备', "应用卫星":'太空装备', "空间探测器":'太空装备', "航天飞机":'太空装备', "宇宙飞船":'太空装备', "地雷":'爆炸物', "水雷":'爆炸物',
        "手榴弹":'爆炸物', "炸弹":'爆炸物', "鱼雷":'爆炸物', "火箭弹":'爆炸物', "原子弹":'爆炸物', "氢弹":'爆炸物', "中子弹":'爆炸物'
    }
    # 国家及地区
    country_area = ['中国', '蒙古', '朝鲜', '韩国', '日本', '菲律宾', '越南', '老挝', '柬埔寨', '缅甸', '泰国', '马来西亚', '文莱', '新加坡',
                  '印度尼西亚','东帝汶','尼泊尔','不丹','孟加拉国','印度','巴基斯坦','斯里兰卡','马尔代夫','哈萨克斯坦','吉尔吉斯斯坦',
                  '塔吉克斯坦','乌兹别克斯坦','土库曼斯坦','阿富汗','伊拉克','伊朗','叙利亚','约旦','黎巴嫩','以色列','巴勒斯坦',
                  '沙特阿拉伯','巴林','卡塔尔','科威特','阿拉伯联合酋长国（阿联酋）','阿曼','也门','格鲁吉亚','亚美尼亚','阿塞拜疆',
                  '土耳其','塞浦路斯','芬兰','瑞典','挪威','冰岛','丹麦 法罗群岛（丹）','爱沙尼亚','拉脱维亚','立陶宛','白俄罗斯',
                  '俄罗斯','乌克兰','摩尔多瓦','波兰','捷克','斯洛伐克','匈牙利','德国','奥地利','瑞士','列支敦士登','英国',
                  '爱尔兰','荷兰','比利时','卢森堡','法国','摩纳哥','罗马尼亚','保加利亚','塞尔维亚','马其顿','阿尔巴尼亚','希腊',
                  '斯洛文尼亚','克罗地亚','波斯尼亚和墨塞哥维那','意大利','梵蒂冈','圣马力诺','马耳他','西班牙','葡萄牙','安道尔',
                  '埃及','利比亚','苏丹','突尼斯','阿尔及利亚','摩洛哥','亚速尔群岛（葡）','马德拉群岛（葡）埃塞俄比亚','厄立特里亚',
                  '索马里','吉布提','肯尼亚','坦桑尼亚','乌干达','卢旺达','布隆迪','塞舌尔','乍得','中非','喀麦隆','赤道几内亚','加蓬',
                  '刚果共和国（刚果（布））','刚果民主共和国（刚果（金））','圣多美及普林西比','毛里塔尼亚','西撒哈拉','塞内加尔','冈比亚',
                  '马里','布基纳法索','几内亚','几内亚比绍','佛得角','塞拉利昂','利比里亚','科特迪瓦','加纳','多哥','贝宁','尼日尔',
                  '加那利群岛（西）','赞比亚','安哥拉','津巴布韦','马拉维','莫桑比克','博茨瓦纳','纳米比亚','南非','斯威士兰','莱索托',
                  '马达加斯加','科摩罗','毛里求斯','留尼旺（法）','圣赫勒拿（英）','澳大利亚','新西兰','巴布亚新几内亚','所罗门群岛','瓦努阿图',
                  '密克罗尼西亚','马绍尔群岛','帕劳','瑙鲁','基里巴斯','图瓦卢','萨摩亚','斐济群岛','汤加','库克群岛（新）','关岛（美）',
                  '新喀里多尼亚（法）','法属波利尼西亚','皮特凯恩岛（英）','瓦利斯与富图纳（法）','纽埃（新）','托克劳（新）','美属萨摩亚','北马里亚纳（美）',
                  '加拿大','美国','墨西哥','格陵兰','危地马拉','伯利兹','萨尔瓦多','洪都拉斯','尼加拉瓜','哥斯达黎加','巴拿马','巴哈马','古巴','牙买加',
                  '海地','多米尼加共和国','安提瓜和巴布达','圣基茨和尼维斯','多米尼克','圣卢西亚','圣文森特和格林纳丁斯','格林纳达','巴巴多斯','特立尼达和多巴哥',
                  '波多黎各（美）','英属维尔京群岛','美属维尔京群岛','安圭拉（英）','蒙特塞拉特（英）','瓜德罗普（法）','马提尼克（法）','荷属安的列斯','阿鲁巴（荷）',
                  '特克斯和凯科斯群岛（英）','开曼群岛（英）','百慕大（英）','哥伦比亚','委内瑞拉','圭亚那','法属圭亚那','苏里南','厄瓜多尔','秘鲁','玻利维亚','巴西',
                  '智利','阿根廷','乌拉圭','巴拉圭','苏联']
    # 无效字符
    remove_chars = '[·’!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]+‘'

    # ###################################指代消解###################################################### #
    for p_key, paragraph_info in ALL_DATA.items():
        sentences = paragraph_info["sentences"]
        new_sentence = []
        original_spo=[]
        for data in sentences:  # 对每一个句子内进行处理
            prop = jieba.analyse.extract_tags(data['text'], topK=5, withWeight=False, allowPOS='r')  # 这句话中出现的代词集合
            abadon_keys = []
            if len(data['spo_list']) == 0:  # 如果没有
                new_sentence.append(data)
            elif len(data['spo_list']) == 1:  # 如果只有一个三元组
                original_spo.append({
                    "subject": data['spo_list'][0]['object']['@value'],
                    "predicate": data['spo_list'][0]["predicate"],
                    "object": data['spo_list'][0]["subject"],
                    #"label": data["label"]
                })
                if data['spo_list'][0]['object']['@value'] not in prop and data['spo_list'][0]['object']['@value'] not in remove_chars and data['spo_list'][0]['object']['@value'] != '':
                    new_sentence.append(data)
                    # print("只有一个三元组")
                    ALL_DATA[p_key]["nodes_zone"].append({
                        "subject": data['spo_list'][0]['object']['@value'],
                        "predicate": data['spo_list'][0]["predicate"],
                        "object": data['spo_list'][0]["subject"],
                        "label": data["label"]
                    })
                else:
                    print("去除", data)
            elif len(data['spo_list']) > 1:  # 如果有多个三元组  消除代词或模糊
                obj_count = dict()  # 用于统计主语数量
                for spo in data['spo_list']:  # 句内相似指代消解
                    if spo['object']['@value'] not in obj_count:
                        obj_count[spo['object']['@value']] = 1
                    else:
                        obj_count[spo['object']['@value']] = +1

                    original_spo.append({
                        "subject": spo['object']['@value'],
                        "predicate": spo["predicate"],
                        "object": spo["subject"],
                        # "label": spo["label"]
                    })

                if len(obj_count) > 1:  # 找到句子中需要被替换掉的代词或重叠词
                    print('句内存在多个主语，进行分析', obj_count.keys())
                    for key in obj_count:
                        if key in prop or key in remove_chars:
                            print(key, '是代词，需进行合并')
                            abadon_keys.append(key + '@$@' + 'FINDOBJ')
                        else:
                            for query in obj_count:
                                if simicos(key, query) > 0.5 and key != query or key.endswith(query):
                                    print(key, "和", query, '可能是同一实体的不同指代')
                                    ab_one = key if len(key) < len(query) else query
                                    selected_one = key if len(key) >= len(query) else query
                                    abadon_keys.append(ab_one + '@$@' + selected_one)
                                elif key != query:
                                    print(key, "和", query,'描述不同的实体')
                abadon_keys = list(set(abadon_keys))
                if len(abadon_keys)>0:
                    print('需要修改的词', abadon_keys)

                new_spo_list = []
                if len(abadon_keys) == 0:
                    new_spo_list = data['spo_list']
                    new_sentence.append({'text': data['text'], "spo_list": new_spo_list, "label": data["label"], "id": data["id"]})
                    #print("abadon_keys == []")
                    for spo in data['spo_list']:
                        ALL_DATA[p_key]["nodes_zone"].append({
                            "subject": spo['object']['@value'],
                            "predicate": spo["predicate"],
                            "object": spo["subject"],
                            "label": data["label"]
                        })

                else:
                    # #########################修改三元组############################# #
                    for spo in data['spo_list']:
                        print("before", data['spo_list'])
                        for stop_sign in abadon_keys:
                            if stop_sign.find(spo['object']['@value']) == 0:  # 如果这个三元组的主体需要被合并
                                bef, aft = stop_sign.split("@$@")
                                print('合并', bef, '--->', aft)
                                if aft == 'FINDOBJ':
                                    d = data['text']
                                    obj_count.pop(bef)
                                    new_object = max(obj_count.items(), key=lambda x: x[1])
                                    spo['object']['@value'] = new_object[0]
                                    new_spo_list.append(spo)
                                    # flag=jieba.analyse.extract_tags(data['text'],topK=1,allowPOS='n')
                                else:
                                    spo['object']['@value'] = aft
                                    new_spo_list.append(spo)
                            else:  # 不需要被合并
                                new_spo_list.append(spo)
                        print('refine:', new_spo_list)    # 消歧后句内的三元组集合

                    new_sentence.append({'text': data['text'], "spo_list": new_spo_list, "label": data["label"], "id": data["id"]})
                    print("abadon_keys != []")
                    for spo in new_spo_list:
                        ALL_DATA[p_key]["nodes_zone"].append({
                            "subject": spo['object']['@value'],
                            "predicate": spo["predicate"],
                            "object": spo["subject"],
                            "label":data["label"]
                        })
        print("n:\n", len(new_sentence))

        ALL_DATA[p_key]["sentences"]=new_sentence
    #################################################################################################


    # ######################################段内实体对齐################################################## #
    for para in ALL_DATA:
        print("Paragrapgh ==============",para)
        spo_zone = ALL_DATA[para]["nodes_zone"]
        if len(spo_zone)== 0:
            continue
        node_id = 1
        for spo in spo_zone:   # 三元组去噪处理
            # ########################################删除无效三元组####################################################
            if spo["subject"] in remove_chars or spo["object"] in remove_chars or spo["object"]==spo["subject"]:
                print("三元组无效，删除该三元组：",spo)
                spo["subject"] = ''
                spo["object"] = ''
                spo["predicate"] = ''
            # ##############################如果小类名称出现在主语部分，则进行分析##########################################
            elif spo["subject"] in classes:
                # print("说明了主体的类型为:",spo["subject"],"寻找主体名称")
                subject_name = {}
                if spo['predicate'] == '型号' and spo["object"] != spo["subject"]:
                    # print("找到实体的名称与其型号")
                    # spo['label']=spo['predicate']
                    # ALL_DATA[para]["nodes"]["node"+str(node_id)]={
                    #     "label":[spo["subject"],small2big[spo["subject"]]],
                    #     "名称":spo["object"]
                    # }
                    temp_sub = spo["subject"]
                    spo["subject"] = spo["object"]
                    # spo["object"]=ALL_DATA[para]["nodes"]["node"+str(node_id)]["label"][0]
                    spo["object"] = temp_sub
                elif spo['predicate'] != '型号' and spo["object"] != spo["subject"]:
                    for node_name in ALL_DATA[para]["nodes"]:
                        if ALL_DATA[para]["nodes"][node_name]["label"][0] == spo["subject"]:
                            print("考虑主语置换")
                            new_spo = {
                                "subject": ALL_DATA[para]["nodes"][node_name]["名称"],
                                "predicate": spo['predicate'],
                                "object": spo["object"],
                                "label": spo["subject"]
                            }
                            ALL_DATA[para]["nodes_zone"].append(new_spo)
                            # spo["subject"]=ALL_DATA[para]["nodes"][node_name]["名称"]
            # ##################################其他情况#############################################################
            else:
                continue
                # print("非特殊三元组，直接保留")

                # for spo_query in spo_zone:
                #     if spo_query['predicate']=='型号' and spo["subject"]==spo_query["subject"]:
                #         subject_name[spo_query["object"]]=0 if spo_query["object"] not in subject_name else \
                #         subject_name[spo_query["object"]]+1
                # sub_name = subject_name[0] if len(subject_name) == 1 else find_name(subject_name)
                # if sub_name==None:
                #     print("实体名称缺失，出大问题")
        # ###################################cluster& analysis############################################
        with open("spo_in_para.csv", 'w', encoding='utf-8',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["index", "subject", "predicate", "object", "label"])
            id = 0
            for data in spo_zone:
                if data['subject'] != '':
                    writer.writerow([id, data['subject'], data['predicate'], data['object'], data['label']])
                    id += 1
        if id >1:
            print("进行聚类分析......")
            cluster("spo_in_para.csv", "cluster_in_para.csv")
            print("完成聚类分析")
            clusters = {}
            with open("F:/graduate_design/code/knowledge_label/cluster_in_para.csv", "r", encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # 这里不需要readlines
                for line in reader:
                    if line != [] and line[0] != 'Cluster ID':
                        if line[0] not in clusters:
                            clusters[line[0]] = []
                        clusters[line[0]].append(line[3:])
            print(clusters)
            # ################################聚类后簇内消歧####################################### #
            for cls in clusters:
                item = {
                    "label": ['', ''],
                    "名称": '',
                }
                for it in clusters[cls]:
                    if it[0] not in classes and item["名称"] == '':
                        item["名称"] = it[0]
                    if it[1] == '型号' and it[2] in classes:
                        item['label'] = [it[2],small2big[it[2]]]
                    elif it[1] == '型号' and it[2] not in classes:
                        print("进行翻转操作")
                        item["名称"] = it[2]
                    elif it[0] not in classes and it[1] != '型号':
                        # ##################对产国名称需要准确化################### #
                        if it[1] == '产国':
                            if it[2] not in country_area:
                                for ca in country_area:
                                    if it[2].find(ca) >= 0:
                                        print("准确化：",it[2],'---->',ca)
                                        it[2]=ca
                                        break
                                    elif ca.find(it[2]) >= 0:
                                        print("名称查询",it[2],'--->',ca)
                                        if para_dict[para]["content"].find(ca)>=0:
                                            print("查询成功")
                                            it[2] = ca
                                            break
                                        else:
                                            print("查询失败，保留原信息")
                                if it[2] not in country_area:
                                    print("国家/地区信息错误，删除")
                                    it[2]=''
                        if it[1] in item and it[2] != item[it[1]]:
                            print("已存在属性，进行消歧：",it[2],"<---->",item[it[1]][0])
                            if simicos(it[2],item[it[1]]) > 0.5:
                                # print("属性值相似度高，进行合并")
                                new_v=it[2] if len(it[2]) >= len(item[it[1]]) else it[2]
                            else:
                                # print(it[1],"属性值相似度低，进行对比")
                                if it[1] in ['宽度','长度','高度','重量']:
                                    if len(it[2]) != len(item[it[1]][0]):
                                        result = item[it[1]][0] if len(item[it[1]][0]) >= len(it[2]) else it[2]
                                        #it[2]=result
                                        # print("比长度")
                                    else:
                                        center=para_dict[para]["content"].find(it[1][0])
                                        pos1 = para_dict[para]["content"].find(item[it[1]][0])
                                        pos2 = para_dict[para]["content"].find(it[2])
                                        result = item[it[1]][0] if abs(center-pos1) < abs(center-pos2) else it[2]
                                        #it[2]=result
                                        # print("找位置，", abs(center - pos1), abs(center - pos2))
                                    # print(result)
                                    item[it[1]] = [result]
                                    # else:
                                    #     result = item[it[1]][0] if len(item[it[1]][0]) > len(it[2]) else it[2]
                                    #     item[it[1]] = [result]
                                    #     print("看长度",result)
                                else:
                                    item[it[1]] = [item[it[1]][0], it[2]]

                        elif it[2] != '':
                            item[it[1]] = [it[2]]
                if item["名称"] != '':
                    if item["label"] != ['', '']:
                        ALL_DATA[para]["nodes"]["node" + str(node_id)] =item
                        node_id += 1
                    else:
                        mini_label=vote_value(clusters[cls],3)
                        item["label"] = [mini_label,small2big[mini_label]]
                        ALL_DATA[para]["nodes"]["node" + str(node_id)] = item
                        node_id += 1
            print("nodes")
            print(ALL_DATA[para]["nodes"])
        else:
            only_data=spo_zone[0]
            # print("only_data:")
            if only_data['predicate'] == '产国':
                if only_data['object'] not in country_area:
                    for ca in country_area:
                        if only_data['object'].find(ca) >= 0:
                            print("准确化：", only_data['object'], '---->', ca)
                            only_data['object'] = ca
                            break
                        elif ca.find(only_data['object']) >= 0:
                            print("名称查询", only_data['object'], '--->', ca)
                            if para_dict[para]["content"].find(ca) >= 0:
                                print("查询成功")
                                only_data['object'] = ca
                                break
                            else:
                                print("查询失败，保留原信息")
                    if only_data['object'] not in country_area:
                        print("国家/地区信息错误，删除")
                        only_data['object'] = ''

            ALL_DATA[para]["nodes"]["node1"]={
                    "label": [only_data['label'], small2big[only_data['label']]],
                    "名称": only_data['subject']
                    #only_data['predicate']:[only_data['object']]
                }
            if only_data['predicate'] != '型号':
                ALL_DATA[para]["nodes"]["node1"][only_data['predicate']]=[only_data['object']]
            else:
                if only_data['object']!=only_data['label'] and only_data['object'] in classes:
                    ALL_DATA[para]["nodes"]["node1"]["label"]=[only_data['object'], small2big[only_data['object']]]
                if only_data['object'] != only_data['label'] and only_data['object'] not in classes:
                    ALL_DATA[para]["nodes"]["node1"]["名称"]=only_data['object']
        # ################################################################################### #

        # ###################################生成关系######################################### #
        rel_id=0
        for n in ALL_DATA[para]["nodes"].values():
            if "产国" in n:
                print("创建关系", n['名称'], '->', '产国', n['产国'])
                ALL_DATA[para]["rels"]["rel"+str(rel_id)]={
                    'start': n['名称'],
                    "end": n['产国'],
                    'rel_name': '产国'
                }
                rel_id += 1
            if "研发单位与厂商" in n:
                print("创建关系", n['研发单位与厂商'], '->', '生产研发', n['名称'])
                ALL_DATA[para]["rels"]["rel" + str(rel_id)] = {
                    'start': n['研发单位与厂商'],
                    "end": n['名称'],
                    'rel_name': '生产研发'
                }
                rel_id += 1
            if "产国" in n and "研发单位与厂商" in n:
                print("创建关系", n['研发单位与厂商'], '->', '属于', n['产国'])
                ALL_DATA[para]["rels"]["rel" + str(rel_id)] = {
                    'start': n['研发单位与厂商'],
                    "end": n['产国'],
                    'rel_name': '属于'
                }
                rel_id += 1
        print(ALL_DATA[para]["rels"])

    print('original')
    print(original_spo)
    print('processed')
    for p in ALL_DATA:
        print(ALL_DATA[p].pop("nodes_zone"))
        ALL_DATA[p].pop("sentences")
    # print(ALL_DATA)
    with codecs.open(final_path, 'w', 'utf-8') as f:
        ALL_DATA = json.dumps(ALL_DATA, ensure_ascii=False)
        f.write(ALL_DATA)
        f.write('\n')
    with codecs.open('F:/graduate_design/code/knowledge_label/output/id2para.json', 'w', 'utf-8') as f:
        PARA_DICT = json.dumps(para_dict, ensure_ascii=False)
        f.write(PARA_DICT)
        f.write('\n')