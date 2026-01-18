# SporeScraper
A tool for scraping, analysis and visualization of the contents of the spore.fandom.com page,
made as a final project for a university Python course.

The project was made in accordance with the CC-BY-SA licence attached to the fandom website.

### How to run
Create a Python virtual environment in and install dependencies in the folder where the program files have been downloaded.
```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```
Then input `python3 wiki_scraper.py [put arguments here]` to run.  
Type in `python3 wiki_scraper.py -h` for more information.

### How to test
Test modules for certain parts of the code can be found in the 'tests' folder.
To conduct a full test trial of the project, install project requirements 
as shown above, and then while inside the main project folder, run
```
pytest
```
in the created virtual environment.