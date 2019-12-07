from docx import Document
from docx.shared import Mm, Pt

class Person:
  def __init__(self):
    self.id = ""
    self.info = []
    self.total = []


f = open("/home/cobot/ddd/data.txt", "r")
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

document = Document()

# page setup to A4
section = document.sections[0]
section.page_height = Mm(297)
section.page_width = Mm(210)

# Default style
style = document.styles['Normal']
font = style.font
font.name = 'TH SarabunPSK'
font.size = Pt(16)

seq=seq+1
for j in range(len(information)):
  p = document.add_paragraph('No.')
  p.add_run(str(seq))
  p = document.add_paragraph('เลขสมาชิก : L')
  p.add_run(str(information[j].id))
  document.add_paragraph(str('วันที่ : ')+str(date))
  document.add_paragraph(str('----------'))
  for k in information[j].info:
    i=0
    while i < len(k):
      if k[i].isnumeric():
        break
      i=i+1
    if i != 0:
      k = k[:i] + str(' ') + k[i:]
    document.add_paragraph(str(k))
  document.add_paragraph(str('----------'))
  document.add_paragraph(str('รวม ')+str(information[j].total[0])+str(' ชิ้น'))
  document.add_paragraph(str('เหลือ ')+str(information[j].total[1])+str(' ชิ้น'))
  seq=seq+1


document.save('demo.docx')

