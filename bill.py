import math
import os

from docx import Document
from docx.shared import Mm, Pt
from docx.enum.style import WD_STYLE_TYPE

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Person:
  def __init__(self):
    self.id = ""
    self.info = []
    self.total = '-'
    self.count = 0.0
    self.cash = 0.0
    self.old_total = 0.0
    self.font_sz = 36
    self.line = 6

def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

def read_info(name):
  f = open(name, "r")
  data = []
  for line in f.readlines():
    data.append(line)
  f.close()

  print(data)

  date, seq = data[0].split()
  seq = int(seq)
  print(date)
  print(seq)

  information = []
  for i in range(1, len(data)):
    tmp = data[i].split()
    v = Person()
    v.id = tmp[0]
    v.info = tmp[1:len(tmp)-1]
    v.total = tmp[len(tmp)-1:]
    information.append(v)

  return date, seq, information

def processing(information):
  for v in information:
    _b_err = False
    _sum_cash = 0.0
    #print(v.info)
    for k in range(len(v.info)):
      if v.info[k].find('*') != -1:
        i=0
        while i < len(v.info[k]):
          if v.info[k][i].isnumeric():
            break
          i=i+1
        if i != 0:
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
          if (len(new_info) is 3) and (mul != new_info[2]):
            print("new=%s : old=%s : %s" %(new_info, _info, normal_round(new_info[0]*new_info[1])))
            _b_err = True
            break
          elif len(new_info) is 2:
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
          #print("v.info[k][i:] : %s" % v.info[k][i:])
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

def insert_space(info):
  for k in range(len(info)):
    i=0
    while i < len(info[k]):
      if info[k][i].isnumeric():
        break
      i=i+1
    if i != 0:
      info[k] = info[k][:i] + str(' ') + info[k][i:]
  return info

def reduce_line(info):  
  for i in range(len(info)-1):
    for j in range(i+1, len(info)):
      x=info[i]
      y=info[j]
      if len(x+"    "+y) < 20:
        info[i] = info[i]+"    "+info[j]
        del info[j]
        return True
  return False


if __name__ == '__main__':

  fpath = "data/"
  fname = "data_63_01_02"

  date, seq, information = read_info(str(fpath+fname+".txt"))

  infor_base = []

  #### To Do
  #### read database file to variable
  #f = open("database.txt", "r")
  #for t in f.readline():
  #  print(t)
  #  if 

  for x in information:
    print(x.__dict__)

  information = processing(information)

  print('-----')
  for x in information:
    print(x.__dict__)
    
  #  for y in infor_base:

  #### To Do
  #### save variable to database file
  #f = open("database.tmp", "w")

  document = Document()

  # page setup to A4
  section = document.sections[0]
  section.page_height = Mm(297)
  section.page_width = Mm(210)

  # Default style
  style = document.styles['Normal']
  font = style.font
  font.name = 'TH SarabunPSK'
  font.size = Pt(36)
  
  styles = document.styles
  style_a36 = styles.add_style('A36', WD_STYLE_TYPE.PARAGRAPH)
  style_a36.font.name = 'TH SarabunPSK'
  style_a36.font.size = Pt(36)

  style_a34 = styles.add_style('A34', WD_STYLE_TYPE.PARAGRAPH)
  style_a34.font.name = 'TH SarabunPSK'
  style_a34.font.size = Pt(34)

  style_a31 = styles.add_style('A31', WD_STYLE_TYPE.PARAGRAPH)
  style_a31.font.name = 'TH SarabunPSK'
  style_a31.font.size = Pt(31)

  style_a28 = styles.add_style('A28', WD_STYLE_TYPE.PARAGRAPH)
  style_a28.font.name = 'TH SarabunPSK'
  style_a28.font.size = Pt(28)

  style_a26 = styles.add_style('A26', WD_STYLE_TYPE.PARAGRAPH)
  style_a26.font.name = 'TH SarabunPSK'
  style_a26.font.size = Pt(26)

  style_a24 = styles.add_style('A24', WD_STYLE_TYPE.PARAGRAPH)
  style_a24.font.name = 'TH SarabunPSK'
  style_a24.font.size = Pt(24)

  f_tmp = open(fpath+"database.tmp", "w")
  f_tmp.writelines("DATE : "+date+"\n")

  for j in range(len(information)):
    information[j].info = insert_space(information[j].info)

  font_sz = [36, 34, 31, 28, 26, 24]
  lines   = [ 6,  7,  8,  9, 10, 11]
  j=0
  while j<len(information):
    line=0
    if information[j].count != 0.0:
      line=line+1
      if not (information[j].total[0] == '-'):
        line=line+1
    if information[j].cash != 0.0:
      line=line+1

    if len(information[j].info)+line > 6:
      while reduce_line(information[j].info):
        print(information[j].info)
    information[j].line = len(information[j].info)+line
    information[j].font_sz = font_sz[max(0, information[j].line-6)]
    #print("ID:%s, line:%d, font:%d" % (information[j].id, information[j].line, information[j].font_sz))
    j=j+1
  
  seq=seq+1
  for j in range(len(information)):
    print("ID:%s, line:%d, font:%d" % (information[j].id, information[j].line, information[j].font_sz))

    style = document.styles[str('A'+str(information[j].font_sz))]
    p = document.add_paragraph('No.', style)

    p.add_run(str(seq))
    f_tmp.write(str(seq)+",\t")
    p = document.add_paragraph('เลขสมาชิก : ', style)
    if information[j].id[0].isnumeric():
      p.add_run('L')
      f_tmp.write("L")
    p.add_run(str(information[j].id))
    f_tmp.write(str(information[j].id)+"\t")
    p = document.add_paragraph(str('วันที่ : ')+str(date), style)
    p = document.add_paragraph(str('----------'), style)
    
    for k in range(len(information[j].info)):
      p = document.add_paragraph(str(information[j].info[k]), style)

    p = document.add_paragraph(str('----------'), style)
    if information[j].count != 0.0:
      p = document.add_paragraph(str('รวม ')+str(information[j].count)+str(' ชิ้น'), style)
      if not (information[j].total[0] == '-'):
        old_total = float(information[j].total[0])
        new_total = old_total-information[j].count
        if new_total == int(new_total):
          new_total = int(new_total)
        p = document.add_paragraph(str('เหลือ ')+str(new_total)+str(' ชิ้น'), style)
        f_tmp.write("\t,total:"+str(new_total))
    if information[j].cash != 0.0:
      p = document.add_paragraph(str('ยอดชำระ ')+str(information[j].cash)+str(' บาท'), style)
      f_tmp.write("\t,cash:"+str(information[j].cash))
    f_tmp.writelines("\n")
    line=information[j].line
    while line < 6:
      p = document.add_paragraph('', style)
      line=line+1
    seq=seq+1

  docx = 'demo_'+fname+'.docx'
  document.save(docx)
  
  document.save('debug.docx')

#  f_database = open(fpath+"database_new.txt", "r")
#  for t in f_database.readlines():
#    f_tmp.write(t)

#  os.rename(fpath+"database.tmp", fpath+"database_new.txt")

  f_tmp.close()
#  f_database.close()

##############################
##############################
##############################

#  gauth = GoogleAuth()
#  gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
#  drive = GoogleDrive(gauth)
  
#  folder_id = '1fKs5geKxK3i3aNMvrMTW6ZIfuoganM-N'
#  file1 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}]})
#  file1.SetContentFile(docx)
#  file1.Upload() # Upload the file.
  
  # View all folders and file in your Google Drive
#  fileList = drive.ListFile({'q': "'{0}' in parents and trashed=false".format(folder_id)}).GetList()
#  for file in fileList:
#    if file['title'] == docx:
#      print('Title: %s, ID: %s' % (file['title'], file['id']))


