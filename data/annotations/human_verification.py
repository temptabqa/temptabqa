import ast
import re

df_t = {
    "gold_answer" : ["23 years"],
    "answers" : ["[\"23\", \"23 year\", \"23 years\"]"]
}

def categorical_to_numeric(text):
  categorical_to_numeric = {
                            "one":1,
                            "two":2,
                            "three":3,
                            "four":4,
                            "five":5,
                            "six":6,
                            "seven":7,
                            "eight":8,
                            "nine":9,
                            "ten":10,
                           }
  for key,value in zip(categorical_to_numeric.keys(),categorical_to_numeric.values()):
    text = re.sub(str(key),str(value),text)

  return text

corrected_answer = []
corrected_gold_answer = []
majority_answer = []
scores = []
k = 0

for answer in df_t["gold_answer"]:
    answer = answer.lower()
    answer = answer.strip()
    answer = answer.replace("\"","")
    answer = answer.replace("~","")
    answer = answer.replace("#","")
    answer = answer.replace("%","")
    answer = answer.replace(">","")
    answer = answer.replace("+","")
    answer = answer.replace("us$","")
    answer = answer.replace("usd$","")
    answer = answer.replace("$","")
    answer = re.sub(r'\.$', '', answer)
    answer = re.sub(r'^\.', '', answer)
    answer = categorical_to_numeric(answer)
    answer = re.sub(r' (\()(.*)(\))$',r'',answer)
    answer = re.sub(r'(\d)(rd|th|st|nd)',r'\1',answer)

    answer = re.sub(r'^(almost |over |after |in or before |at age |in the year |at the age of |age |age of |he was )?(\d+)( active)? (gold |bronze |silver )?(goal|vehicle|win|race|episode|single|langley|album|team|hurricane|time|year|month|day|week|month|season|medal|minute|hour|second)(s)?(( ago)|( old)|( longer)|( almost)|( after))?(.)?$', r'\2', answer)
    answer = re.sub(r'^(at least|at the age of |after the age of |nearly |age of )(\d+)$',r'\2',answer)
    answer = re.sub(r'^(bronze|gold|silver) (medal)$ ',r'\2',answer)
    corrected_gold_answer.append(answer)

i = 0
for x in df_t["answers"]:
  if type(x)!=type(""):
    x="[]"
  x = ast.literal_eval(x)
  answer_updated = []


  for answer in x:

    answer = answer.lower()
    answer = answer.strip()
    answer = answer.replace("\"","")
    answer = answer.replace("~","")
    answer = answer.replace("#","")
    answer = answer.replace("%","")
    answer = answer.replace(">","")
    answer = answer.replace("+","")
    answer = answer.replace("us$","")
    answer = answer.replace("usd$","")
    answer = answer.replace("$","")
    answer = re.sub(r'\.$', '', answer)
    answer = re.sub(r'^\.', '', answer)
    answer = categorical_to_numeric(answer)
    answer = re.sub(r'(\d)(rd|th|st|nd)',r'\1',answer)

    answer = re.sub(r'^(over |after |in or before |at age |in the year |at the age of |age |age of |he was )?(\d+)( active)? (gold |bronze |silver )?(episode|single|langley|album|team|hurricane|time|year|month|day|week|month|season|medal|minute|hour|second)(s)?(( ago)|( old)|( longer)|( almost)|( after))?(.)?$', r'\2', answer)
    answer = re.sub(r'^(bronze|gold|silver) (medal)$ ',r'\2',answer)

    if " " + corrected_gold_answer[i] + " " in answer:
      answer = corrected_gold_answer[i]

    if " " + corrected_gold_answer[i] + "," in answer:
      answer = corrected_gold_answer[i]

    if " " + corrected_gold_answer[i] + ". " in answer:
      answer = corrected_gold_answer[i]

    for w in [" ", ",","-year","-minute"]:
      if answer.startswith(corrected_gold_answer[i] + w):
        answer = corrected_gold_answer[i]

    if answer.endswith(" " + corrected_gold_answer[i]):
      answer = corrected_gold_answer[i]

    if answer != corrected_gold_answer[i]:
      if corrected_gold_answer[i] in answer:
        alter_answer = re.sub(r'.*(\()(.*)(\))$',r'\2',answer)
        if alter_answer != answer:
          if alter_answer == corrected_gold_answer[i]:
            answer = corrected_gold_answer[i]

    answer_updated.append(answer)

  corrected_answer.append(answer_updated)
  set_answer = set(answer_updated)
  majority = 1
  if len(answer_updated) > 0:
    majority_answ = answer_updated[0]
  else:
    majority_answ = ""

  for z in set_answer:
    y = answer_updated.count(z)
    if majority < y:
      majority = y
      majority_answ = z

  majority_answer.append(majority_answ)
  scores.append(majority)

df_t["scores"] = scores
df_t["corrected_answer"] = corrected_answer
df_t["corrected_gold_answer"] = corrected_gold_answer
df_t["majority_answer"] = majority_answer