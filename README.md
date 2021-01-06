<<<<<<< HEAD
# OneTable Django Test App


### Background

OneTable is a test project for exploring the Django framework. It is a quick way for users to creating organizations and apps where they create forms and add records. This project will help to explore Django's unique ORM and powerful querying mechanism, frontend template languge, user management, and Rest Framework project. 

Developing this app will help us with the following:

1. Test to see if Django ORM / Postgres / etc configuration meets minimum performance needs for managing large datasets and simple interfaces / template rendering. Much of our work involves large, relational datasets and help clients to more quickly store and organize this information outside of spreadsheets like Excel or Google Sheets.

2. If we confirm that Django meets the performance needs we expect in #1, use Django, and the architecture / principles developed for this project to prototype concepts and test with clients over the next year.

3. If any ideas from #2 work well or seem to have some traction, we'll do a follow up performance test for the Django Rest Framework to determine if Django can be made into a suitable backend for large apps with a strong focus on data management / data processing / ML / etc.

4. If Django is suitable for #3, we'll likely replace the frontend of any larger / longer term apps with Angular on the Django Rest API

5. If Django is not suitable for #3, we'll replace entire app backends with Spring, if / once the ideas from #2 are actually proven to be a good idea 

Ultimately, spending some time working with Django will allow us to verify if Django is a framework that is fast, cheap, and flexible to quickly proof concepts with clients. Right now, seems Django may be a good chance for this, and the OneTable concept will test this with an extreme use case (i.e. lots of records with embedded deep linking and export requirements).


--------------


### Structure

For now, the structure is simple --> over time we should develop standard practices for how we manage settings, templates, static files, etc.
In all cases at this stage, we should follow Django best practice, since the framework is mature / robust in feature sets, and it would be rare to find a use case for this project where Django has not solved in the past.

#### Core App
'Core' is the django app for main settings. In 'core', we set the django project settings, root urls, production / dev environment setup, and config for things like wsgi

#### Home App
'Home' is a normal django app. This app controls all of the styling (css, js, etc) as well as the template files and urls for the main website. Please note that the website is using SBAdmin template code which was just droppped into the project (no optimization) and just with some light edits to change colors. Longer term we can develop a library of css / js templates to use for clients. For now, using pre-built SBAdmin code is okay.

#### Other Notes
- Right now caching is not setup on the app - should probably implement redis at some point soon so we have that ready for other projects
- Whitenoise is being used for serving static files, which seems like the recommendation
- Static files used on the website (i.e. images on the homepage) are served from the same intance that hosts the app / as part of django, but S3 is used for user uploads when in production using the django-storages and boto3 libraries. In development, we don't use S3 -- just uploads to django project. I need to move the S3 credentials to environment variables in heroku so these are protected, once I create a new S3 bucket for this site.
- Have not added sitemaps for anything for SEO yet - not really needed at this time on a web app like OneTable with mostly internal pages.


--------------


### Models

Currently we have the following models that are core to the app's structure:

**Organization**: Highest level model storing information for the user's parent organization (group, company, team, etc).

**OrganizationUser**: Users who have access to / been added to an organization

**App**: A 'workspace' where users can create forms to store lists of objects with different fields

**AppUser**: Users who have access to / been added to an app

**List**: Parent object for naming and defining a 'form' to be created and used by a user for entering data

**ListField**: Definitions for the fields associated with and to be collected for each List

**Record**: Parent object for storing a List form entry saved by a user

**RecordField**: Field values saved for each ListField in a Record

_Note: right now, the concept of an OrganizationUser / AppUser does not use any of the Django roles and permissions frameworks but can / should be implemented with this in the future_


--------------


### Deployment

(Same as all Django projects)

- Make sure you are in a virtualenv
- Install everything from requirements.txt using ```pip3 install -r requirements.txt```
- Make sure you create a local database in your local postgres called 'one-table-local' (see the `core.settings.base.py` settings file)
- Run ```python3 manage.py makemigrations``` to create database migrations
- Run ```python3 manage.py migrate``` to create database tables / initial setup
- Run ```python3 manage.py createsuperuser``` to create an admin user
- Run ```python3 manage.py runserver``` for start the local server
- Access locally at http://127.0.0.1:8000/


--------------


### Deployment

- The app has been configured to be deployed on Heroku
- Automatic deployments are **not** configured on Heroku at this time through a webhook for the master branch
- There is a setup for dev and production, using an environment variable 'environment' on Heroku to designate 'production' settings should be used. There may be a better approach for switching between development and production settings (this is just an initial approach working for now)



=======
# OneTable
>>>>>>> dce99c064d39f8bb3cef7cc2f0b5b939e2df7b82
