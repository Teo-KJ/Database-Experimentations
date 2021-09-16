import psycopg2
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlalchemy

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

def crawlData():
    url = "http://www.cinemaonline.sg/movies/nowshowing.aspx"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.findAll("li")
    tags = [str(i) for i in tags]

    movieData = []
    for i in range(0, len(tags)):
        movieData.append(striphtml(tags[i]))

    del movieData[:20]
    movieData = movieData[:len(movieData)-4]

    for i in range(0, len(movieData)):
        movieData[i] = stripStuff(movieData[i])

    duration = []
    movieName = []
    classification = []
    castList = []
    releaseDate = []

    for i in movieData:
        find = re.search("Running Time: (.+?)Release", i).group(1)
        duration.append(find)
        find = re.search("(.+?)\(", i).group(1)
        movieName.append(find)
        find = re.search("Classification: (.+?)Genre:", i).group(1)
        classification.append(find)
        find = re.search("Cast: (.+?)\r", i).group(1)
        castList.append(find)
        find = re.search("Release Date: (.+?)Language", i).group(1)
        releaseDate.append(find)
        
    for i in range(0, len(movieName)):
        movieName[i] = stripWhitespace(movieName[i])

    viewType = []
    viewStatus = []

    for i in range(0, len(movieName)):
        viewType.append("Digital")
        viewStatus.append("Now Showing")

    movieDF = pd.DataFrame(np.column_stack([movieName, castList, duration, releaseDate, classification, viewType, viewStatus]), 
                                columns = ['Name', 'Casts', 'Runtime', 'ReleaseDate', 'Classification', 'ViewType', 'ViewStatus'])

    return movieDF

def getData(command, url):    
    conn = psycopg2.connect(url, sslmode='require')
    
    try:
        df = pd.read_sql(command, conn)
        if conn is not None:
            conn.close()
        
        return df
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def insertIntoDB():
    data = crawlData()
    url = 'postgresql://thwhoypafnogzl:a3f953c6eb51f1628ebd58f105128a2b13d9e7d3aa51dc756aca12dcb55a1611@ec2-3-224-7-166.compute-1.amazonaws.com:5432/d8dc5r528m6g32'
    engine = sqlalchemy.create_engine(url)
    data.to_sql(name='movie', con=engine, if_exists='replace')
    
    print("Done")