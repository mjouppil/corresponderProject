# corresponderProject

### Introduction

Helsingin yliopiston kurssin TKT20019 - Tietokannat ja web-ohjelmointi harjoitustyö.

#### Name:
Corresponder.

#### Description:

An application dedicated to enable personal private correspondence between individuals.

#### Features:
- Users can create an account with login credentials and a separate username.
- Visibility of the account can be determined by the owner of the account.
- List of visible accounts can be searched.
- Users can send a request to visible users to add them as a contact. The request can be accepted or declined.
- Invisible users can create a token that can be send to some other party by extraneous means and used in the app by another user to send a contact request.
- Users can send messages to and receive from other users on their contact list.
- Messages are displayed as a time based ordered thread.
- Maybe also extra features such as group threads, message deletion, encrypted messaging etc. now or later on.

#### Setting up and running:

Get the source code.

Create .env-file to project root with following contents:
>DATABASE_URL="postgresql:///database_name"
> 
>SECRET_KEY="insert a secret key here"

Activate virtual environment and install project dependencies:

>$ python3 -m venv venv

>$ source venv/bin/activate

>$ pip install -r ./requirements.txt

Define database tables from schema.sql:

>$ psql (database_name) < schema.sql

Run the Flask application:

>$ flask run

Open the flask-webpage with your browser.

### Status on 22.10.2023:

#### Current status

- Almost ready. It is better than I expected.

#### Tips for testing

- You can register many users and try to connect them, send and respond to contact requests.
- You can create from the profile page a contact token for a user.
- Some other user can utilize it to connect with the token owner even though the user would be hidden from other users.
- Users can make new threads and add their contacts and start messaging.

#### For future development.

- Many many things, for example:
  - basic thread and message deleting,
  - admin right handling for threads,
  - encrypted messaging,
  - nicer user profile features, like images and colors
  - etc.
- There is a known bug, that sometimes when making a new thread, some of the users are not selectable from the list.

### Status on 8.10.2023:

#### Short setup:
- Get the source code and run (flask run).
- You can create a PostgreSQL-database based on schema.sql.

#### Testing in practice:
- You can register a new user.
- You can log in and out wit a registered user.
- Navigation bar doesn't do anything.
- If there are many users registered, it is possible to:
  - see visible users listed,
  - send them contact requests,
  - accept or decline contact requests.
  - Though these don't work wholly as supposed to at the moment.
- Threads and messages are not functional at the moment.

#### Work done:

- Expanded SQL-database tables and properties to cover almost all final functionalities.
- SQL-queries are further developed to cover most of user actions but not yet messaging actions.
- Passwords are now hashed.
- Introducing Bootstrap:
  - Nicer look and feel.
  - Preliminary navigation.
- Some structure changes in the code:
  - Routing and request handling better divided into modules.
- updated README.md

### Status on 24.9.2023:

#### Work done:
- basic imports and methods in app.py.
- added .env-file.
- added index.html.
- Login/logout-templates.
- Placeholders for "Contacts" and Message threads"-lists.
- installations for PostgresSQL.
- Update README.md.

#### Testing in practice:
- Get the source code and run (flask run).
- In the browser you can log in with any credentials and log out.
- Not much functionality (work very much in progress).
