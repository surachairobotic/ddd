from os import listdir
from os.path import isfile, join
import math
import matplotlib.pyplot as plt

fpath = "data_65/"
fname = "database.txt"

def main():
  onlyfiles = [f for f in listdir(fpath) if isfile(join(fpath, f)) and f.find("_6") != -1]
  onlyfiles.sort()
  
  #for x in onlyfiles:
  #  print(x)
  #print(type(onlyfiles))
  #print(type(onlyfiles[0]))
  
  #exit()

  min_day = 9999
  min_7 = 9999
  min_15 = 9999
  min_30 = 9999
  max_day = 0
  max_7 = 0
  max_15 = 0
  max_30 = 0

  _all = []
  avg7 = []
  avg15 = []
  avg30 = []
  cnt7 = []
  cnt15 = []
  cnt30 = []
  cashs = []
  counts = []
  cashs7 = []
  counts7 = []
  all7 = []
  for indx in range(len(onlyfiles)):
    #print(onlyfiles[indx])
    information = read_info(onlyfiles[indx])
    information = processing(information)
    sum_count = 0
    sum_cash = 0
    for item in information:
      sum_count += item.count
      sum_cash += item.cash
    counts.append(sum_count)
    cashs.append(sum_cash)
    _all.append(sum_cash+sum_count*11)
    len_cashs = len(cashs)
    d = 30
    if len_cashs < d:
        cashs7.append(sum(cashs)/len_cashs)
        counts7.append(sum(counts)/len_cashs)
        all7.append(sum(_all)/len_cashs)
    else:
        cashs7.append(sum(cashs[len_cashs-d:])/d)
        counts7.append(sum(counts[len_cashs-d:])/d)
        all7.append(sum(_all[len_cashs-d:])/d)
    min_day = min(min_day, sum_cash+sum_count*11)
    max_day = max(max_day, sum_cash+sum_count*11)
    cnt7.append(sum_count)
    cnt15.append(sum_count)
    cnt30.append(sum_count)
    avg7.append(sum_cash+sum_count*11)
    avg15.append(sum_cash+sum_count*11)
    avg30.append(sum_cash+sum_count*11)
    while len(avg7) > 6:
      avg7.pop(0)
    while len(avg15) > 14:
      avg15.pop(0)
    while len(avg30) > 26:
      avg30.pop(0)
    while len(cnt7) > 6:
      cnt7.pop(0)
    while len(cnt15) > 14:
      cnt15.pop(0)
    while len(cnt30) > 26:
      cnt30.pop(0)
    _str = str("%s, count: %.2f, cash: %.2f, total:%.2f" % (onlyfiles[indx], sum_count, sum_cash, sum_cash+sum_count*11))
    if len(avg7) == 6:
      _str += str(", avg[7]: %f" % (sum(avg7)/len(avg7)))
      min_7 = min(min_7, sum(avg7)/len(avg7))
      max_7 = max(max_7, sum(avg7)/len(avg7))
    if len(avg15) == 14:
      _str += str(", avg[15]: %f" % (sum(avg15)/len(avg15)))
      min_15 = min(min_15, sum(avg15)/len(avg15))
      max_15 = max(max_15, sum(avg15)/len(avg15))
    if len(avg30) == 26:
      _str += str(", avg[30]: %f" % (sum(avg30)/len(avg30)))
      min_30 = min(min_30, sum(avg30)/len(avg30))
      max_30 = max(max_30, sum(avg30)/len(avg30))
    if len(cnt7) == 6:
      _str += str(", cnt[7]: %f" % (sum(cnt7)/len(cnt7)))
    if len(cnt15) == 14:
      _str += str(", cnt[15]: %f" % (sum(cnt15)/len(cnt15)))
    if len(cnt30) == 26:
      _str += str(", cnt[30]: %f" % (sum(cnt30)/len(cnt30)))
    print(_str)
  print("day : %.2f, %.2f" % (min_day, max_day))
  print("7 : %.2f, %.2f" % (min_7, max_7))
  print("15 : %.2f, %.2f" % (min_15, max_15))
  print("30 : %.2f, %.2f" % (min_30, max_30))
  print("all: %.2f, avg: %.2f" % (sum(_all), (sum(_all)/len(_all))))

  fig, axarr = plt.subplots(3, 1, sharex=True)
  #axarr[0].plot(counts)
  #axarr[1].plot(cashs)
  #axarr[2].plot(_all)
  axarr[0].plot(counts7)
  axarr[1].plot(cashs7)
  axarr[2].plot(all7)

  #plt.gca().invert_xaxis()
  plt.plot()
  plt.show()

def read_info(_fname):
  f = open(str(fpath+_fname), "r", encoding="utf8")
  lines = f.readlines()
  f.close()
  data = []
  for line in lines:
    if line.find("++") == -1:
      if line[len(line)-1] == '\n':
        line = line[:len(line)-1]
      focus = ['340', '301', '276', '370', '900']
      b_save = False
      for x in focus:
        if line.find(x) != -1:
            b_save = True
            break
      b_save = True
      if b_save:
        data.append(line)
      #print(line)

  information = []
  for i in range(1, len(data)):
    tmp = data[i].split()
    v = Person()
    start = 1
    if tmp[1][0] == '(':
      start = 2
    end = len(tmp)
    if tmp[len(tmp)-1].isnumeric() or tmp[len(tmp)-1].find("-") != -1:
      end -= 1
    v.info = tmp[start:end]
    information.append(v)

  return information

def processing(information):
  for v in information:
    _b_err = False
    _sum_cash = 0.0
    #print(v.info)
    for k in range(len(v.info)):
      i=0
      if v.info[k].find('*') != -1:
        while i < len(v.info[k]):
          if v.info[k][i].isnumeric():
            break
          i=i+1
        if i != 0:
          #print(v.info[k])
          new_info = split(["*","="], v.info[k][i:])
          new_info = [float(i) for i in new_info]
          mul = new_info[0]*new_info[1]
          #print("new=%s : old=%s : %s" %(new_info, _info, normal_round(new_info[0]*new_info[1])))
          if new_info[1] > 4:
            mul = normal_round(mul)
            v.cash = v.cash+mul
            #print("%s | %s" % (mul, _sum_cash))
          else:
            v.count = v.count + mul
          if (len(new_info) == 3) and (mul != new_info[2]):
            print("new=%s : old=%s : %s" %(new_info, _info, normal_round(new_info[0]*new_info[1])))
            _b_err = True
            break
          elif len(new_info) == 2:
            #print('In')
            #print(v.info[k])
            v.info[k] = v.info[k]+str('=')+str(mul)
            #print(v.info[k])
            #print('--In--')
      elif not (v.info[k][0] == 'ม'):
        #print("debug : %s" % v.info[k])
        i=0
        while i < len(v.info[k]):
          if v.info[k][i].isnumeric():
            break
          i=i+1
        if i != 0:
          #print("v.info[%d][%d:] : %s" % (k, i, v.info[k][i:]))
          new_info = int(v.info[k][i:])
          v.count = v.count + new_info
    if v.count == int(v.count):
      v.count = int(v.count)
    if v.cash == int(v.cash):
      v.cash = int(v.cash)
      #print("v.count, int(v.count) : %f, %d" % (v.count, int(v.count)))
    #print(v.info)
            
    if _b_err:
      print("ERROR : %s" % v.__dict__)
  return information

def old_main():
  vText = get_all_database()
  date = ""
  state = 0
  total = 0
  cash = 0
  sum_cash = 0
  f = open(str(fpath+"database_by_day.txt"), "w")
  for txt in vText:
    txt = txt[:len(txt)-1]
    if txt.find("DATE") != -1:
      if state == 0:
        total = 0
        cash = 0
        state = 1
      elif state == 1:
        print("cash : ", cash)
        sum_cash += cash
        total = 0
        cash = 0
      print(txt)
        
    elif txt.find("total") != -1:
      i = txt.find("total");
      #print("total : ", txt[i+6:])
      if txt.find("cash") != -1:
        j = txt.find('\t', i+6)
        total += float(txt[i+6:j])
    if txt.find("cash") != -1:
      i = txt.find("cash");
      cash += float(txt[i+5:])
      #print("cash : ", txt[i+5:])
      #f.writeline(txt[:len(txt)-1])
  f.close()
  print("cash : ", cash)
  sum_cash += cash
  print("sum_cash : ", sum_cash)
  
  onlyfiles = [f for f in listdir(fpath) if isfile(join(fpath, f))]
  print(onlyfiles)

def get_all_database():
  global fpath, fname

  f = open(str(fpath+fname), "r")  
  data = []
  for txt in f.readlines():
    #data.append(list(filter(None, re.split(r',|\n|\t| ', txt))))
    if txt.find("SPECIAL") != -1 or txt.find("INITIAL") != -1 or txt.find("0000") != -1:
      continue
    data.append(txt)
  f.close()
  return data

def find_second_letter(_txt):
  indx = -1
  
  return indx

class Person:
  def __init__(self):
    self.info = []
    self.count = 0.0
    self.cash = 0.0

def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

if __name__ == '__main__':
  main()
  #some_id("L255")

