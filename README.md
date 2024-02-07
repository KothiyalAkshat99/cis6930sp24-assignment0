# cis6930sp24-assignment0

Name: Akshat Kothiyal <br>
UFID: 53292487

# Assignment Description
This assignment is aimed towards successful data extraction from an online source in the form of a pdf, and data reformatting and database insertion according to needs.
We're using Python, SQL for program code and database purposes.


# How to install
pipenv install PyMuPDF
pipenv install pytest

## How to run
pipenv run python assignment0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-07_daily_incident_summary.pdf

https://github.com/KothiyalAkshat99/cis6930sp24-assignment0/assets/143772575/8c37915a-df20-4831-afd1-c1d0a994b3da



## Functions
#### main.py(url) - 
Main function to call all other functions. Takes a url argument from command line call.

#### fetchincidents(url) - 
This function takes the pdf URL which has been provided through Command line arguments to fetch pdf data from the URL and returns this it back to main() in the form of an in-memory binary stream, instead of writing the file to disk locally.

#### extractincidents(incident_data) - 
This function takes the data returned from the fetchincidents() function and extracts raw text from this in-memory binary stream, and changes it into a format that is ready to be inserted into the database. For our use case, it also removes extraneous info which is not required from pdf pages and also handles some edge cases. This data which is extracted is split into - datetime, incident number, location, nature, incident ori. This function returns a single list 'incidents' which comprises 5 sublists which are mentioned in previous line.

I have used 'PyMuPDF'/ 'Fitz' module to extract data from the pdf. The module allows us to extract blocks of information from the pdf and extract the content from inside these blocks. The get_text("blocks") method returns the following information -<br>
1. x0, y0, x1, y1: Coordinates defining the bounding box of the text block.
2. lines: A list of strings representing the lines of text within the block.
3. bbox: Similar to x0, y0, x1, y1, providing the bounding box of the text block.
4. char_count: Total character count within the text block.

I used the 'lines' portion to extract the text from these blocks/lines of text and then split them into the 5 columns as required in our usecase.

This function extractincidents also handles edge cases for blank 'location', 'nature', and also other edge case where Location has multi-lined values.

#### createdb() -
This function creates a new database and establishes a connection, and creates a new table 'incidents' in this database. The function returns the connection object created.

#### populatedb(db, incidents) - 
This function takes the database connection object returned by the createdb() function and the incident list returned from the extractincidents() functions. It takes data from the list for each of the five columns, joins them into tuple format, and inserts them into the database. The function returns the database connection object back to main.

#### status(db) - 
This function takes the database connection object and uses it to query the database using SQL and outputs a list of nature of incidents along with their frequencies to standarad out.



## Database Development
Database used for this assignment is SQLite3. It is imported into Python as a module using 'import sqlite3'. 

From the code, function 'createdb()' creates the database and connection, alongwith the required 'incidents' table. Function 'populatedb()' inserts tuples into the database for the required columns - incident_time, incident_number, location, nature, incident_ori. Function 'status()' queries the database to fetch required data for outputting to standard out.



## Bugs and Assumptions
No apparent bugs in actual code according to testing on local system.

During testing using PyTest, bugs found with importing package/ main.py into pytest file for actual testing. Found a solution to add parent path to sys.path. Might bug out in other environments. Needs more testing/ or an alternate approach.

### Assumptions made - 
Only 'location' has 'multi-line' data in edge cases; <br>
Only 'location' and 'nature' have blank data in edge cases; <br>
Assumption that PDF url actually links to a pdf which hasn't been removed by Norman PD; <br>
Assumptions on consistency of the pdf which is being supplied. If pdf creation consistency changes, code might break.



## Testing using PyTest

### How to run tests:
pipenv run python -m pytest

### Test Functions:

#### test_fetchincidents() - 
This function tests fetchincidents(url) for multiple URLs and aptly handles exceptions.

#### test_extractincidents() - 
This function tests extractincidents(incident_data) for multiple incident data responses recorded from previously provided URLs, and handles exceptions if there are any issues with data extraction from these incidents

#### test_createdb() -
Tests the createdb() function to check if DB and table are being created or if there are any exceptions.

#### test_populatedb() - 
Tests if the Database is being populated by the populatedb(db, incidents) method by supplying the dabatabase connection object and incident data which has been split into 5 columns as per the returned object from extractincidents(incident_data)

#### test_status() - 
Tests if there are any issues when status(db) pulls data from the database and writes it to stdout.

### Test Results and Observations - 
All tests ran successfully.



## Linux Environment Test (Google Cloud VM)

### Tested main.py, pytest on Python 3.11

![DE_Assignment0_Linux_1](https://github.com/KothiyalAkshat99/cis6930sp24-assignment0/assets/143772575/b66c243e-e5b8-4ea9-a8d7-08eee21b2b97)

![DE_Assignment0_Linux_2](https://github.com/KothiyalAkshat99/cis6930sp24-assignment0/assets/143772575/219c2644-5b5f-4a34-95c6-6f986cac5ba0)
