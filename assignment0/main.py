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

    doc = fitz.open(stream = incident_data, filetype="pdf")

    global dttime, inc_no, loc, nature, inc_ori
    dttime = []
    inc_no = []
    loc = []
    nature = []
    inc_ori = []

    for page_number in range(len(doc)):

        x = doc[page_number]
        text = x.get_text("text")

        if page_number == 0: # Replacing/ Removing Extraneous Info from PDF text extract
            text = text.replace('Date / Time', '')
            text = text.replace('Incident Number', '')
            text = text.replace('Location', '')
            text = text.replace('Nature', '')
            text = text.replace('Incident ORI', '')
            text = text.replace('NORMAN POLICE DEPARTMENT', '')
            text = text.replace('Daily Incident Summary (Public)', '')
    
        text = text.strip() # Trimming extra spaces
        tsplit = text.split('\n') # Splitting text into rows

        #page_number = 22
        if page_number == len(doc)-1: # Removing extraneous info from last page of PDF
            tsplit.pop(len(tsplit)-1)
        
        #print(type(tsplit))
        dttime.append(tsplit[0::5]) # Splicing for date and time
        inc_no.append(tsplit[1::5]) # Splicing for incident number
        loc.append(tsplit[2::5]) # Splicing for location
        nature.append(tsplit[3::5]) # Splicing for nature
        inc_ori.append(tsplit[4::5]) # Splicing for incident ORI
        #print(dttime)

    incidents = [dttime, inc_no, loc, nature, inc_ori]
    return incidents
    

def createdb():

    con = sqlite3.connect("normanpd.db") # Creating Database connection
    cur = con.cursor() # Database Cursor

    cur.execute("DROP TABLE incidents;")
    cur.execute("CREATE TABLE incidents (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT);")
    #res = cur.execute("SELECT name FROM sqlite_master;")
    #print(res.fetchone())

    #cur.execute("INSERT INTO incidents VALUES ('12/1/2023 23:36', '2023-00081308', '901 12TH AVE NE', 'Suspicious', 'OK0140200');")
    #con.commit()
    #res = cur.execute("SELECT * FROM incidents;")
    #print(res.fetchall())
    return con


def populatedb(db, incidents):

    #db = sqlite3.connect("normanpd.db")
    cur = db.cursor()

    dttime = incidents[0]
    inc_no = incidents[1]
    loc = incidents[2]
    nature = incidents[3]
    inc_ori = incidents[4]
    temp = []

    for i in range(len(dttime)): # Total pages in the PDF
        #cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", dttime[i], inc_no[i], loc[i], nature[i], inc_ori[i])
        for j in range(len(dttime[i])): # Entries per page
            #print (dttime[i][j], end='\n')
            #cur.execute("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)",)
            temp.append((dttime[i][j], inc_no[i][j], loc[i][j], nature[i][j], inc_ori[i][j]))
    #print(temp)
    cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", temp)
    db.commit()
    #res = cur.execute("SELECT * FROM incidents")
    #print(res.fetchall())
    return db


def status(db):
    #con = sqlite3.connect("normanpd.db")
    cur = db.cursor()
    
    res = cur.execute("SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY COUNT(*) DESC, nature ASC")
    for t in res.fetchall():
        print(f'{t[0]} | {t[1]}', end='\n')
    
    db.close()


def main(url):

    #url='https://www.normanok.gov/sites/default/files/documents/2023-12/2023-12-01_daily_incident_summary.pdf'

    #Download data
    incident_data = fetchincidents(url)

    # Extract data
    incidents = extractincidents(incident_data)
	
    # Create new database
    db = createdb()
	
    # Insert data
    db = populatedb(db, incidents)
	
    # Print incident counts
    status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)











