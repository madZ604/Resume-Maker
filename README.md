# Resume Maker
#### Video Demo:  <https://youtu.be/iT_fu2OPD-w>
#### Description:
Objective: To create a website/page for users to generate a basic resume based on the information they enter

File included in project:
    - templates: consists of all static html pages
    - application.py: consists the main python code
    - resume.db: database for resume maker consists of the tables "data" and "account"
    - styles.css: css style sheet for the templates
    - README.md: a description of the project

### templates:
    - layout.html
    consists of the basic layout of all the html pages required for this project, is extended to all other html pages
    - login.html
    consists of the html code for the login page
    - register.html
    before the user logs in, they have to register an account for themselves that's what register.html is for
    - edit.html
    consists of the html code for the page in which the details of the resume
    - resume.html
    consists of the html code for the page which displays the users resume
    - error.html
    used for displaying errors in the main application

### resume.db
    Consists of 2 tables:
        - data: for storing account usernames and passwords
        - account: for storing details from the user for their resume

### application.py
    - login_required(f):
        This function decorates routes to require login

    - error(message, code=400)
        Used to display error messages for missing username, incomplete forms, etc.

    - login():
        This function is used log in the user who has already registered. It accepts two methods,
        GET and POST. The GET method simply shows the login page, while the POST method makes sure
        the fields are filled before logging in. If person hasn't registered or enters wrong username/password,
        error is thrown.

    - register():
        This function is used to register people who do not have an account yet. This too accepts GET
        and POST methods. The GET method is to display the registration form. The POST method is for
        making sure all the fields have been entered and to register and save the details in the data base
        for when the user wants to login.

    - edit():
        This function is only reachable when user has logged in. On filling in the form for editing resume
        details, this function basically saves the information entered by the user into the database. If any
        field is left blank, an appropriate error is thrown. Accesible only after login.

    - view():
        Here, the data collected through edit() is returned to resume.html, to display the resulting resume.
        Accessible only after login.

    - logout():
        Used for looging the user out by clearing out the session data.