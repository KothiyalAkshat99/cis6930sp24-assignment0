import fitz
from urllib.request import urlopen
import io
import sqlite3
import argparse

def fetchincidents(url):
    #headers = {}
    #headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    response = urlopen(url).read()
    response = io.BytesIO(response) # In-Memory Binary Stream, can be read like a file

    return response


def extractincidents(incident_data):

    doc = fitz.open(stream = incident_data, filetype="pdf") # Using PyMuPDF/ Fitz module for PDF data extraction

    global dttime, inc_no, loc, nature, inc_ori
    dttime = []
    inc_no = []
    loc = []
    nature = []
    inc_ori = []

    for page_number in range(len(doc)):

        global ls
        ls = []
        
        x = doc[page_number]
        text = x.get_text("blocks")

        if page_number == 0: # Removing extraneous info from first page
            text.pop(0)
            text.pop()
            text.pop()
        elif page_number == len(doc)-1: # Removing extraneous info from last page
            text.pop()
        
        for t in text: # Splitting text list into required columns
            
            temp = t[4].split('\n')
            temp.remove('')
            if(len(temp)<5): # Handling Blank Spaces for 'Nature' column
                temp.insert(2, ' ')
                temp.insert(3, ' ')
            elif(len(temp)>5): # Handling Multi-line 'Location' issues
                temp[2] = temp[2] + temp[3]
                temp.pop(3)
            ls.append(temp)

        dttime.append([sublist[0] for sublist in ls])
        inc_no.append([sublist[1] for sublist in ls])
        loc.append([sublist[2] for sublist in ls])
        nature.append([sublist[3] for sublist in ls])
        inc_ori.append([sublist[4] for sublist in ls])

    incidents = [dttime, inc_no, loc, nature, inc_ori]
    return incidents


def createdb():

    con = sqlite3.connect("resources/normanpd.db") # Creating Database connection
    cur = con.cursor() # Database Cursor
    
    #Creating incident table
    cur.execute("DROP TABLE IF EXISTS incidents;")
    cur.execute("CREATE TABLE incidents (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT);")
    
    return con


def populatedb(db, incidents):

    cur = db.cursor()

    dttime = incidents[0]
    inc_no = incidents[1]
    loc = incidents[2]
    nature = incidents[3]
    inc_ori = incidents[4]
    temp = []

    # Splitting and re-arranging data into tuple format for easy insertion using executemany
    for i in range(len(dttime)): # Total pages in the PDF
        for j in range(len(dttime[i])): # Entries per page
            temp.append((dttime[i][j], inc_no[i][j], loc[i][j], nature[i][j], inc_ori[i][j]))
    
    # Data insertion
    cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", temp)
    db.commit() # Committing to save changes to DB
    
    return db


def status(db):

    cur = db.cursor()
    
    # Pulling 'nature' type and frequency from DB
    res = cur.execute("SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY COUNT(*) DESC, nature ASC")
    
    global bl
    bl = []

    for t in res.fetchall():
        #if t[0]==' ': # Handling blank nature case
            #bl.append(t[1])
            #continue
        print(f'{t[0]} | {t[1]}', end='\n')
    
    #for t in bl: # Printing blank nature case
        #print(f'  | {t}', end='\n')
    
    db.close() # Closing DB connection


def main(url):

    #Downloading data
    incident_data = fetchincidents(url)

    # Extracting data
    incidents = extractincidents(incident_data)
	
    # Creating new database
    db = createdb()
	
    # Inserting data
    db = populatedb(db, incidents)
	
    # Printing incident 'nature' frequencies
    status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
