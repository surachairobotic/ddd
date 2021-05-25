import re
import numpy as np
from os import listdir
from os.path import isfile, join


fpath = ["data_64/", "data_63/", "data_62/"]
fname = "database.txt"

def main():
  filenames = []
  for i in range(len(fpath)):
    filenames += [f for f in listdir(fpath[i]) if isfile(join(fpath[i], f)) and f.find("_6") != -1]
  print(filenames)

  vText = get_all_database()

  #print(vText)
  #vText = del_list_numpy(vText, 213)
  #exit()

  f = open(str(fpath[0]+"database_by_id.txt"), "w")  
  fa = open(str(fpath[0]+"database_by_id_all.txt"), "w")  
  for _id in range(0, 999):
    txt = "L"+"{:0>3d}".format(_id)
    #f.writelines("-----  "+txt+"  -----\n")
    date = ""
    indx_remove = []
    first=True
    prev=-1
    for i in range(0, len(vText)):
      #print("i/len(vText) : " + str(i) + "/" + str(len(vText)) + "id: " + str(_id))
      if vText[i].find("DATE") != -1:
        date = vText[i][:len(vText[i])-1]
      if vText[i].find(txt) != -1 and vText[i].find("total") != -1:
        vText[i] = vText[i].replace("total", "เหลือ")
        tmpTxt = list(filter(None, re.split(r',|\n|\t| ', vText[i])))
        if tmpTxt[0] == "0000":
          if prev==1:
            fa.writelines('\n')
          prev=0
          fa.writelines(tmpTxt[0] + tmpTxt[1] + tmpTxt[2])
          if first:
            f.writelines(tmpTxt[0] + tmpTxt[1] + tmpTxt[2])
        if tmpTxt[0] == 'SPECIAL':
          prev=1
          fa.writelines(tmpTxt[3] + "ต่อ" + tmpTxt[5] + tmpTxt[7])
          if first:
            f.writelines(tmpTxt[3] + "ต่อ" + tmpTxt[5] + tmpTxt[7])
        else:
          if prev!=2:
            fa.writelines('\n')
          prev=2
          fa.writelines(tmpTxt[1] + "," + tmpTxt[2] + ",")
          if first:
            f.writelines(tmpTxt[1] + "," + tmpTxt[2])
          if date:
            end = date.find("/64")
            if end == -1:
              end = date.find("/63")
              if end == -1:
                end = date.find("/62")
            if end != -1:
              #print(date + " : " + date[7:] + " : " + str(end) + " : " + date[7:end+3])
              tmpTxt = list(filter(None, re.split(r'/', date[7:end+3])))
              target_name = str(tmpTxt[2]+"_"+"{:0>2d}".format(int(tmpTxt[1]))+"_"+"{:0>2d}".format(int(tmpTxt[0])))
              _fname = [name for name in filenames if name.find(target_name) != -1]
              if len(_fname):
                #print(target_name + ", " + _fname[0])
                #print(get_rawdata(_fname[0], str("{:0>3d}".format(_id))))
                rawdata = get_rawdata(_fname[0], str("{:0>3d}".format(_id)))
                #print(rawdata)
                for k in range(0, len(rawdata)):
                  fa.writelines(rawdata[k])
              else:
                print("Error : " + target_name + ", " + str(_fname) + ", " + str("{:0>3d}".format(_id)) + ", " + date)
            else:
              print("error" + date)
          #fa.writelines('\n')
        if date != "":
          fa.writelines(',วดป' + date.replace("DATE : ", "") + '\n')
          if first:
            f.writelines(',วดป' + date.replace("DATE : ", "") + '\n')

        first=False

        indx_remove.append(i)
        date = ""
    vText = del_list_numpy(vText, indx_remove)
  fa.close()
  f.close()

def del_list_numpy(l, id_to_del):
    arr = np.array(l)
    return list(np.delete(arr, id_to_del))
    
def get_all_database():
  global fpath, fname

  f = open(str(fpath[0]+fname), "r")  
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

def get_rawdata(_fname, _id):
  res = []
  for i in range(len(fpath)):
    if _fname.find(fpath[i][:-1]) != -1:
      ff = open(str(fpath[i]+_fname), "r")
      for txt in ff.readlines():
        if txt.find(_id) != -1:
          txt = txt.replace(str(_id+' '), "")
          res.append(txt.replace('\n', ""))
      ff.close()
  return res

if __name__ == '__main__':
  main()
  #some_id("L255")

