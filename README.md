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
