import re
import numpy as np

fpath = "data/"
fname = "database.txt"

def main():
  vText = get_all_database()
  date = ""
  f = open(str(fpath+"database_by_day.txt"), "w")
  for txt in vText:
    if txt.find("DATE") != -1:
      f.writeline(txt[:len(txt)-1])
  f.close()

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

if __name__ == '__main__':
  main()
  #some_id("L255")

