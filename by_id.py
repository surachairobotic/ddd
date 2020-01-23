import re
import numpy as np

fpath = "data/"
fname = "database.txt"

def main():
  vText = get_all_database()

  f = open(str(fpath+"database_by_id.txt"), "w")  
  for _id in range(0, 350):
    txt = "L"+"{:0>3d}".format(_id)
    f.writelines("-----  "+txt+"  -----\n")
    date = ""
    indx_remove = []
    for i in range(0, len(vText)):
      if vText[i].find("DATE") != -1:
        date = vText[i][:len(vText[i])-1]
      if vText[i].find(txt) != -1:
        if date != "":
          f.writelines(date.replace("DATE : ", ""))
        f.writelines(", "+vText[i])
        indx_remove.append(i)
        date = ""
    vText = del_list_numpy(vText, indx_remove)
  f.close()

def del_list_numpy(l, id_to_del):
    arr = np.array(l)
    return list(np.delete(arr, id_to_del))
    
def get_all_database():
  global fpath, fname

  f = open(str(fpath+fname), "r")  
  data = []
  for txt in f.readlines():
    #data.append(list(filter(None, re.split(r',|\n|\t| ', txt))))
    data.append(txt)
  f.close()
  return data

def some_id(_id):
  global fpath, fname
  
  f = open(str(fpath+fname), "r")
  
  date = ""
  for txt in f.readlines():
    if txt.find("DATE") != -1:
      date = txt.replace('\n', '')
    if txt.find(_id) != -1:
      if date != "":
        print(date)
      print(txt.replace('\n', ''))
      date=""
  
  f.close()
  

if __name__ == '__main__':
  main()
  #some_id("L255")

