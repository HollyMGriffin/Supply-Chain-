Installing flask: python -m pip install flask

Creating DB: python database.py

Start Application: python app.py

app.py is responsible for handling which html file to render and registering backend api blueprints

Flask API endpoints for orders should be created in orders.py inside the routes folder
Database operations should be handled in order_repository inside db folder
js files are inside static folder

Flask workflow: 
1. Javascript calls API endpoint and sends any necessary data
2. API endpoint handles and validates data
3. API calls a function in db_repo
4. db_repo handles db operations
5. API endpoint returns response in JSON format
6. Javascript processes response and updates webpage


Logins:
The database starts with one admin account. Log in with it, change its
password right away (Change Password in the sidebar), then create the
other accounts from the Accounts page.
- Username: admin
- Password: ChangeMe123

Roles:
- Admin: creates accounts, views all orders and inventory, cannot change them
- Supply Chain Manager: sees every order and can add, edit and cancel; views inventory
- Warehouse Manager: sees In Transit and Delivered orders; adds, edits and deletes inventory
- Employee: view only, sees Delivered orders

Passwords are salted and hashed with PBKDF2-SHA256 (passwords.py) before
they are stored. Every user can change their own password.
The app runs database setup on start. supply_chain.db is not kept in Git;
each person's copy is created the first time they run the app. If you have an
old supply_chain.db from before accounts were hashed, delete it and restart.
Roles and permissions are in auth.py.
