# OneTable Django Test App


### Background

This app will help us with the following:

1. Test to see if Django ORM / Postgres / etc configuration meets minimum performance needs for managing large datasets and simple interfaces / template rendering. Much of our work involves large, relational datasets and help clients to more quickly store and organize this information outside of spreadsheets like Excel or Google Sheets.

2. If we confirm that Django meets the performance needs we expect in #1, use Django, and the architecture / principles developed for this project to prototype concepts and test with clients over the next year.

3. If any ideas from #2 work well or seem to have some traction, we'll do a follow up performance test for the Django Rest Framework to determine if Django can be made into a suitable backend for large apps with a strong focus on data management / data processing / ML / etc.

4. If Django is suitable for #3, we'll likely replace the frontend of any larger / longer term apps with Angular on the Django Rest API

5. If Django is not suitable for #3, we'll replace entire app backends with Spring, if / once the ideas from #2 are actually proven to be a good idea 

I want to find a framework that is fast, cheap, and flexible to quickly proof concepts with clients. Right now, seems Django may be a good chance for this, and the OneTable concept will test this with an extreme use case (i.e. lots of records with embedded deep linking and export requirements).

--------------


### Structure

For now, the structure is simple --> overtime we should develop standard practices for how we manage settings, templates, static files, etc.

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
- Automatic deployments are not configured on Heroku at this time
- There is a setup for dev and production, using an environment variable 'environment' on Heroku to designate 'production' settings should be used. There may be a better approach for switching between development and production settings (just an initial approach I tried)



