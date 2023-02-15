# PSKK project
This is a repository with the source code of PSKK platform

### Currently, the platform's web interface contains:
1. Main page with news
2. Login page
3. Account creation page
4. User's personal page, where user can:
   1. Edit his personal data and password
   2. View his projects (TBD)
   3. Logout

### Code structure consists of:
1. Main file: app.py, where routing is performed
2. Util files:
   1. Data_Validator.py, where input data from user is validated 
   2. DB_Handler.py, where database operations are performed
3. Entities:
   1. User.py - personal user entity, connected to "persona_user" table in db
   2. Company.py - company entity, connected to "company_user" table in db
   3. Project.py - project entity, connected to "project" table in db
   4. Skill.py - skill entity, which can be owned by personas and companies; connected to "skill" table in db
   5. Base.py - base class
   6. Associations.py - tables-associations between entities
4. DB:
   1. pskk_db - sqlite database for storing entities
5. Templates:
   1. create.html - user creation page
   2. login.html - login page
   3. update_data.html - editing data page
   4. update_password.html - editing password page
   5. userpage.html - user's personal page
   6. index.html - main page
   7. post.html - news page
   8. projects.html - list of projects
6. Content - news templates


TODO:
7. Add pages design
