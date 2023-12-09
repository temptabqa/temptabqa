from bs4 import BeautifulSoup
import re

def remove_italics(soup):
    for i in soup.findAll('i'):
        i.replaceWithChildren()
    return soup

def clean_stack(stack):
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
        if(s[-1]!=" "):
            s = s+ " "+word
        else:
            s = s+word
    if(s.isspace()==False):
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

          main_json[header_name] = header_dictionary

          header_name = ""
          header_dictionary = {}
          non_th_list = []

        header_name = clean_stack(tr.find('td').findAll(string=True))
        continue

      elif 'font-weight:' in str(tr.find('td')):
        if header_name != "":
          if len(non_th_list) > 0:
            header_dictionary[header_name] = non_th_list

          main_json[header_name] = header_dictionary

          header_name = ""
          header_dictionary = {}
          non_th_list = []

        header_name = clean_stack(tr.find('td').findAll(string=True))
        continue

    if header_name != "":
      stack = []
      for td in tr.findAll(['th','td']):
        if len(clean_stack(td.findAll(string=True))) != 0:
          stack.append(clean_stack(td.findAll(string=True)))
      if clean_stack(stack) != "":
        non_th_list.append(clean_stack(stack))

      continue

    if len(tr.findAll('td')) == 1 and len(tr.findAll('th')) == 0 and header_name == "":
      if "class" in tr.find('td').attrs and tr.find('td').attrs["class"][0] == "infobox-image":
        key = "infobox-image"
        value = clean_stack(tr.find('td').findAll(string=True))

        main_json[key] = value
        continue

  if header_name != "":
    if len(non_th_list) > 0:
      header_dictionary[header_name] = non_th_list

    main_json[header_name] = header_dictionary

    header_name = ""
    header_dictionary = {}
    non_th_list = []

  return main_json