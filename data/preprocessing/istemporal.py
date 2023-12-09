import re

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

def text_lowercase(text):
    return text.lower()

def text_preprocess(text):
  if text == "":
    return text

  text = text_lowercase(text)
  text = categorical_to_numeric(text)
  text = italian_months_to_english(text)

  return text

before_related = ["yesterday","previous to","prior to","soon before"]
after_realated = ["tomorrow","since","soon after"]
during_related = ['when at the time']
now_related = [" now","currently",'at the same time',"daily","recently","recent"]
past_related = ["earlier","in the past"]
begin_related = ["at the beginning"]


temporal_keywords = before_related + after_realated + during_related + now_related + past_related + begin_related
temporal_keyword_regex = r".*((" + ')|('.join(temporal_keywords) + ")).*"
#6/6/9089   or  2020/20 or 6-6-9089 or 2020-90
date_pattern0 = r".*((\d{2}|\d)(/|-)(\d{2}|\d)(/|-)(\d{2})|(\d{4}(/|-)\d{2})).*"

#in the* year* may* 2022
date_pattern1 = r'.*in (both )*(the )*(year )*(jan(?:uary)|feb(?:ruary)|mar(?:ch)|apr(?:il)|may|jun(?:e)|jul(?:y)|aug(?:ust)|sep(?:tember)|oct(?:ober)|nov(?:ember)|dec(?:ember))*\s*\d{4}.*'

# 28/null (F/f)eb/(F/f)eburary 2022/22
date_pattern2 = r'(\d{2}|\d)*\s*((J|j)an(?:uary)|(F|f)eb(?:ruary)|(M|m)ar(?:ch)|(A|a)pr(?:il)|(M|m)ay|(J|j)un(?:e)|(J|j)ul(?:y)|(A|a)ug(?:ust)|(S|s)ep(?:tember)|(O|o)ct(?:ober)|(N|n)ov(?:ember)|(D|d)ec(?:ember))\s+(\d{4}|\d{2}).*'

#from/between year to year
date_pattern3 = r'.*(from|between)\s*((the years of)|(the))*\s*\d{4}\s*(to|and|-)\s*\d{4}.*'

#5, 2002
date_pattern4 = r".*\d(th)*, \d{4}.*"

# \d+ year/years
date_pattern5 = r'.*\d+(th)* (year|day|week|month|hour|century|second|minute|hour).*'
#year \d+
date_pattern6 = r'.*(year|day|week|month|hour|century|second|minute|hour)(s)* \d+.*'

# before/after
date_pattern7 = r'.*(before|after|at the|of|since|as early as|through|unitl) (\d{4}).*'

date_pattern15 = r".*(as|of the|from|around|the|for|by) (((18|19)\d{2})|(2\d{3})) .*"

#may 6,1987 or may 6 1986
date_pattern8 = r".*((J|j)an(?:uary)|(F|f)eb(?:ruary)|(M|m)ar(?:ch)|(A|a)pr(?:il)|(M|m)ay|(J|j)un(?:e)|(J|j)ul(?:y)|(A|a)ug(?:ust)|(S|s)ep(?:tember)|(O|o)ct(?:ober)|(N|n)ov(?:ember)|(D|d)ec(?:ember)) \d+(th)*(,|\s)\d+.*"

#1789's
date_pattern9 = r".*\d{4}('s|s).*"

#28 jan or jan 28
date_pattern10 = r'.*(\d{2}|\d|date)(th)*\s*(of|-)*\s*((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?) .*'
date_pattern11 = r'.*((J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|(N|n)ov(?:ember)?|(D|d)ec(?:ember)?)(-|\s+)(\d).*'

#1980 winter
date_pattern12 = r".*((\d+ (winter|summer|autumn|spring))|((summer|winter|autumn|spring) \d+)).*"

#around 1980
date_pattern13 = r".*(((around|season|from|to|during|which|until|by|early|late) \d{4}(\?| ))|( \d{4} ((pre-)?season|election))).*"

#1980 - 1987
# date_pattern14 = r".*\d{4} .* \d{4}.*"

# 01:01:01/01:01
time_pattern = r".*(\d+|(\d+.\d+))(:(\d+|(\d+.\d+)))+.*"

#pm/am
date_pattern16 = r".*\d\s*(pm|am).*"

#which \d4 \d4
date_pattern17 = r".*which.* (18|19|20)\d{2}.* (18|19|20)\d{2}.*"

#1980-present
date_pattern18 = r".*\d{4}-present.*"

# -- time --
time_keyword0 = r".*(longer|longest|faster|slower|highest|lower|higher|lowest|slowest|fastest|shortest|shorter|what|difference|at the|top|consecutive|least|most|less|more|finish)\s*((between|the|in|was|total|than|amount|of|a|\d+)\s)*\s*time.*"
time_keyword1 = r".*time\s*(of|is)*\s*(difference|more|less|more|less|above|below|quicker|faster|slower|( .*\d+.*)).*"

#january
months = r".*(((J|j)anuary)|((F|f)ebruary)|((M|m)arch)|((A|a)pril)|((M|m)ay)|((J|j)une)|((J|j)uly)|((A|a)ugust)|((S|s)eptember)|((O|o)ctober)|((N|n)ovember)|((D|d)ecember)).*"

#monday
days = r".*((M|m)onday|(T|t)uesday|(W|w)ednesday|(t|T)hursday|(f|F)riday|(S|s)aturday|(S|s)unday).*"

#temporal year(year|day|week|month|hour|century|second|minute|hour)
temporal_year0 = r".*(what|which|how many|consecutive).*(decade|season|year|day|week|month|hour|century|second|minute|hour|time).*"
temporal_year1 = r".*(same|last|first|this|only|number of|in|per|that|each|more|less)( the)? (decade|season|year|day|week|month|hour|century|second|minute|hour|time).*"
temporal_year2 = r".*(decade|season|year|day|week|month|hour|century|second|minute|hour|time)(s)* (before|after).*"

#released
album_released = r".*((came\s*(in)*\s*(first|last))|(released\s*(album|single)*\s*(first|last|earliest))|((first|last|earliest)\s*(album|single)*\s*(that was)*\s*released)).*"

#2022 , 2022-    #answer
# year_pattern = r'(^\s*\d{4}[^\d])|(^\s*\d{4}\s*$)'

#fiscal 1980 for tatqa and finqa
financial_pattern = r".*fiscal \d{4}.*"

proper_noun_olympics = [
    "afc",
    "fifa",
    "eaff",
    "eurobasket",
    "olympic",
    "fiba",
    "brazilian football team",

    "film",
    "movie"
    "battle",
    "revenue",
    "population",
    "census",
]
proper_noun_olympics_regex = r".*\d{4} ((" + ')|('.join(proper_noun_olympics) + ")).*"

keyword_time = [
    ".*year.*",
    "now( |,).*"
]
keyword_time_regex = '(' + ')|('.join(keyword_time) + ')'

times_of_day = [
    "night",
    "evening",
    "morning",
    "midnight",
    "dawn",
    "sunrise",
    "midday",
    "noon",
    "sunset",
    "afternoon",
    "daylight",
    "winter",
    "summer",
    "autumn",
    "spring"
]
times_of_day_regex = r".*(before|after|at|of|since|as early as|through|until|this|for)( the)? ((" + ')|('.join(times_of_day) + "))( |,|\?).*"

months_name = [
    "january",
    "feburary",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december"
]

answer_pattern_list= [
                      proper_noun_olympics_regex,
                      time_pattern,
                      months,
                      date_pattern0,
                      date_pattern2,
                      date_pattern4,
                      date_pattern5,
                      date_pattern6,
                      date_pattern8,
                      date_pattern10,
                      date_pattern11,
                      date_pattern12,
                      date_pattern18
                      ]
answer_pattern = re.compile( '|'.join(answer_pattern_list))

question_pattern_list = [
                         financial_pattern,
                         times_of_day_regex,
                         proper_noun_olympics_regex,
                         keyword_time_regex,
                         album_released,
                         time_pattern,
                         months,
                         days,
                         time_keyword0,
                         time_keyword1,
                         temporal_year0,
                         temporal_year1,
                         temporal_year2,
                         date_pattern0,
                         date_pattern1,
                         date_pattern2,
                         date_pattern3,
                         date_pattern4,
                         date_pattern5,
                         date_pattern6,
                         date_pattern7,
                         date_pattern8,
                         date_pattern9,
                         date_pattern10,
                         date_pattern11,
                         date_pattern12,
                         date_pattern13,
                         date_pattern15,
                         date_pattern16,
                         date_pattern17,
                         date_pattern18,
                         ]
question_pattern = re.compile( '|'.join(question_pattern_list))

answer_question = [
    [["when.*",".*year.*"],["\d{4}"]],
]

def is_temporal(question,answer):
  if re.match(question_pattern,question):
    return True

  elif re.match(temporal_keyword_regex,question):
    return True

  elif re.match(answer_pattern,answer):
    return True

  else:
    for pattern in answer_question:
      question_p = re.compile( '|'.join(pattern[0]))
      answer_p = re.compile( '|'.join(pattern[1]))

      if re.match(question_p,question) and re.match(answer_p,answer):
        return True

  return False