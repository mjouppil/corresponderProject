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
