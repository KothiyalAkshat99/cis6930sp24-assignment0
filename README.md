# cis6930sp24-assignment0

Name:Akshat Kothiyal

# Assignment Description (in your own words)
This assignment is aimed towards successful data extraction from an online source in the form of a pdf and then reformatting the data according to needs.
We're using Python, SQL for program code and database purposes.


# How to install
pipenv install PyMuPDF

## How to run
pipenv run python assignment0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-07_daily_incident_summary.pdf

https://github.com/KothiyalAkshat99/cis6930sp24-assignment0/assets/143772575/8c37915a-df20-4831-afd1-c1d0a994b3da




## Functions
#### main.py \ - main function to call all other functions 

#### fetchincidents(url) - 
This function takes the pdf URL which has been provided through Command line arguments to fetch pdf data from the URL and returns this it back to main() in the form of an in-memory binary stream, instead of writing the file to disk locally.

#### extractincidents(incident_data) - 
This function takes the data returned from the fetchincidents() function and extracts raw text from this in-memory binary stream, and changes it into a format that is ready to be inserted into the database. For our use case, it also removes extraneous info which is not required from pdf pages and also handles some edge cases. This data which is extracted is split into - datetime, incident number, location, nature, incident ori. This function returns a single list 'incidents' which comprises of 5 sublists which are mentioned in previous line.

#### createdb() = 
This function creates a new database and establishes a connection, and creates a new table 'incidents' in this database. The function returns the connection object created.

#### populatedb(db, incidents) - 
This function takes the database connection object returned by the createdb() function and the incident list returned from the extractincidents() functions. It takes data from the list for each of the five columns and inserts them into the database. The function returns the database connection object back to main.

#### status(db) - 
This function takes the database connection object and uses it to query the database using SQL and outputs a list of nature of incidents along with their frequencies to standarad out.

## Database Development
Database used for this assignment is SQLite3. It is imported into Python as a module using 'import sqlite3'. 

From the code, function 'createdb()' creates the database and connection, alongwith the required 'incidents' table. Function 'populatedb()' inserts tuples into the database for the required columns - incident_time, incident_number, location, nature, incident_ori. Function 'status()' queries the database to fetch required data for outputting to standard out.

## Bugs and Assumptions
No apparent bugs according to testing on local system.

### Assumptions made - 
Only 'location' has 'multi-line' data in edge cases; 
Only 'location' and 'nature' have blank data in edge cases;
Assumptions on consistency of the pdf which is being supplied. If pdf creation consistency changes, code might break.
