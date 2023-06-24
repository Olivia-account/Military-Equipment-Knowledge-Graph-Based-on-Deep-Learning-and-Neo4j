import json
import csv
input_path = r'C:\Users\zhour\PycharmProjects\neo4j_practice\dedupe-examples-master\dedupe-examples-master\knowledge_label\datam\duie.json'
f = open(input_path, 'r', encoding='utf-8')
with open("spo.csv", 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["index", "subject", "predicate", "object", "label"])
id = 0
for data in f:

    with open("spo.csv", 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(["index", "subject", "predicate", "object", "label"])

        data = json.loads(data)
        spo_zone=data["spo_list"]
        label=data['label']
        for data in spo_zone:
            if data['subject'] != '':
                writer.writerow([id,data['object']['@value'] , data['predicate'],data['subject'] ,label])
                id += 1