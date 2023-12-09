import pandas as pd
import os
import re
import glob
from tqdm import tqdm
import numpy as np
import json
import math
import copy
from glob import glob

df = pd.DataFrame()
for file in tqdm(glob("./annotation_batches/*.csv")):
  tmp = pd.read_csv(file)
  df = df.append(tmp, ignore_index = True)

df=df[['AssignmentId','WorkerId','AssignmentStatus','Input.table','Input.table_id','Input.name','Input.category','Input.question1', 'Input.a1', 'Answer.Ans1',
       'Answer.Res1', 'Approve', 'Reject','Input.question2', 'Input.a2', 'Answer.Ans2',
       'Answer.Res2','Input.question3', 'Input.a3', 'Answer.Ans3',
       'Answer.Res3']]


l=[]
for i in range(len(df)):
  di={}
  for c in ['AssignmentId','WorkerId','AssignmentStatus','Input.table','Input.table_id','Input.name','Input.category']:
    di[c]=df[c][i]
  for j in range(1,4):
    di2=di.copy()

    di2['question'] = df['Input.question'+str(j)][i]
    di2['gold_answer'] = df['Input.a'+str(j)][i]
    di2['answer'] = df['Answer.Ans'+str(j)][i]
    di2['explanation'] = df['Answer.Res'+str(j)][i]
    # print(di2['question'],di2['gold_answer'])
    l.append(di2)
dft = pd.DataFrame(l)
dft.dropna(subset = ['question','answer'],inplace=True)
dft=dft[dft['AssignmentStatus']!='Rejected'].reset_index()

ids=[]
names=[]
for i in range(len(dft)):
  if type(dft['Input.table_id'][i])==type("") and not dft['Input.table_id'][i].isdigit():
    ids.append(dft['Input.name'][i])
    names.append(dft['Input.table_id'][i])
  else:
    names.append(dft['Input.name'][i])
    ids.append(dft['Input.table_id'][i])
dft['Input.table_id']=ids
dft['Input.name']=names

df2=dft[['question', 'Input.table_id']]
df2=df2.drop_duplicates()
# len(df2)

l=[]
for q, table in zip(df2['question'], df2['Input.table_id']):
  d={}
  d['question']=q
  d['Input.table_id']=table
  # print(q, table)
  t = dft[ (dft['question']==q) & (dft['Input.table_id']==table) ]
  # print(len(t))
  # break
  d['assinment_ids'] = list(t['AssignmentId'])
  d['worker_ids'] = list(t['WorkerId'])
  d['answers'] = list(t['answer'])
  d['explanations'] = list(t['explanation'])
  t=t.reset_index()
  for c in t.columns:
    if c not in ['WorkerId', 'answer', 'explanation','Approve','Reject', 'AssignmentStatus','Input.num','AssignmentId','Input.table_id']:
      if len(t[c])!=0:

        d[c]=list(t[c])[0]
      # else:
      #   print(q)
  l.append(d)
df_t=pd.DataFrame(l)
try:
  df_t=df_t.drop(['level_0','index'],axis=1)
except:
  pass
df_t.to_csv('./combined_verification_pseudo_wid.csv')

