import os
import sys
import re
import shutil
from pdf2txt import main as pdf2txt
import csv
from pyPdf import PdfFileWriter, PdfFileReader

def batesName(oldname,filePath,prefix,numDigits):
    saveout = sys.stdout
    logFile = filePath + '/out.log'
    pdfFile = filePath + '/' + oldname
    fsock = open(logFile, 'w')
    sys.stdout = fsock
    pdf2txt(["","-p 1",pdfFile])
    sys.stdout = saveout
    fsock.close()
    #
    f = open(logFile, 'r')
    text_list = f.readlines()
    for i in text_list:
        searchterm = prefix + ("\d" * numDigits)
        excerpt = re.search(searchterm,i)
        try:
            start = excerpt.string.find(prefix)
            batesnumber = excerpt.string[start:start+numDigits+len(prefix)] + '.pdf'
            newFile = filePath + '/' + batesnumber
            os.rename(pdfFile,newFile)
            print batesnumber
            f.close()
            return
        except AttributeError: 
            continue

def batchBatesName():
    filePath = raw_input("Enter path of files to be renamed: ")
    prefix = raw_input("Enter bates prefix of files: ")
    numDigits = int(raw_input("Enter the number of numerical digits in each Bates label: "))
    fileList = os.listdir(filePath)
	
    for i in fileList:
        try:
            batesName(i,filePath,prefix,numDigits)
        except:
            print "probably not a PDF"

def extractCopy():
    sourceText = raw_input("Enter path of text file with target files: ")
    destination = raw_input("Enter destination path for copying: ")
	
    f = open(sourceText,'r')
    doclist = [a.strip() for a in f.readlines()]

    for i in doclist:
        shutil.copy(i,destination)
		


def batesAppend(oldname,filePath,prefix,numDigits):
    saveout = sys.stdout
    logFile = filePath + '/out.log'
    pdfFile = filePath + '/' + oldname
    fsock = open(logFile, 'w')
    sys.stdout = fsock
    pdf2txt(["","-p 1",pdfFile])
    sys.stdout = saveout
    fsock.close()
    #
    f = open(logFile, 'r')
    text_list = f.readlines()
    for i in text_list:
        searchterm = prefix + ("\d" * numDigits)
        excerpt = re.search(searchterm,i)
        try:
            start = excerpt.string.find(prefix)
            batesnumber = excerpt.string[start:start+numDigits+len(prefix)]
            newFile = filePath + '/' + batesnumber + "--" + oldname
            os.rename(pdfFile,newFile)
            print batesnumber
            f.close()
            return
        except AttributeError: 
            continue

def batchBatesAppend():
    filePath = raw_input("Enter path of files to be renamed: ")
    prefix = raw_input("Enter bates prefix of files: ")
    numDigits = int(raw_input("Enter the number of numerical digits in each Bates label: "))
    fileList = os.listdir(filePath)
	
    for i in fileList:
        try:
            batesAppend(i,filePath,prefix,numDigits)
        except:
            print "probably not a PDF"
			
def treeExtract():
    fileList = raw_input("Enter the path of the csv file containing files info:")
    destinationPath = raw_input("Enter the destination path for copying:")
    fp = open(fileList,'rU')
    reader = csv.reader(fp)
    list = []
    for row in reader:
        list.append(row)
    for file in list:
        destination = destinationPath + '/' + file[1] + '/'
        if not os.path.exists(destination):
            os.makedirs(destination)
        shutil.copy(file[0],destination)
    fp.close()
	
def flattenDirs():
    sourcePath = raw_input("Enter the root path to flatten:")
    charstart = len(sourcePath) + 1
    destinationPath = raw_input("Enter the destination path for copying:")
    for root, dirs, files in os.walk(sourcePath):
        for file in files:
            src = root + '/' + file
            begname = root[charstart:].replace('\\','--')
            newname = begname + '--' + file
            shutil.copy(src,destinationPath+'/'+newname)
			
	
def batesNumberName(oldname,filePath):
    #only use this and the batch function below when the Bates is the only extractable text
    saveout = sys.stdout
    logFile = filePath + '/out.log'
    pdfFile = filePath + '/' + oldname
    fsock = open(logFile, 'w')
    sys.stdout = fsock
    pdf2txt(["","-p 1",pdfFile])
    sys.stdout = saveout
    fsock.close()
    #
    f = open(logFile, 'r')
    text_list = f.readlines()
    try:
        newNumber = str(int(re.findall("[0-9]+",text_list[0])[0]))
        batesnumber = newNumber + '.pdf'
        newFile = filePath + '/' + batesnumber
        os.rename(pdfFile,newFile)
        print batesnumber
        f.close()
        return
    except AttributeError: 
        print "text not found"


def batchBatesNumberName():
    filePath = raw_input("Enter path of files to be renamed: ")
    fileList = os.listdir(filePath)
    for i in fileList:
        try:
            batesNumberName(i,filePath)
        except:
            print "probably not a PDF"

def pdfSplit():
    splitList = raw_input("Enter path of text file with page split info: ")
    targetPDF = raw_input("Enter the path of the target PDF: ")
    destinationPath = raw_input("Enter the destination path for the split PDFs:")

    splitsFile = open(splitList,"r")
    pageRanges = [a.strip().split(',') for a in splitsFile.readlines()]
    inputPDF = PdfFileReader(file(targetPDF,'rb'))

    for pageRange in pageRanges:
        outputPDF = PdfFileWriter()
        for page in range(int(pageRange[0]),int(pageRange[1])+1):
            outputPDF.addPage(inputPDF.getPage(page-1))
        outputName = destinationPath + pageRange[0] + "-" + pageRange[1] + ".pdf"
        outputStream = file(outputName,"wb")
        outputPDF.write(outputStream)
        print outputName + " complete."
        outputStream.close()

    splitsFile.close()
    
def batchPdfAssemble():
    splitList = raw_input("Enter path of text file containing paginations: ")
    sourceDir = raw_input("Enter path containing single page sources: ")
    targetDir = raw_input("Enter target directory for output: ")
    
    splitsFile = open(splitList,"r")
    pageRanges = [a.strip().split(',') for a in splitsFile.readlines()]
    
    for pageRange in pageRanges:
        outputPDF = PdfFileWriter()
        for page in range(int(pageRange[1]),int(pageRange[2])+1):
            targetName = sourceDir + str(page) + '.pdf'            
            inputPDF = PdfFileReader(file(targetName,'rb'))
            outputPDF.addPage(inputPDF.getPage(0))
        outputName = targetDir + pageRange[0] + '.pdf'
        outputStream = file(outputName,"wb")
        outputPDF.write(outputStream)
        print outputName + " complete."
        outputStream.close()
    
    splitsFile.close()
        
def pdfPageCount():
    pdfPath = raw_input("Enter path of PDF files: ")
    totalPages = 0
    pdfFiles = os.listdir(pdfPath)
    for file in pdfFiles:
       totalPages += PdfFileReader(open(pdfPath+'/'+file,'rb')).getNumPages()
       #print file + " has this many pages: " + str(PdfFileReader(open(pdfPath+'/'+file,'rb')).getNumPages()) + '\n'
    print str(len(pdfFiles)) + " PDFs contain " + str(totalPages) + " pages"
    return totalPages
    

def incrementSplit():
    pdfPath = raw_input("Enter path of target PDF: ")
    outputPath = raw_input("Enter path for output: ")
    splitIncrement = int(raw_input("Enter page increment at which to split: "))
    targetPDF = PdfFileReader(open(pdfPath,'rb'))
    totalPages = targetPDF.getNumPages()
    numSets, leftover = divmod(totalPages,splitIncrement)
    onPage = 0
    onSet = 0
    while onSet <= numSets:
       fileName = outputPath + "/" + str(onSet).zfill(4) + ".pdf"
       outputStream = file(fileName,"wb")
       outputPDF = PdfFileWriter()
       while onPage < onSet*splitIncrement:
          outputPDF.addPage(targetPDF.getPage(onPage))
          onPage += 1
       outputPDF.write(outputStream)
       outputStream.close()
       onSet += 1
    #Create last PDF of leftovers
    fileName = outputPath + "/" + str(onSet).zfill(4) + ".pdf"
    outputStream = file(fileName,"wb")
    outputPDF = PdfFileWriter()
    while onPage < targetPDF.getNumPages():
        outputPDF.addPage(targetPDF.getPage(onPage))
        onPage += 1
    outputPDF.write(outputStream)
    outputStream.close()
    
def incrementSplit2(pdfPath,outputPath,splitIncrement):
    targetPDF = PdfFileReader(open(pdfPath,'rb'))
    totalPages = targetPDF.getNumPages()
    numSets, leftover = divmod(totalPages,splitIncrement)
    onPage = 0
    onSet = 0
    while onSet <= numSets:
       fileName = outputPath + "/" + str(onSet).zfill(4) + ".pdf"
       outputStream = file(fileName,"wb")
       outputPDF = PdfFileWriter()
       while onPage < onSet*splitIncrement:
          outputPDF.addPage(targetPDF.getPage(onPage))
          onPage += 1
       outputPDF.write(outputStream)
       outputStream.close()
       onSet += 1
    #Create last PDF of leftovers
    fileName = outputPath + "/" + str(onSet).zfill(4) + ".pdf"
    outputStream = file(fileName,"wb")
    outputPDF = PdfFileWriter()
    while onPage < targetPDF.getNumPages():
        outputPDF.addPage(targetPDF.getPage(onPage))
        onPage += 1
    outputPDF.write(outputStream)
    outputStream.close()
       
       
        
   
    