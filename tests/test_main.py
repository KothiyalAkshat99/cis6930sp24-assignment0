import pytest
import sys
import os
from pathlib import Path
from urllib.request import urlopen

assignment0_path = Path(__file__).parent.parent / 'assignment0'

sys.path.append(str(assignment0_path))

import main


url = ['https://www.normanok.gov/sites/default/files/documents/2023-12/2023-12-01_daily_incident_summary.pdf',
       'https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-07_daily_incident_summary.pdf',
       'https://www.normanok.gov/sites/default/files/documents/2024-02/2024-01-31_daily_incident_summary.pdf',
       'https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-25_daily_incident_summary.pdf']

global response, incidents
response = []
incidents = []

# Test for Fetching Data from test URLs
def test_fetchincidents():
    
    for i in url:
        try:
            tresponse = main.fetchincidents(i)
            response.append(tresponse)
            assert True
        
        except Exception as e:
            print("Error while fetching data from URL "+ str(e), file=sys.stderr)
            assert False


# Test for Extracting Incident Data from test URLs
def test_extractincidents():

    for i in response:
        #response = main.fetchincidents(i)

        try:
            tincidents = main.extractincidents(i)
            incidents.append(tincidents)
            assert True

        except Exception as e:
            print("Error while extracting data "+ str(e), file=sys.stderr)
            assert False


# Test for Creating DB
def test_createdb():
    
    try:
        db = main.createdb()
        assert db

    except Exception as e:
        print("Error while creating database "+ str(e), file=sys.stderr)
        assert False


# Test for Populating DB
def test_populatedb():

    db = main.createdb()

    for i in incidents:
        try:
            db = main.populatedb(db, i)
            assert db
        
        except Exception as e:
            print("Error while inserting into database "+ str(e),file=sys.stderr)
            assert False


# Test for Final Status Check/ Output
def test_status():

    db = main.createdb()

    try:
        main.status(db)
        assert True
    
    except Exception as e:
        print("Error while printing to stdout"+ str(e),file=sys.stderr)
        assert False