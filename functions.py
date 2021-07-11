
import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def stripStuff(data):
    data = re.sub("\n", "", data)
    data = re.sub("\xa0\r", "", data)
    data = re.sub("\xa0New\xa0", "", data)
    data = re.sub("\xa0", "", data)
    return data

def stripWhitespace(data):
    return re.sub("                                            ", "", data)


