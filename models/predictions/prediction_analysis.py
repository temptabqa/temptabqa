import pandas as pd
import nltk
nltk.download('wordnet')
from nltk.translate import meteor_score
from rouge_score import rouge_scorer
import sys
from evaluate import load
import re
from word2number import w2n
from datetime import datetime
import calendar


date_regex = re.compile(r"\b((?:0?[1-9]|[12]\d|3[01])[-/](?:0?[1-9]|1[0-2])[-/]\d{4})|(?:\d{4}[-/](?:0?[1-9]|1[0-2])[-/](?:0?[1-9]|[12]\d|3[01]))|(?: (?:0?[1-9]|1[0-2])[-/](?:0?[1-9]|[12]\d|3[01])[-/] \d{4})\b")
date_only = [#28 jan or jan 28
      '(\d{2}|\d|date)(th)*\s*(of|-)*\s*((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?)',
      '((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?)(-|\s+)(\d)',
]

def convert_date_to_dd_mm(date_string):
    try:
        pattern = r'(\d{1,2})(?:th|st|nd|rd)?\s+(?:of\s+)?(January|February|March|April|May|June|July|August|September|October|November|December)'
        pattern1 = r'(\d{1,2})(?:th|st|nd|rd)?\s+(?:of\s+)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)'
        pattern2 = r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:of\s+)?(\d{1,2})(?:th|st|nd|rd)?'
        pattern3 = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\s+(?:of\s+)?(\d{1,2})(?:th|st|nd|rd)?'
        match = re.search(pattern, date_string, re.IGNORECASE)
        match1 = re.search(pattern1, date_string, re.IGNORECASE)
        match2 = re.search(pattern2, date_string, re.IGNORECASE)
        match3 = re.search(pattern3, date_string, re.IGNORECASE)
        if match:
            day = match.group(1)
            month = match.group(2)
            month_number = str(list(calendar.month_abbr).index(month[:3].title())).zfill(2)
            dd_mm_date = f"{day.zfill(2)}-{month_number}"
            return dd_mm_date
        elif match1:
            day = match1.group(1)
            month = match1.group(2)
            month_number = str(list(calendar.month_abbr).index(month[:3].title())).zfill(2)
            dd_mm_date = f"{day.zfill(2)}-{month_number}"
            return dd_mm_date
        elif match2:
            day = match2.group(2)
            month = match2.group(1)
            month_number = str(list(calendar.month_abbr).index(month[:3].title())).zfill(2)
            dd_mm_date = f"{day.zfill(2)}-{month_number}"
            return dd_mm_date
        elif match3:
            day = match3.group(2)
            month = match3.group(1)
            month_number = str(list(calendar.month_abbr).index(month[:3].title())).zfill(2)
            dd_mm_date = f"{day.zfill(2)}-{month_number}"
            return dd_mm_date
        else:
            # print("Date not found in the given string")
            return date_string
    except ValueError:
        # print("Invalid date format")
        return date_string

number_mapping = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000,
    'trillion': 1000000000000,
}

def convert_number_name_to_integer(number_name):
    words = number_name.split()
    total = 0
    current = 0
    lis=[]
    for l in number_mapping:
      lis.append(str(l))
    for word in words:
        if word in lis:
            current += number_mapping[word]
        elif word == 'and':
            continue
        else:
            multiplier = number_mapping[word]
            total += current * multiplier
            current = 0
    return total + current



def convert_to_canonical_date(match):
    """
    Given a match object, convert the date to the canonical form YYYY-MM-DD
    """
    for date_str in match.groups():
        if date_str is not None:
            date_str = date_str.replace("/", "-")  # replace slashes with hyphens
            parts = date_str.split("-")
            if len(parts[2]) == 2:  # two-digit year
                parts[2] = "20" + parts[2] if int(parts[2]) > 21 else "19" + parts[2]  # assume 20xx for years > 21, else 19xx
            return "-".join([parts[2], parts[1].zfill(2), parts[0].zfill(2)])  # return canonical date in the format YYYY-MM-DD

def convert_dates_to_canonical(text):
    """
    Given a text, convert all dates in the text to the canonical form YYYY-MM-DD
    """
    return date_regex.sub(convert_to_canonical_date, text)

# 1 to 2

time_regex_1 = re.compile(r"(\d{1,2})(:|.)(\d{2})\s*(AM|PM|am|pm)?")
time_regex_2 = re.compile(r"(\d{2})(:|.)(\d{2})")

def convert_time_to_canonnical(time_str):
  match = time_regex_1.search(time_str)
  if match==None:
     return time_str
  # Extract hour, minute, and AM/PM from the match object
  hour, minute, am_pm = match.group(1), match.group(3), match.group(4)

  # Convert hour to 24-hour format
  if (am_pm == "PM" or am_pm == "pm") and hour != "12":
      hour = str(int(hour) + 12)
  elif (am_pm == "AM" or am_pm == "am") and hour == "12":
      hour = "00"

  # Concatenate hour and minute to form time in the format of time_regex_2
  time_str_regex_2 = f"{hour.zfill(2)}:{minute}"
  # print(time_str_regex_2)
  return(str(time_str_regex_2)) # Output: 17:30

def convert(actual, pred):
  c=0
  cnt=0
  actual=str(actual)
  pred=str(pred)
  actual=actual.lower()
  pred=pred.lower()
  if actual==pred:
    cnt+=1
    c+=1
    return actual, pred
  else:
    try:
      actual=convert_number_name_to_integer(actual)
    except:
      pass
    try:
      pred=convert_number_name_to_integer(pred)
    except:
      pass
    # print(actual)
    # print(pred)
    actual=str(actual)
    pred=str(pred)
    actual=actual.replace("\"","")
    pred=pred.replace("\"","")
    actual = re.sub(r'(\w)\.', r'\1', actual)
    pred = re.sub(r'(\w)\.', r'\1', pred)
    actual_timec=convert_time_to_canonnical(actual)
    predicted_timec=convert_time_to_canonnical(pred)
    if actual_timec==predicted_timec and actual_timec != None:
      cnt+=1
      pred=actual
    else:
      if pred in actual:
        # print(actual)
        # print(pred)
        # print()
        actual=pred
        cnt+=1
      elif actual in pred:
        # print(actual)
        # print(pred)
        pred=actual
        cnt+=1
      else:
        numeric_part_actual = re.findall(r'\d+', actual)
        numeric_part_pred = re.findall(r'\d+', pred)
        if numeric_part_actual==numeric_part_pred:
          cnt+=1
        else:
          # pass
          if convert_date_to_dd_mm(actual)==convert_date_to_dd_mm(pred):
            cnt+=1
            actual=convert_date_to_dd_mm(actual)
            pred=actual
  return actual,pred
def f1_score(reference_answer, predicted_answer):
    reference_answer=str(reference_answer)
    predicted_answer=str(predicted_answer)
    reference_tokenized = set(reference_answer.lower().split())
    predicted_tokenized = set(predicted_answer.lower().split())
    intersection = reference_tokenized & predicted_tokenized
    # print(reference_answer)
    # print(predicted_answer)
    precision = len(intersection) / len(predicted_tokenized)
    recall = len(intersection) / len(reference_tokenized)
    if precision + recall == 0:
        return 0
    f1 = 2 * precision * recall / (precision + recall)
    return f1

# Define a function to calculate exact match score
def exact_match_score(reference_answer, predicted_answer):
    reference_answer=str(reference_answer)
    predicted_answer=str(predicted_answer)
    reference_tokenized = reference_answer.lower().split()
    predicted_tokenized = predicted_answer.lower().split()
    return reference_tokenized == predicted_tokenized

def get_rouge_scores(predicted_answer, actual_answer):
  actual_answer=str(actual_answer)
  predicted_answer=str(predicted_answer)
  scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
  scores = scorer.score(predicted_answer, actual_answer)
  return scores

def get_f1(df, c1, c2):
  f=0
  for i in df.index:
    f+=f1_score(df[c2][i], df[c1][i])
  return f/len(df)

def get_rouge(df, c1, c2):
  r1=0
  rl=0
  for i in df.index:
    r1+=get_rouge_scores(df[c2][i], df[c1][i])['rouge1'][2]
    rl+=get_rouge_scores(df[c2][i], df[c1][i])['rougeL'][2]
  return r1/len(df), rl/len(df)

def get_exact_match(df, c1, c2):
  f=0
  for i in df.index:
    f+=exact_match_score(df[c2][i], df[c1][i])
  return f/len(df)

def calculate_meteor_score(reference, candidate):
    # Tokenize the reference and candidate sentences
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()

    # Calculate the METEOR score
    score = meteor_score.meteor_score([reference_tokens], candidate_tokens)

    # Return the METEOR score
    return score

# Example usage
def get_meteor(df, c1, c2):
  meteor_score=0
  for i in df.index:
    meteor_score += calculate_meteor_score(str(df[c1][i]), str(df[c2][i]))
  meteor_score/=len(df)
  return meteor_score

squad_v2_metric = load("squad_v2")

def get_squad_v2_metric(df, c1, c2):
  predictions = []
  for i , pred in enumerate(list(df[c2])):
    predictions.append({"prediction_text" : pred , "id" : str(i), 'no_answer_probability': 0.})

  references = []
  for i , act in enumerate(list(df[c1])):
    references.append({'answers' : {'answer_start': [0], 'text': [act]}, 'id': str(i)})

  results = squad_v2_metric.compute(predictions=predictions, references=references)
  results
  return results

PATH=sys.argv[1]
df=pd.read_csv(PATH)

if str(sys.argv[2])=='0':
  if len(df)!=0:
    squad = get_squad_v2_metric(df, 'actual_answer', 'predicted_answer')
    print('exact match score: ',squad['exact'])
    print('f1 score: ', squad['f1'])
    print('rouge score: ', get_rouge(df, 'actual_answer', 'predicted_answer'))
    print('meteor score: ', get_meteor(df, 'actual_answer', 'predicted_answer'))

  else:
    print('empty dataframe')
else:
  if len(df)!=0:
    actual=[]
    pred=[]
    for i in df.index:
        a,p=convert(df['actual_answer'][i], df['predicted_answer'][i])
        actual.append(a)
        pred.append(p)
    df['conv_actual_answer']=actual
    df['conv_predicted_answer']=pred

    squad = get_squad_v2_metric(df, 'conv_actual_answer', 'conv_predicted_answer')
    rouge = get_rouge(df, 'conv_actual_answer', 'conv_predicted_answer')
    met = get_meteor(df, 'conv_actual_answer', 'conv_predicted_answer')
    print('exact match score: ',squad['exact'])
    print('f1 score: ', squad['f1'])
    print('rouge score: ', rouge)
    print('meteor score: ', met)
    print(str(squad['f1'])+'\t'+str(squad['exact'])+'\t'+str(rouge[0])+'\t'+str(rouge[1])+'\t\t\t'+str(met))
  else:
    print('empty dataframe')

