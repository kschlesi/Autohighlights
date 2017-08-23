#### Simplifying the art of social media sharing
-----------------------------------------------
#### Check out the web app at [autohighlights.us](http://autohighlights.us)
-----------------------------------------------

### About
How do you choose the perfect quote to headline your latest social media post? This repository contains a Flask web app that recommends compelling quotes from online articles.

The app uses a supervised machine learning model, trained on reader-annotated articles from medium.com, to predict which passages from your article will draw the most reader engagement.

### Organization
 - `master` branch contains the deployed version of the web app, currently hosted on AWS.
 - `dev` branch contains small changes to master and serves as the starting point for prototyping, debugging, and launching new feature integrations.
 - `autoscrape` branch implements a feature that allows for scraping and analyzing text from completely unknown articles. Testing is still underway before final deployment of this feature.
 
### More Info
 - For more info about the creator, see [kschlesi](http://kschlesi.github.io)
 - For more info about the project, see the slides at [autohighlights](https://docs.google.com/presentation/d/1mIC-t_Uozi1fYdcNjJoZ6_mtEiWBWJBqrRgWVj0L65E/present?slide=id.p)
