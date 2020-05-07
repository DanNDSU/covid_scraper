# COVID-SCRAPER
A Django application that builds a distributed web scraper.
Consists of three identical server files that return a filtered list of scraped
websites, along with the first paragraph element in each site that contains
either "covid-19" or "coronavirus."
Also consists of the web app that manages these servers and displays the results.

# Dependencies
This website depends on three python modules: django, requests, and beautifulsoup4.
While you can install each directly using pip install _____, it is much more
recommended to use pipenv for this. Pipenv creates a virtual environment
and installs the dependencies in that environment, so your computer
does not become full of extraneous modules installed globally.

## To use pipenv:
Install pipenv with $ pip install pipenv
cd into covid_scraper with $ cd covid_scraper
initiate environment and dependencies: $ pipenv install
start up the environment: $ pipenv shell

You'll know the environment is created and running when (covid_scraper)
appears to the left of the terminal prompt.
To exit your pipenv environment, type exit into the terminal.

# Running the application
## Start the servers.
In one terminal, cd into covid_scraper, then $ pipenv shell
Start the first server with $ python server12345.py

Start two more terminals, and do the same, except with
$ python server12346.py
$ python server12347.py

## Start Django
In another terminal (you'll have four total),
cd into covid_scraper, then $ pipenv shell, then cd into scraper_project

### Create User Account
With the terminal in the scraper_project directory,
run $ python manage.py createsuperuser
and respond to the prompts to make your username and password
you can skip entering an e-mail address.

start Django with $ python manage.py runserver

This will allow you to access the website at localhost:8000/
