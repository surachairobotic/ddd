from docx import Document
from docx.shared import Mm, Pt
import math

class Person:
  def __init__(self):
    self.id = ""
    self.info = []
    self.total = []
    self.cash = -1.0

def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

fname = "data_62_12_7"
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
  v.info = tmp[1:len(tmp)-2]
  v.total = tmp[len(tmp)-2:]
  information.append(v)

for x in information:
  print(x.__dict__)

for v in information:
  _b_err = False
  _b_cash = False
  _sum_cash = 0.0
  for _info in v.info:
    if _info.find('*') != -1:
      i=0
      while i < len(_info):
        if _info[i].isnumeric():
          break
        i=i+1
      if i != 0:
        new_info = split(["*","="], _info[i:])
        new_info = [float(i) for i in new_info]
        tmp_cash = new_info[0]*new_info[1]
        #print("new=%s : old=%s : %s" %(new_info, _info, normal_round(new_info[0]*new_info[1])))
        if new_info[1] > 4:
          _b_cash = True
          tmp_cash = normal_round(tmp_cash)
          _sum_cash = _sum_cash+tmp_cash
          #print("%s | %s" % (tmp_cash, _sum_cash))
        if tmp_cash != new_info[2]:
          print("new=%s : old=%s : %s" %(new_info, _info, normal_round(new_info[0]*new_info[1])))
          _b_err = True
          break
          
  if _b_err:
    print("ERROR : %s" % v.__dict__)
  elif _b_cash:
    v.cash = _sum_cash

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
  if not (information[j].total[0] == '-'):
    document.add_paragraph(str('รวม ')+str(information[j].total[0])+str(' ชิ้น'))
    line=line-1
  if not (information[j].total[1] == '-'):
    document.add_paragraph(str('เหลือ ')+str(information[j].total[1])+str(' ชิ้น'))
    line=line-1
  if information[j].cash != -1.0:
    document.add_paragraph(str('ยอดชำระ ')+str(information[j].cash)+str(' บาท'))
    line=line-1
  while line > 0:
    document.add_paragraph('')
    line=line-1
  seq=seq+1


document.save('demo_'+fname+'.docx')

