from transformers import AutoTokenizer, T5ForConditionalGeneration
import torch
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from datasets import Dataset, DatasetDict
import dataclasses
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from transformers import Trainer, TrainingArguments
import torch.nn as nn
from torch.nn.parallel import DataParallel
import os

if torch.cuda.is_available():
    device = 'cuda'
else:
    device = 'cpu'
    
df = pd.read_csv("../../../data/maindata/qapairs/combinedata/all_annotated_data.csv")

tables = df["Input.table"].unique()

table_id_mapping={}
id_table_mapping={}
for i,t in enumerate(df['Input.table'].unique()):
  table_id_mapping[t]=i
  id_table_mapping[i]=t

table_qs = {}
table_hitid = {}
for i in range(len(df)):
  if df['Input.table'][i] not in table_qs.keys():
    table_qs[df['Input.table'][i]]=set()
    table_hitid[df['Input.table'][i]]=set()
  table_qs[df['Input.table'][i]].add(df['question'][i])
  table_hitid[df['Input.table'][i]].add(df['HITId'][i])

category_to_table = {}
table_to_category = {}
category_counts = {}
for i in range(len(df)):
  table_to_category[df['Input.table'][i]] = df['Input.category'][i]
  if df['Input.category'][i] not in category_to_table.keys():
    category_to_table[df['Input.category'][i]] = set()
  category_to_table[df['Input.category'][i]].add(df['Input.table'][i])

for x in category_to_table:
  category_counts[x] = len(category_to_table[x])
category_counts = pd.Series(category_counts)

question_answer_mapping = {}
for table,question,answer in zip(df['Input.table'],df["question"],df["answer"]):
  question_answer_mapping[table,question] = answer

def remove_italics(soup):
    for i in soup.findAll('i'):
        i.replaceWithChildren()
    return soup

def clean_stack(stack):
    #clean=stack
    clean=[]
    count=0
    for word in stack:
        if(clean_string(str(word))!=""):
            if(count!=0):
                clean.append("|")
            clean.append(clean_string(str(word)))
            count+=1
    s = " "
    for word in clean:
        #print(word)
        if(s[-1]!=" "):
            s = s+ " "+word
        else:
            s = s+word
    if(s.isspace()==False):
        #print(s[1:])
        return(s[1:])
    else:
        return ""

def clean_string(string):
    filter_arr=['\n','\xa0','\u200b','•']
    s2=""
    for char in string:
        if(char not in filter_arr):
            s2=s2+char
        else:
            s2 = s2+" "
    s2 = re.sub(' +', ' ',s2)
    if(s2.isspace()==False and len(s2)>=1):
        while(s2[-1]==":" or s2[-1]=="：" or s2[-1]==" "):
            s2= s2[:-1]
            if(len(s2)<1):
                break
        return s2
    else:
        return ""

def find_colon(string):
    try:
        i = len(string)
        while(string[i-1]==" " or string[i-1]=="\n"):
            i=i-1
        if(string[i-1]==":" or string[i-1]=="："):
            return True
        return False
    except:
        return False

def html2json_convertor(table,category):
  soup = BeautifulSoup(table,'lxml')

  for abbrevation in soup(["abbr"]):
    abbrevation.replace_with(abbrevation["title"] + " ")

  soup = remove_italics(soup)

  for img in soup(["img"]):
    img.replace_with(img["alt"])

  main_json = {}

  header_dictionary = {}
  header_name = ""

  non_th_list = []

  main_json["category"] = category

  if soup.find("caption") != None:
    main_json["caption"] = clean_stack(soup.find("caption").findAll(string=True))

  for tr in soup.findAll('tr'):
    if tr.findAll(string=True) == []:
      continue

    if tr.findAll("table") != []:
      continue
    # print(tr)
    # print(header_name)

    if len(tr.findAll('td'))==1 and len(tr.findAll('th'))==1:
      key = clean_stack(tr.find('th').findAll(string=True))
      value = clean_stack(tr.find('td').findAll(string=True))

      if header_name == "":
        main_json[key] = value
      else:
        header_dictionary[key] = value
      continue

    if len(tr.findAll('td'))==2 and len(tr.findAll('th'))==0:
      if len(tr.find('td').findAll('b'))!=0 :
        key = clean_stack(tr.find('td').findAll(string=True))
        value = clean_stack(tr.findAll('td')[1].findAll(string=True))

        if header_name == "":
          main_json[key] = value
        else:
          header_dictionary[key] = value
        continue      

      elif 'font-weight:' in str(tr.find('td')) :
        key = clean_stack(tr.find('td').findAll(string=True))
        value = clean_stack(tr.findAll('td')[1].findAll(string=True))

        if header_name == "":
          main_json[key] = value
        else:
          header_dictionary[key] = value
        continue      

    if len(tr.findAll('td'))==2 and len(tr.findAll('th'))==0 and find_colon(tr.find('td').find(string=True))==True:
      key = clean_stack(tr.find('td').findAll(string=True))
      value = clean_stack(tr.findAll('td')[1].findAll(string=True))

      if header_name == "":
        main_json[key] = value
      else:
        header_dictionary[key] = value
      continue



    if len(tr.findAll('td'))==0 and len(tr.findAll('th'))==1:
      if header_name != "":
        if len(non_th_list) > 0:
          header_dictionary[header_name] = non_th_list
          # main_json[header_name + "_list"] = non_th_list

        main_json[header_name] = header_dictionary

        header_name = ""
        header_dictionary = {}
        non_th_list = []

      header_name = clean_stack(tr.find('th').findAll(string=True))
      continue

    if len(tr.findAll('td'))==1 and len(tr.findAll('th'))==0:
      if len(tr.find('td').findAll('b'))!=0:
        if header_name != "":
          if len(non_th_list) > 0:
            header_dictionary[header_name] = non_th_list
            # main_json[header_name + "_list"] = non_th_list

          main_json[header_name] = header_dictionary

          # if len(non_th_list) > 0:
          #   main_json[header_name] = non_th_list

          header_name = ""
          header_dictionary = {}   
          non_th_list = []  

        header_name = clean_stack(tr.find('td').findAll(string=True))
        continue

      elif 'font-weight:' in str(tr.find('td')):
        if header_name != "":
          if len(non_th_list) > 0:
            header_dictionary[header_name] = non_th_list
            # main_json[header_name + "_list"] = non_th_list

          main_json[header_name] = header_dictionary

          # if len(non_th_list) > 0:
          #   main_json[header_name] = non_th_list

          header_name = ""
          header_dictionary = {}   
          non_th_list = []  

        header_name = clean_stack(tr.find('td').findAll(string=True))
        continue

    if header_name != "":
      stack = []
      for td in tr.findAll(['th','td']):
        if len(clean_stack(td.findAll(string=True))) != 0:
          # if 
          stack.append(clean_stack(td.findAll(string=True)))
      if clean_stack(stack) != "":
        non_th_list.append(clean_stack(stack))

      continue

    if len(tr.findAll('td')) == 1 and len(tr.findAll('th')) == 0 and header_name == "":
      # print(tr.find('td').attrs["class"])
      if "class" in tr.find('td').attrs and tr.find('td').attrs["class"][0] == "infobox-image":
        key = "infobox-image"
        value = clean_stack(tr.find('td').findAll(string=True))

        main_json[key] = value
        continue

    # print(tr)
    # print(header_name)
      

  if header_name != "":
    if len(non_th_list) > 0:
      header_dictionary[header_name] = non_th_list
      # main_json[header_name + "_list"] = non_th_list

    main_json[header_name] = header_dictionary

    # if len(non_th_list) > 0:
    #   main_json[header_name] = non_th_list

    header_name = ""
    header_dictionary = {}
    non_th_list = []

  return main_json
table_json = {}
for table in tqdm(tables[:-1]):
  table_id = table_id_mapping[table]
  category = table_to_category[table]
  ptable = table.replace("—",'-')
  ptable = ptable.replace("–",'-')
  ptable = ptable.replace("–",'-')
  ptable = ptable.replace("–",'-')
  ptable = ptable.replace("–",'-')
  json_object = html2json_convertor(ptable,category)

  table_json[table] = json_object

table_to_csv = {}
for table in tqdm(table_json.keys()):
  json = table_json[table]

  data = {}
  for key in json.keys():
    if type(json[key]) == type(dict()):
      for sub_key in json[key].keys():
        if sub_key == key:
          for i in range(len(json[key][sub_key])):
            new_key = key + "/list_" + str(i+1)
            data[new_key] = json[key][sub_key][i]
        else:
          new_key = sub_key + "(" + key + ")"
          data[new_key] = json[key][sub_key]

    else:
      data[key] = json[key]
  # print(table_id_mapping[table])
  csv = pd.DataFrame(data,index=[0])

  table_to_csv[table] = csv

test_list = {'actor': [2, 8, 3], 'agency': [1139, 1141, 1143], 'aircraft': [1130, 1128, 226], 'athelete': [1026, 963, 1024], 'badminton': [166, 174, 129], 'baseball': [405, 401, 400], 'basketball': [569, 566, 568], 'board game': [1147, 1163, 1188], 'body builder': [806, 866, 778], 'car driver': [518, 516, 521, 523], 'character': [1104, 1101, 1095], 'christian leader': [817, 829, 824], 'church': [714, 715, 719], 'company': [597, 592, 595], 'concert': [1054, 1034, 1035], 'conference': [], 'country': [424, 436, 438], 'court': [254, 253, 257], 'curling': [291, 281, 288], 'current war': [964, 990, 1006, 1018], 'earthquake': [1042, 1036, 1047], 'economy': [235, 243, 248, 250], 'emperor': [122, 765, 119], 'empire': [430, 22, 433], 'figure skating': [747, 748, 743, 735], 'football': [], 'footballer': [36, 40, 479], 'game': [1151, 1161, 1175], 'golf': [66, 68, 70], 'handball': [503, 493, 504, 492], 'ice hockey': [577, 561, 579], 'lacrosse': [656, 642, 644, 655], 'legislature': [935, 936], 'martial artist': [849, 840, 264], 'military conflict': [1014, 1012, 966], 'monument': [751, 726, 626], 'music': [1071, 1066, 1070], 'musician': [472, 468, 347], 'national cricket team': [1191], 'nba': [81, 89, 83], 'nfl': [551, 540, 547, 546], 'nobel': [352, 369, 370], 'office holder': [928, 913, 861], 'painter': [349, 350, 356], 'painting': [], 'person': [340, 353, 915], 'racing': [265, 517, 272], 'rugby': [74, 75, 558], 'sailor': [668, 688, 677, 671], 'scientist': [315, 364, 321], 'skier': [781, 804, 791, 793], 'song': [1075, 1070], 'space probe': [457, 1206, 452], 'swimming': [115, 118, 669, 665], 'tabletennis': [710], 'tennis': [50, 509, 512], 'university': [611, 624, 606], 'volleyball': [96, 588, 93], 'war_conflict': [1015, 972, 985], 'website': [600], 'wrestling': [7, 339, 13], 'civil war': [1022, 979], 'album': [948, 942], 'event': [1056, 634], 'railway': [464, 465], 'navy vessel': [1113, 1109], 'cricket team': [1172, 1164], 'fighter': [229], 'stadium': [621, 627], 'space program': [1132, 1062], 'national football team': [1166, 1160], 'politician': [904], 'launchpad': [629, 628], 'show': [1088, 1085], 'movie': [1078, 1077], 'rail line': [1092, 1094], 'book': [929, 702]}
dev_list = {'actor': [1], 'agency': [1142], 'aircraft': [1131], 'athelete': [960, 1025, 1027], 'badminton': [165, 164, 127], 'baseball': [403], 'basketball': [570], 'board_game': [1184, 1171], 'body builder': [794], 'car driver': [266, 275], 'character': [1099, 1103], 'christian leader': [832, 823, 825], 'church': [720], 'company': [604], 'concert': [952], 'conference': [], 'country': [439], 'court': [256], 'curling': [299, 301, 287], 'current war': [995], 'earthquake': [1038], 'economy': [232, 252], 'emperor': [766], 'empire': [418, 432, 421], 'figure skating': [746, 739], 'football': [], 'footballer': [483], 'game': [1148], 'golf': [530, 60, 72], 'handball': [505, 499], 'ice hockey': [572], 'lacrosse': [646, 645], 'legislature': [934], 'martial artist': [848], 'military conflict': [968, 967, 1017], 'monument': [724], 'music': [1075], 'musician': [469], 'national cricket team': [], 'nba': [86], 'nfl': [548, 540], 'nobel': [365, 334, 446], 'office holder': [895, 873, 858], 'painter': [359], 'painting': [], 'person': [855, 391], 'racing': [274], 'rugby': [77], 'sailor': [675, 694], 'scientist': [320, 337, 867], 'skier': [797, 775], 'song': [1071], 'space probe': [450], 'swimming': [113, 660], 'tabletennis': [787], 'tennis': [511], 'university': [607], 'volleyball': [95], 'war_conflict': [976], 'website': [632], 'wrestling': [323], 'civil war': [197], 'album': [949], 'event': [], 'railway': [463], 'navy vessel': [], 'cricket team': [1156], 'fighter': [], 'stadium': [618], 'space program': [1051], 'national football team': [1170], 'politician': [], 'launchpad': [630], 'show': [1087], 'movie': [1079], 'rail line': [1135], 'book': [1064]}
adversarial_list=['ship',
 'time zone',
 'cyclone',
 'holiday',
 'planet',
 'terrorist orgnization',
 'disease',
 'proxy war',
 'sports event',
 'sumo',
 'orbitor',
 'cricket',
 'squash',
 'boxing',
 'hockey',
 'army',
 'cycling',
 'political party',
 'f1']
 
table_string = {}
for table in tqdm(tables[:-1]):
  table_s = ""
  for key in table_json[table].keys():
    if type(table_json[table][key]) == type(dict()):
      table_s = table_s + key + "\n"
      for sub_key in table_json[table][key].keys():
        if sub_key == key:
          table_s = table_s + str(table_json[table][key][sub_key]) + "\n"
        else:
          table_s = table_s + sub_key +"\t" + table_json[table][key][sub_key] + "\n"
      table_s = table_s + "\n"
    else:
      table_s = table_s + key +"\n" + table_json[table][key] + "\n\n"

  table_string[table] = table_s

test_dev_table_ids = []

test_data = []
for category in test_list:
  for table_id in test_list[category]:
    test_dev_table_ids.append(table_id)
    table = id_table_mapping[table_id]
    for question in table_qs[table]:
      test_data.append({"table_json": table_string[table] ,"question" : question , "answer" : question_answer_mapping[table,question]})
test_dataset = Dataset.from_list(test_data)

dev_data = []
for category in dev_list:
  for table_id in dev_list[category]:
    test_dev_table_ids.append(table_id)
    table = id_table_mapping[table_id]
    for question in table_qs[table]:
      dev_data.append({"table_json": table_string[table]  ,"question" : question , "answer" : question_answer_mapping[table,question]})
dev_dataset = Dataset.from_list(dev_data)

adversarial_data = []
for category in adversarial_list:
  for table in category_to_table[category]:
    for question in table_qs[table]:
      adversarial_data.append({"table_json": table_string[table]  ,"question" : question , "answer" : question_answer_mapping[table,question]})
adversarial_dataset = Dataset.from_list(adversarial_data)

train_data = []
for category in category_to_table.keys():
  for table in category_to_table[category]:
    table_id = table_id_mapping[table]
    if table_id in test_dev_table_ids:
      continue
    if table_id == 1207:
      print(category)
      continue
    for question in table_qs[table]:
      train_data.append({"table_json": table_string[table]  ,"question" : question , "answer" : question_answer_mapping[table,question]})
train_dataset = Dataset.from_list(train_data)

raw_dataset = DatasetDict({
                        'train': train_dataset,
                        'validation': dev_dataset,
                        'test': test_dataset,
                        "adversarial" : adversarial_dataset,
                      })

raw_dataset

#torch.cuda.empty_cache();
print(device)   
tokenizer = AutoTokenizer.from_pretrained('google/flan-t5-base')
model = T5ForConditionalGeneration.from_pretrained('flant5_base_finetune').cuda()

def prepare_example(context, question):
    return f"question: {question} </s> context: {context} </s>"

c = 0
for classify in tqdm(["head", "dev", "tail"]):
  df_eval=pd.DataFrame()
  input_data=[]
  output=[]
  actual_answers=[]
  all_qs=[]
  all_tabs=[]
  df=pd.read_csv("../../../data/maindata/qapairs/" + classify + "-set/" + classify + "-set.csv")
  tables=df['table_id'].unique()
  for t in tqdm(tables):
    t = id_table_mapping[t]
    if table_id_mapping[t]==1207:
      continue
    for q in table_qs[t]:
      all_qs.append(q)
      all_tabs.append(t)
      actual_answers.append(question_answer_mapping[t,q])
      input_data.append( 
          {
              "context": table_string[t],
              "question": q
          })
  # if f==1:
  #   continue
  for example in tqdm(input_data):
    input_text = prepare_example(example['context'], example['question'])
    #print(input_text)
    input_ids = tokenizer(input_text,max_length=2048,return_tensors="pt",truncation=True,padding=True).input_ids.cuda()
    with torch.no_grad():
        outputs = model.generate(input_ids, bos_token_id=0)
        
    input_ids = input_ids.cpu()
    outputs = outputs.cpu()
    del input_ids
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    
    #if c < 20:
    print(result)
    output.append(result)
    if c == 20:
        print(output)
        
    c+=1
  
  df_eval['predicted_answer']=output
  df_eval['actual_answer']=actual_answers
  df_eval['question']=all_qs
  df_eval['table']=all_tabs
  df_eval.to_csv(classify+'_eval_flant5_base_finetune.csv')
 
