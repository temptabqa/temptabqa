import openai
import pandas as pd
from tqdm import tqdm
import glob
import json
import time

DF_PATH=''
RESULT_PATH = ''
openai.api_key = "<KEY>"

#zero shot
def prepare_example(context, question):
    return f"""
    Answer the question based on the context provided (take the current year as 2022)
    generate only the relevant answer do not include the question and unnecessary verbs in it thus generate small answer within 1 to 10 words.

    question : {question}
    context : ***{context}***
    answer : """

#few shot without reasoning
# def prepare_example(context, question):
#     return f"""
#     Answer the questions based on the context provided (take the current year as 2022)
#     questions : How old was Charles Brenton Huggins when he won the Nobel Prize in 1966?

#     context : ***category
#     nobel

#     Charles Brenton Huggins
#     Born	( | 1901-09-22 | ) | September 22, 1901 | Halifax, Nova Scotia
#     Citizenship	Canadian / American
#     Awards	Nobel Prize for Physiology or Medicine | (1966) | Gairdner Foundation International Award | (1966)
#     ['Charles Brenton Huggins nobel.jpg | Charles Brenton Huggins']***
#     answers : 65 years old

#     ###
#     question : When was the last time that Frederick John Perry won the Davis Cup?
#     context : ***category
#     tennis

#     Full name
#     Frederick John Perry

#     Died
#     2 February 1995 | (1995-02-02) | (aged 85) | Melbourne, Victoria, Australia

#     Team competitions
#     Davis Cup	W | (1933, 1934, 1935, 1936)***
#     answer : 1936
#     ###
#     question : {question}
#     context : ***{context}***
#     answer :"""

#few shot with reasoning
# def prepare_example(context, question):
#     return f"""
#     Answer the question based on the context provided (take the current year as 2022)
#     generate only the relevant answer do not include the question and unnecessary verbs in it thus generate small answer within 1 to 10 words.
#     Also give the proper reasoning with the answer, first answer then the reason for the generated answer.

#     question :
#     How old was Charles Brenton Huggins when he won the Nobel Prize in 1966?

#     context : ***category
#     nobel

#     Charles Brenton Huggins
#     Born	( | 1901-09-22 | ) | September 22, 1901 | Halifax, Nova Scotia
#     Citizenship	Canadian / American
#     Awards	Nobel Prize for Physiology or Medicine | (1966) | Gairdner Foundation International Award | (1966)
#     ['Charles Brenton Huggins nobel.jpg | Charles Brenton Huggins']***
#     answer and reasoning: 65 years old && Charles was born in 1901 and he won the price in 1966, thus he was 65 years old. (1966 - 1901)
#     ###
#     question : When was the last time that Frederick John Perry won the Davis Cup?
#     context : ***category
#     tennis

#     Full name
#     Frederick John Perry

#     Died
#     2 February 1995 | (1995-02-02) | (aged 85) | Melbourne, Victoria, Australia

#     Team competitions
#     Davis Cup	W | (1933, 1934, 1935, 1936)***
#     answer and reasoning: 1936 && He won the davis cup four times among them 1936 is the lastest year in which he won.
#     ###
#     question : {question}
#     context : ***{context}***
#     answer and reasoning: """

def chatgpt_result(question):
    completion=openai.ChatCompletion.create(
      model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
      messages=[{"role": "user", "content": question}]
    )
    print(completion.usage)
    return completion.choices[0].message.content


id_to_json = {}

for filename in glob.glob("../data/maindata/tables/json/*"):
  f = open(filename,'r')
  data = json.load(f)
  id_to_json[int(filename.split("/")[-1].split(".")[0])] = data

df=pd.read_csv('./data/maindata/qapairs/dev-set/dev-set.csv')

table_string = {}
tables=id_to_json.keys()
for tab in tqdm(tables):
  table_s = ""
  table=id_to_json[tab]
  for key in table.keys():
    if type(table[key]) == type(dict()):
      table_s = table_s + key + "\n"
      for sub_key in table[key].keys():
        if sub_key == key:
          table_s = table_s + str(table[key][sub_key]) + "\n"
        else:
          table_s = table_s + sub_key +"\t" + table[key][sub_key] + "\n"
      table_s = table_s + "\n"
    else:
      table_s = table_s + key +"\n" + table[key] + "\n\n"

  table_string[tab] = table_s

try:
  df_eval_original=pd.read_csv(RESULT_PATH)
except:
  df_eval_original=pd.DataFrame()

df_eval = pd.DataFrame()
actual_answers=[]
all_qs=[]
all_tabs=[]
all_output = []
count = 0
start = len(df_eval_original)

df=pd.read_csv(DF_PATH)

for i in tqdm(range(start,len(df))):
    t=df['table_id'][i]
    q=df['question'][i]
    ans=df['answer'][i]
    count += 1
    all_qs.append(q)
    all_tabs.append(t)
    actual_answers.append(ans)

    context = table_string[t]
    input_text = prepare_example(context,q)

    jum = 0
    while True:
      try:
          if jum == 3:
            result = "res"
          else:
            # print(input_text)
            result = chatgpt_result(input_text)
          # time.sleep()
          break
      except:
          jum += 1
          print("....halt....")
          time.sleep(20)

    all_output.append(result)
    # print(input_text)
    print(ans,result)

    if count%5 == 0:
      df_eval['actual_answer']=actual_answers
      df_eval['question']=all_qs
      df_eval['table']=all_tabs
      df_eval['predicted_answer']=all_output
      df_eval_original = pd.concat([df_eval_original, df_eval], ignore_index=True, sort=False)
      df_eval_original.to_csv(RESULT_PATH,index=False)
      df_eval_original=pd.read_csv(RESULT_PATH)

      all_tabs = []
      all_output = []
      all_qs = []
      actual_answers = []
      df_eval = pd.DataFrame()

df_eval['actual_answer']=actual_answers
df_eval['question']=all_qs
df_eval['table']=all_tabs
df_eval['predicted_answer']=all_output
df_eval_original = pd.concat([df_eval_original, df_eval], ignore_index=True, sort=False)
df_eval_original.to_csv(RESULT_PATH,index=False)