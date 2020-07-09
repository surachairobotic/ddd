import re
import numpy as np

fpath = "data/"
fname = "database.txt"

def main():
  vText = get_all_database()

  #print(vText)
  #vText = del_list_numpy(vText, 213)
  #exit()

  f = open(str(fpath+"database_by_id.txt"), "w")  
  for _id in range(0, 365):
    txt = "L"+"{:0>3d}".format(_id)
    #f.writelines("-----  "+txt+"  -----\n")
    date = ""
    indx_remove = []
    first=True
    for i in range(0, len(vText)):
      #print("i/len(vText) : " + str(i) + "/" + str(len(vText)) + "id: " + str(_id))
      if vText[i].find("DATE") != -1:
        date = vText[i][:len(vText[i])-1]
      if vText[i].find(txt) != -1 and vText[i].find("total") != -1:
        if first:
          if date != "":
            f.writelines(date.replace("DATE : ", ""))
          vText[i] = vText[i].replace("total", "เหลือ")
          tmpTxt = list(filter(None, re.split(r',|\n|\t| ', vText[i])))
          if tmpTxt[0] == "0000":
            f.writelines("," + tmpTxt[0] + tmpTxt[1] + tmpTxt[2] + '\n')
          if tmpTxt[0] == 'SPECIAL':
            f.writelines("," + tmpTxt[3] + "ต่อ" + tmpTxt[5] + tmpTxt[7] + '\n')
          else:
            f.writelines("," + tmpTxt[1] + "," + tmpTxt[2] + '\n')
          first=False
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

