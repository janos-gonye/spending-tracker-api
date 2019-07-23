# Spending Tracker API

This small [Flask](https://palletsprojects.com/p/flask/) application helps you **track your expenses**.
You can clone, configure and deploy your own instance (to [Heroku](https://www.heroku.com/) or elsewhere) *without any major (or minor) company monitoring what you spend your money on*.

> You can find the corresponding front end application [here](https://github.com/janos-gonye/spending-tracker-cross-platform-front-end). (Or you can write your own if you please...)

#### What you can do with it
 - Create categories and subcategories of any category.
 - Add transactions to categories.
 - Show statistics and export it to JSON format which sent automatically to your registered email address.
 - Users can register by email address which must be confirmed. So your friends, family members or girlfriend can use it, too.

> *Please note, it's just a hobby project, not an enterprise application.*  
> *Though, I think you knew this... :-)*

## Setup for development on Ubuntu (basically any Linux)

**Setup database**  
You can use any database supported by [SQLAlchemy](https://www.sqlalchemy.org/).
I use personally [PostgreSQL](https://www.postgresql.org/).  
The following lines contain how to install PostgreSQL and setup a database for this application.  
*Tested on Ubuntu 18.04.*

Install PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```
Test if it works...
```bash
sudo -u postgres psql
\q
```

Create database and role for *spending-tracker-api*  
*Tested on Ubuntu 18.04 with PostgreSQL version 10.9'*
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE <your-db-name>;
CREATE USER <your-db-user-name> WITH ENCRYPTED PASSWORD '<your-db-user-password>';
GRANT ALL ON DATABASE <your-db-name> to <your-db-user-name>;
\q
```

Navigate to the directory you'd like to store the application in
```bash
cd /<path>/<to>/<your>/<projects>/<directory>
```

Clone the project  
Project name is optional. Default: 'spending-tracker-api'
```
git clone https://github.com/janos-gonye/spending-tracker-api.git <project-name>
cd ./<project-name>
```

Create and activate your virtual environment  
*Tested with Python 3...*
```bash
sudo apt-get install virtualenv
virtualenv -p python3 <virtual-environment-name>
source ./<virtual-environment-name>/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

Set the folllowing environment variables
```bash
"HOST": "<your-host>"                                                             # 0.0.0.0 for dev
"PORT": "<your-port>"                                                             # Default: 5000
"FLASK_APP": "run.py"
"FLASK_DEBUG": "<your-flask-debug>"                                               # <1> or <0>
"ENV": "<your-env>"                                                               # <development> or <production>
"DEBUG": "<your-debug>"                                                           # <True> or anything else (<False>)
"SECRET_KEY": "<your-secret-key>"
"MAIL_SERVER": "<your-mail-server>"                                               # <True> or anything else (<False>) https://support.google.com/a/answer/176600?hl=en
"MAIL_PORT": "<your-mail-port>"                                                   # <True> or anything else (<False>) https://support.google.com/a/answer/176600?hl=en
"MAIL_USE_TLS": "<your-mail-use-tls>"                                             # <True> or anything else (<False>) https://support.google.com/a/answer/176600?hl=en
"MAIL_USE_SSL": "<your-mail-use-ssl"                                              # <True> or anything else (<False>) https://support.google.com/a/answer/176600?hl=en
"MAIL_DEBUG": "<your-mail-debug>"                                                 # <True> or anything else
"MAIL_MAX_EMAILS": "<your-max-email>"                                             # Integer number > 0
"MAIL_USERNAME": "<your-mail-username>"                                           # https://support.google.com/a/answer/176600?hl=en
"MAIL_PASSWORD": "<your-mail-password>"                                           # https://support.google.com/a/answer/176600?hl=en
"MAIL_DEFAULT_SENDER": "<your-mail-username>"                                     # https://support.google.com/a/answer/176600?hl=en
"SQLALCHEMY_DATABASE_URI": "<engine-configuration>"                               # https://docs.sqlalchemy.org/en/13/core/engines.html
"SQLALCHEMY_TRACK_MODIFICATIONS": "False"                                         # To silence a warning
"REGISTRATION_TOKEN_LIFETIME": "<your-registartion-token-lifetime>"               # As seconds, default: 86400
"CANCEL_REGISTRATION_TOKEN_LIFETIME": "<your-cancel-registartion-token-lifetime>" # As seconds, default: 86400
"LOGIN_TOKEN_LIFETIME": "<login-token-lifetime>"                                  # As seconds, default: 3600
```

Run server
```bash
flask run
```

## Setup for development on Windows
> Coming soon...

## API Endpoints

#### Registration
***[POST]** /api/auth/registration*
```json
{
	"username": "<string:username>",
	"password": "<string:password>"
}
```
***[GET]**  /api/auth/registration/confirm*

<hr>

#### Cancel Account
***[DELETE]** /api/auth/registration*

***[GET]** /api/auth/registration/cancel/confirm*

<hr>

#### Login

***[POST]** /api/auth/login*
```json
{
	"username": "<string:required>",
	"password": "<string:required>"
}
```
***[GET]** /api/auth/verify-token*

<hr>

#### CRUD Categories

***[GET]** /api/categories*

***[POST] /api/categories*
```json
{
	"title": "<string:required>",
	"description": "<string:optional>",
	"parent_id": "<string|null:optional>"
}
```
***[GET]** /api/categories/<int:category_id>*

***[PATCH]** /api/categeries/<int:category_id>*

```json
{
	"title": "<string:optional>",
	"description": "<string:optional>",
	"parent_id": "<string|null:optional>"
}
```
***[DELETE]** /api/categories/<int:category_id>*

<hr>

#### CRUD Transactions

***[GET]** /api/categories/<int:category_id  OR "\*">/transactions?from=<number|string:optional>&to=<number|string:optional>*

> *Query parameters 'from' and 'to' are UNIX time stamps and optional*

***[POST]** /api/categories/<int:category_id>/transactions*
```json
{
    "amount": "<number:required>",
    "processed_at": "<number|string:required>", // Unix Timestamp
    "comment": "<string:optional>"
}
```
***[GET]** /api/categories/<int:category_id>/transactions/<int:transaction_id>*

***[PATCH]** /api/categories/<int:category_id>/transactions/<int:transaction_id>*
```json
{
    "amount": "<number:optional>",
    "processed_at": "<number|string:optional>", // Unix Timestamp
    "comment": "<string:optional>"
}
```
***[DELETE]** /api/categories/<int:category_id>/transactions/<int:transaction_id>*

<hr>

#### Statistics

***[GET]** /api/statistics*

***[GET]** /api/statistics/export*

<hr>
<br>

*Thanks for reading,*  
*Johnny*
