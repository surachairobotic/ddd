from docx import Document
from docx.shared import Mm, Pt
import math

class Person:
  def __init__(self):
    self.id = ""
    self.info = []
    self.total = '-'
    self.count = 0.0
    self.cash = 0.0
    self.old_total = 0.0

def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

fname = "data_62_12_17"
f = open(fname+".txt", "r")
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

infor_base = []

#### To Do
#### read database file to variable
#f = open("database.txt", "r")
#for t in f.readline():
#  print(t)
#  if 

for x in information:
  print(x.__dict__)

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

seq=seq+1
for j in range(len(information)):
  p = document.add_paragraph('No.')
  p.add_run(str(seq))
  p = document.add_paragraph('เลขสมาชิก : ')
  if information[j].id[0].isnumeric():
    p.add_run('L')
  p.add_run(str(information[j].id))
  document.add_paragraph(str('วันที่ : ')+str(date))
  document.add_paragraph(str('----------'))
  line=6
  for k in information[j].info:
    i=0
    while i < len(k):
      if k[i].isnumeric():
        break
      i=i+1
    if i != 0:
      k = k[:i] + str(' ') + k[i:]
    document.add_paragraph(str(k))
    line=line-1
  document.add_paragraph(str('----------'))
  if information[j].count != 0.0:
    document.add_paragraph(str('รวม ')+str(information[j].count)+str(' ชิ้น'))
    line=line-1
    if not (information[j].total[0] == '-'):
      old_total = float(information[j].total[0])
      new_total = old_total-information[j].count
      if new_total == int(new_total):
        new_total = int(new_total)
      document.add_paragraph(str('เหลือ ')+str(new_total)+str(' ชิ้น'))
      line=line-1
  if information[j].cash != 0.0:
    document.add_paragraph(str('ยอดชำระ ')+str(information[j].cash)+str(' บาท'))
    line=line-1
  while line > 0:
    document.add_paragraph('')
    line=line-1
  seq=seq+1


document.save('demo_'+fname+'.docx')


