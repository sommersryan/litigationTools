import re
import datetime

def extractDate(string):
   #Takes a string, does some stuff, so what mind you own business
   yyyyMMDD = re.compile(r"(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])")
   mmDDYYYY = re.compile(r"(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d")
   matches = [yyyyMMDD.search(string),mmDDYYYY.search(string)]
   
   if matches[0] is not None: # for yyyymmdd dates
      foundDate = matches[0].string[matches[0].start():matches[0].end()]
      convertedDate = datetime.date(int(foundDate[:4]), int(foundDate[5:7]), int(foundDate[8:]))
      newString = convertedDate.isoformat() + " " + matches[0].string[0:matches[0].start()] + matches[0].string[matches[0].end():]
 
 if matches[1] is not None: # for mmddyyy dates
      foundDate = matches[1].string[matches[1].start():matches[1].end()]
      convertedDate = datetime.date(int(foundDate[6:]), int(foundDate[:2]), int(foundDate[3:5]))
      newString = convertedDate.isoformat() + " " + matches[1].string[0:matches[1].start()] + matches[1].string[matches[1].end():]
   