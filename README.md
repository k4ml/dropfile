Dropfile is a simple file sharing web app that allow people to upload any files (can be restricted to certain files only) and get a list of url alias for that file. The alias would be unique and can be passed to different people to download the same file.

On top of that, Dropfile provide basic tracking, such as when the file is downloaded and set expiry date on the alias.

No registration required to upload files for the initial version but sign up features will be added later.

## Quickstart

Download the source code repo with git:-

    git clone https://github.com/k4ml/dropfile.git
    python app.py

That will start a server at http://localhost:8080/ which you can access with browser.

## Usecase

* People selling ebook simply through email or payment processor that doesn't have the facility to send/serve the files after payment is done. The alias url can be given to customer once they have settle the payment.
* Quickly sharing files with friend with automatic expiring link.
* ...

## Get Involved

This project indeed aim to provide learning environment for web application development, while solving a real world problem. You'll be able to learn:-

* Cherrypy - Among the oldest python web framework, > 10 years being used in production websites.
* Peewee - Simple (single .py file only) but featureful Python ORM.
* Riotjs - A React-like user interface micro-library.
* Automated testing.
* Modern deployment approach. Easy to run in production setup is Dropfile main key principle.
