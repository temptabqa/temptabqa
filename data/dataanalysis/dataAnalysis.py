import pandas as pd
import re
PATH='./maindata/qapairs/train-set/train-set.csv'
def max_operator(question):
  max_related = ['max', 'maximum', 'highest', 'most']
  max_regex = r".*((" + ')|('.join(max_related) + ")).*"
  q = question.lower()
  if re.match(max_regex, q):
      return True
  return False
def min_operator(question):
  min_related = ['min', 'minimum', 'least', 'lowest']
  min_regex = r".*((" + ')|('.join(min_related) + ")).*"
  q = question.lower()
  if re.match(min_regex, q):
      return True
  return False
def count_operator(question):
  count_related = ['how many', 'frequency', 'count']
  count_regex = r".*((" + ')|('.join(count_related) + ")).*"
  q = question.lower()
  if re.match(count_regex, q):
      return True
  return False
def sum_operator(question):
  sum_related = ['sum', 'add', 'total','aggregate']
  sum_regex = r".*((" + ')|('.join(sum_related) + ")).*"
  q = question.lower()
  if re.match(sum_regex, q):
      return True
  return False
def difference_operator(question):
  diff_related = ['difference', 'subtract', 'change', 'delta', 'increase', 'decrease']
  diff_regex = r".*((" + ')|('.join(diff_related) + ")).*"
  q = question.lower()
  if re.match(diff_regex, q):
      return True
  return False
def average_operator(question):
  avg_related = ['avg', 'average', 'mean', 'median', 'mode',' net ', 'fair value']
  avg_regex = avg_regex = r".*((" + ')|('.join(avg_related) + ")).*"
  q = question.lower()
  if re.match(avg_regex, q):
      return True
  return False
def comparison_operator(question):
  com_related = ['higher', 'lower', 'more', 'less', 'bigger', 'smaller', 'larger', 'lesser','exceed']
  com_regex = r".*((" + ')|('.join(com_related) + ")).*"
  q = question.lower()
  if re.match(com_regex, q):
      return True
  return False

def yes_no(question,answer):
  answer = answer.lower()
  question = question.lower()

  regex_explicit_temporal_list = [
      #6/6/9089   or  2020/20 or 6-6-9089 or 2020-90
      "((\d{2}|\d)(/|-)(\d{2}|\d)(/|-)(\d{2})|(\d{4}(/|-)\d{2}))",

      #in the* year* may* 2022
      '(both )*(the )*(year )*(jan(?:uary)|feb(?:ruary)|mar(?:ch)|apr(?:il)|may|jun(?:e)|jul(?:y)|aug(?:ust)|sep(?:tember)|oct(?:ober)|nov(?:ember)|dec(?:ember))*\s*\d{4}',

      # 28/null (F/f)eb/(F/f)eburary 2022/22
      '(\d{2}|\d)*\s*((J|j)an(?:uary)|(F|f)eb(?:ruary)|(M|m)ar(?:ch)|(A|a)pr(?:il)|(M|m)ay|(J|j)un(?:e)|(J|j)ul(?:y)|(A|a)ug(?:ust)|(S|s)ep(?:tember)|(O|o)ct(?:ober)|(N|n)ov(?:ember)|(D|d)ec(?:ember))\s+(\d{4}|\d{2})',

      #5, 2002
      "\d(th)*, \d{4}",

      # \d+ year/years
      '\d+(th)* (year|day|week|month|hour|century|second|minute|hour)',

      #may 6,1987 or may 6 1986
      "((J|j)an(?:uary)|(F|f)eb(?:ruary)|(M|m)ar(?:ch)|(A|a)pr(?:il)|(M|m)ay|(J|j)un(?:e)|(J|j)ul(?:y)|(A|a)ug(?:ust)|(S|s)ep(?:tember)|(O|o)ct(?:ober)|(N|n)ov(?:ember)|(D|d)ec(?:ember)) \d+(th)*(,|\s)\d+",

      #1789's
      "\d{4}('s|s)",

      #28 jan or jan 28
      '(\d{2}|\d|date)(th)*\s*(of|-)*\s*((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?)',
      '((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?)(-|\s+)(\d)',

      #1980 winter
      "((\d+ (winter|summer|autumn|spring))|((summer|winter|autumn|spring) \d+))",

      #january
      "january|february|march|april|may|june|july|august|september|october|november|december",

      #night
      "night|morning|evening|midnight|noon|sunset|afternoon|daylight|winter|summer|autumn|spring",

  ]

  for i in range(len(regex_explicit_temporal_list)):
    regex_explicit_temporal_list[i] = "(in " + regex_explicit_temporal_list[i] + " )?(did|is|was|were|are|does|has|have).*"
  regex_explicit_temporal = re.compile('|'.join(regex_explicit_temporal_list))

  if re.match(r".*(yes or no)|(true/false)|(false/true)|(true or false)|(false or true).*",question):
    return True
  else:
    if re.match(regex_explicit_temporal,question):
      if re.match(r"(.* or .*)|(.*[a-z]/[a-z].*)",question) :
        if re.match(r".* or( |.* )not.*",question) or re.match(r".*(yes or no)|(true/false)|(false/true)|(true or false)|(false or true).*",question):
          return True
      else:
        return True

  if answer == 'yes' or answer == 'no' or answer == 'true' or answer == 'false':
    return True

  return False

def before_related(question):
  before_related = ['before', 'previous to','prior to', 'preceding','past','earlier','ago ',' last ']
  before_regex = r".*((" + ')|('.join(before_related) + ")).*"
  if re.match(before_regex, question):
    return True
  return False

def after_related(question):
  after_related = ['after ', 'following','followed by','later']
  after_regex = r".*((" + ')|('.join(after_related) + ")).*"
  if re.match(after_regex, question):
    return True
  return False

def duration_related(question):
  duration_related = ['between','during','meanwhile','how long','longer','since','until','from.*and']
  duration_regex = r".*((" + ')|('.join(duration_related) + ")).*"
  if re.match(duration_regex, question) or (re.match(".*last.*", question) and not re.match(".* last .*", question)) or re.match(".*how many ((total|active|more|calendar) )?(year|day|season|month|decade|week|hour|century).*",question):
    return True
  return False

def explicit(question):
  year_number0 = r".*(/| |,)*\d{4}('|s|\?| )*.*"
  year_number1 = r"\d{4}('|s)* .*"

  #jan
  month_key = r'.*(january|february|march|april|may|june|july|august|september|october|november|december) .*'

  #day
  day_key = r".*(mon|tues|wednes|thurs|fri|sat|sun)day.*"

  #6/6/9089   or  2020/20 or 6-6-9089 or 2020-90
  date_pattern = r".*((\d{2}|\d)(/|-)(\d{2}|\d)(/|-)(\d{2})|(\d{4}(/|-)\d{2})).*"

  # 01:01:01/01:01
  time_pattern = r".*(\d+|(\d+.\d+))(:(\d+|(\d+.\d+)))+.*"

  # 5 bc/ad
  bc_ad = ".*\d (bc|ad).*"

  # -- time --
  time_keyword0 = r".*(longer|longest|faster|slower|highest|lower|higher|lowest|slowest|fastest|shortest|shorter|what|difference|at the|top|consecutive|least|most|less|more|finish)\s*((between|the|in|was|total|than|amount|of|a|\d+)\s)*\s*time.*"
  time_keyword1 = r".*time\s*(of|is)*\s*(difference|more|less|more|less|above|below|quicker|faster|slower|( .*\d+.*)).*"

  temporal_keywords = ".*(decade|season|year|day|week|month|hour|century|minute).*"

  explicit_question_pattern_list = [
                                    year_number0,
                                    year_number1,
                                    month_key,
                                    day_key,
                                    date_pattern,
                                    time_pattern,
                                    time_keyword0,
                                    time_keyword1,
                                    temporal_keywords,
                                    bc_ad
  ]
  explicit_question_pattern = re.compile( '|'.join(explicit_question_pattern_list))

  if re.match(explicit_question_pattern, question):
    return True

  return False

def implicit(question):
  return not explicit(question)

def ordinal(question):
  ordinal_keywords = ['first','last ','second','third','fourth','fifth','sixth','seventh','eighth','ninth']
  ordinal_question_pattern = ".*((" + ')|('.join(ordinal_keywords) + ")).*"

  if re.match(".*\d(st|nd|rd|th).*", question) and not (re.match(".*\d(st|nd|rd|th)(.{1,15}\d{4}| century).*",question) or re.match(".*(january|february|march|april|may|june|july|august|september|october|november|december).{1,10}\d(st|nd|rd|th).*",question)) :
    return True
  if re.match(ordinal_question_pattern, question):
    return True
  if re.match(".* rank.*",question):
    return True

  return False


def temporal_answer(question,answer):
  #6/6/9089   or  2020/20 or 6-6-9089 or 2020-90
  date_pattern0 = r".*((\d{2}|\d)(/|-)(\d{2}|\d)(/|-)(\d{2})|(\d{4}(/|-)\d{2})).*"

  #jan
  month_key = r'.*(january|february|march|april|may|june|july|august|september|october|november|december) .*'

  #day
  day_key = r".*(mon|tues|wednes|thurs|fri|sat|sun)day.*"

  temporal_keywords = ".*(decade|season|year|day|week|month|hour|century|minute).*"

  #in the* year* may* 2022
  date_pattern1 = r'.*in (the)*\s*(year)*\s*((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?)*\s*\d{4}.*'

  #from/between year to year
  date_pattern3 = r'.*(from|between)\s*(the years of)*\s*\d{4}\s*(to|and|-)\s*\d{4}.*'

  #5, 2002
  date_pattern4 = r".*\d(th)*, \d{4}.*"

  # before/after
  date_pattern7 = r'.*(before|after|at the|of|since|as early as) \d{4}.*'

  #may 6,1987 or may 6 1986
  date_pattern8 = r".*((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?) \d+(th)*(,|\s)\d+.*"

  #1789's
  date_pattern9 = r".*\d{4}('s|s).*"

  #28 jan or jan 28
  date_pattern10 = r'.*(\d{2}|\d|date)(th)*\s*(of)*\s*((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?) .*'
  date_pattern11 = r'.*((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?)\s+(\d).*'

  #1980 winter
  date_pattern12 = r".*((\d+ (winter|summer|autumn|spring))|((summer|winter|autumn|spring) \d+)).*"

  # 01:01:01/01:01
  time_pattern = r".*(\d+|(\d+.\d+))(:(\d+|(\d+.\d+)))+.*"

  # -- time --
  time_keyword0 = r".*(longer|longest|faster|slower|highest|lower|higher|lowest|slowest|fastest|shortest|shorter|what|difference|at the|top|consecutive|least|most|less|more|finish)\s*((between|the|in|was|total|than|amount|of|a|\d+)\s)*\s*time.*"
  time_keyword1 = r".*time\s*(of|is)*\s*(difference|more|less|more|less|above|below|quicker|faster|slower|( .*\d+.*)).*"

  #2022 , 2022-    #answer
  year_pattern = r'(^\s*\d{4}[^\d])|(^\s*\d{4}\s*$)'

  answer_pattern_list= [
                        time_pattern,
                        month_key,
                        day_key,
                        temporal_keywords,
                        time_pattern,
                        date_pattern0,
                        date_pattern1,
                        date_pattern3,
                        date_pattern4,
                        date_pattern7,
                        date_pattern8,
                        date_pattern9,
                        date_pattern10,
                        date_pattern11,
                        date_pattern12,
                        time_keyword0,
                        time_keyword1
                      ]

  answer_pattern = re.compile( '|'.join(answer_pattern_list))

  if re.match(answer_pattern, answer):
    return True

  if re.match(".*((around|in|during|from|at) )?(what|which) ((was|is) the )?((last|first|final|only|release|birth) )?(two )?(olympics )?year.*",question):
    return True

  if re.match(year_pattern,answer) and re.match("(when|(what|which) ((youth|winter) )?olympic).*",question):
    return True

  if re.match("how soon.*",question):
    return True

  return False

def count_answer(question,answer):
  if re.match(".*how many.*",question):
    return True

  if re.match(".*number of.*",question) and re.match(".*\d.*",answer):
    return True

  return False

def age_cardinal_answer(question,answer):
  if re.match("(((at )?(what|which) ((was|is) (the )?)?age)|(how old)).*",question) or re.match(".* age( of)?\?",question):
    return True

  return False

def money_answer(question,answer):
  if re.match(".*[$|€].*",answer):
    return True

  if re.match(".*(trillion|billion|million).*",answer) and re.match(".*(import|export|stock|dollar|budget|gross|money|gpd|gdp|revenue|income|cost).*",question):
    return True

  if re.match("what ((was|is) the )?((annual|nominal|total|operating|estimated|construction) )?(import|export|stock|dollar|budget|gross|money|gpd|gdp|revenue|income|cost)",question):
    return True

  return False

def percentage_answer(question,answer):
  if re.match("(what|how much) ((was|is) the )?(difference in )?percent",question):
    return True

  if re.match(".*%.*",answer):
    return True

  return False

def rank_answer(question,answer):
  if re.match(".*where.*",question) and re.match(".*rank.*",question):
    return True

  if re.match("what (is|was)( the )?.{0,30} rank.*",question):
    return True

  if re.match(".*\d(st|nd|rd|th)( place)?$",answer) or re.match(".*(place|spot).*",answer):
    return True

  return False

def italian_months_to_english(text):
  italian_months_to_english = {
                        "gennaio" : "january",
                        "febbraio": "february",
                        "marzo" : "march",
                        "aprile" : "april",
                        "maggio" : "may",
                        "giugno" :  "june",
                        "luglio" : "july",
                        "agosto" : "august",
                        "settembre" : "september",
                        "ottobre" : "october",
                        "novembre" : "november",
                        "dicembre" : "december",
                       }


  for key,value in zip(italian_months_to_english.keys(),italian_months_to_english.values()):
    text = re.sub(str(key),str(value),text)

  return text

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
                            "sept":"september",
                            "novemeber":"november",
                           }
  for key,value in zip(categorical_to_numeric.keys(),categorical_to_numeric.values()):
    text = re.sub(str(key),str(value),text)

  return text


def analyse_answer(question,answer):
  answer = answer.lower()
  question = question.lower()
  answer = categorical_to_numeric(answer)

  # #yes/no
  if yes_no(question,answer):
    return "YES/NO"

  #date and time
  if temporal_answer(question,answer):
    return "TEMPORAL"
  #cardinal
  ##count
  if count_answer(question,answer):
    return "COUNT"
  ##age
  if age_cardinal_answer(question,answer):
    return "AGE"

  ##money
  if money_answer(question,answer):
    return "MONEY"

  ##percentage
  if percentage_answer(question,answer):
    return "PERCENTAGE"

  #ordinal answer
  if rank_answer(question,answer):
    return "ORDINAL"

  #place country|continent|city|cities|countries|province|capital
  if re.match("((on|in|with|against|for) )?(who|which|what) ((was|is) the )?((last|first|modern|present day|defunct|largest|other|(name (of )?the)|two) )?(country|continent|city|cities|countries|province|capital|location)",question):
    return "PLACE"
  if re.match(".*where.*",question) and not re.match(".*rank.*",question):
    return "PLACE"

  #person
  if re.match("who.*",question):
    return "PERSON"

  #organization  club|team|university|universities
  if re.match("((on|in|with|against|for) )?(who|which|what) ((was|is) the )?((last|first|second|third|modern|present day|defunct|largest|other|(name (of the)?(of)?(the)?)) )?((two|most recent|youth|national|professional|senior|domestic) )?((year|club) )?.{0,4}(club|team|university|universities|college).*",question):
    return "ORGANIZATION"

  #product  medal|color
  if re.match("(what|which) ((was|is) the )?((last|first|main) )?(medal|color)",question):
    return "PRODUCT"

  return "UNKNOWN"


df=pd.read_csv(PATH)
df['explicit'] = df['question'].apply(lambda q: explicit(q))
df['implicit'] = df['question'].apply(lambda q: implicit(q))
df['before_related'] = df['question'].apply(lambda q: before_related(q))
df['after_related'] = df['question'].apply(lambda q: after_related(q))
df['duration_related'] = df['question'].apply(lambda q: duration_related(q))
df['max_operator'] = df['question'].apply(lambda q: max_operator(q))
df['min_operator'] = df['question'].apply(lambda q: min_operator(q))
df['count_operator'] = df['question'].apply(lambda q: count_operator(q))
df['sum_operator'] = df['question'].apply(lambda q: sum_operator(q))
df['difference_operator'] = df['question'].apply(lambda q: difference_operator(q))
df['average_operator'] = df['question'].apply(lambda q: average_operator(q))
df['comparison_operator'] = df['question'].apply(lambda q: comparison_operator(q))
df['ordinal'] = df['question'].apply(lambda q: ordinal(q))
answer_types=[]
for i in df.index:
  answer_types.append(analyse_answer(df['question'][i], df['answer'][i]))
df['answer_type'] = answer_types

df.to_csv(PATH[:-4]+'_analysis.csv')

  