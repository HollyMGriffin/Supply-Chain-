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


Logins (prototype only, passwords are stored in plaintext):
- manager / 1234: Supply Chain Manager, sees every order and can add, edit and cancel
- warehouse / 1234: Warehouse Manager, view only, sees In Transit and Delivered orders
- employee / 1234: Employee, view only, sees Delivered orders

Users are created in schema.sql. The app runs database setup on start, which also
upgrades older databases to allow the 'In Transit' status.
Roles and permissions are in auth.py.
