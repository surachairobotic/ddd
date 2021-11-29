import sys

from PyPDF2 import PdfFileMerger

def main(pdfs):
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write("result.pdf")
    merger.close()

if __name__ == '__main__':  
    print('Number of arguments: ' + str(len(sys.argv)))
    print('Argument List: ' + str(sys.argv))

    if len(sys.argv) > 1:
        data = sys.argv[1:]
        main(data)
    else:
        print("if len(sys.argv) > 1 is FALSE")
