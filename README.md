# laroche-bluegrass-2026

Analyses the Laroche Bluegrass festival website to generate a calendar of events.
This can then we subscribed to via a TinyURL proxy: https://tinyurl.com/LaRoche2026

festival_v2.py uses the openpyxl library to build the formatted Excel spreadsheet with all five tabs
generate_ics.py uses only Python's built-in datetime library to generate the .ics calendar file - no external dependencies needed

If you ever want to run them yourself locally you'd just need Python installed and pip install openpyxl for the spreadsheet one.
The ICS script needs nothing beyond standard Python.
