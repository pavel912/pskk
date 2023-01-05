# PSKK project
This is a repository with the source code of PSKK platform

### Currently the platform's web interface contains:
1. Login page
2. Account creation page
3. User's personal page, where user can:
    1. Edit his personal data and password
    2. View his projects (TBD)
    3. Logout

### Code structure consists of:
1. Main file: app.py, where routing is performed
2. Util files:
    1. Data_Vlidator.py, where input data from user is validated 
    2. DB_Handler.py, where database operations are performed
3. Entities:
    1. User.py - user entity, connected to USER table in DB
4. DB:
    1. pskk_db - sqlite database for storing entities
5. Templates:
    1. create.html - user creation page
    2. login.html - login page
    3. update_data.html - editing data page
    4. update_password.html - editing password page
    5. userpage.html - user's personal page
