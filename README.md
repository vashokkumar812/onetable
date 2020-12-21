# [Website Name]


### Background

Lorem ipsum

TODO list:
- User profile account
- Ajax responses, editing, etc.
- Managing the form on the front end and saving
- Editing records they are saved


--------------


### Structure

Lorem Ipsum

#### Core App
'Core' is the django app for main settings. In 'core', we set the django project settings, root urls, production / dev environment setup, and config for things like wsgi

#### Home App
'Home' is a normal django app. This app controls all of the styling (css, js, etc) as well as the template files and urls for the main website. Please note that the website is using SBAdmin template code which was just droppped into the project (no optimization) and just with some light edits to change colors. Longer term we can develop a library of css / js templates to use for clients. For now, using pre-built SBAdmin code is okay.


--------------


### Architecture

- Right now caching is not setup on the app - should probably implement redis at some point soon so we have that ready for other projects
- Whitenoise is being used for serving static files, which seems like the recommendation
- Static files used on the website (i.e. images on the homepage) are served from the same intance that hosts the app / as part of django, but S3 is used for user uploads when in production using the django-storages and boto3 libraries. In development, we don't use S3 -- just uploads to django project. I need to move the S3 credentials to environment variables in heroku so these are protected, once I create a new S3 bucket for this site.
- Have not added sitemaps for anything for SEO yet - will add that soon


--------------


### Deployment

- The app has been configured to be deployed on Heroku
- Note that anything pushed to the 'master' branch will trigger a deployment automatically on heroku
- There is a setup for dev and production, using an environment variable 'environment' on Heroku to designate 'production' settings should be used. There may be a better approach for switching between development and production settings (just an initial approach I tried)
