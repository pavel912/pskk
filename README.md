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
1. Main files:
   1. app_db.py - Flask app and DB init
   2. route.py - routing definition
2. Util files:
   1. Data_Validator.py, where input data from user is validated
3. Entities:
   1. User.py - personal user entity, connected to "persona_user" table in db
   2. Company.py - company entity, connected to "company_user" table in db
   3. Project.py - project entity, connected to "project" table in db
   4. ProjectStatus.py - status of a project, connected to "project_status" table in db
   5. Skill.py - skill entity, which can be owned by personas and companies; connected to "skill" table in db
   6. News.py - news entity, connected to "news" table in db
   7. Associations.py - tables-associations between entities
4. DB:
   1. pskk_db - sqlite database for storing entities
5. Templates:
   1. create_user_account.html - user creation page
   2. login.html - login page
   3. update_userdata.html - editing data page
   4. userpage.html - user's personal page
   5. index.html - main page
   6. post.html - news page
   7. projects.html - list of projects
6. Content - news templates


TODO:
1. Add pages design
2. Admin pages
3. Project pages
4. Company creation page
5. Superuser right
