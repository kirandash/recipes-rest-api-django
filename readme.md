# RECIPES - REST API with Django

## 1. Intro
### 1.1 Tech Stack
1. **Python**:
    - Programming language
    - v 3.8.3
    - We will use python for writing Application logic and tests
    - Will use PEP-8 best practice guidelines to write python code. ex: max 79 chars per line etc
    - Automated code linting
2. **Django**:
    - Python web framework, easy to learn and helps build web apps rapidly
    - v 3.0.6
    - We will use **ORM** (Object Relational Mapper) from django to help in REST API creation. 
        - ORM helps us convert objects to database rows.
    - **Django Admin**: 
        - Provides out of the box admin site
        - Manage models
        - Visualize DB
3. **Django REST Framework**:
    - Extension to Django with tons of feature related to REST framework
    - Built in Authentication that can be used with endpoints
    - Viewsets: for creating REST API structure for all API endpoints
    - Serializers: 
        - for converting Django DB models into JSON objects and vice versa 
        - to add validations to API endpoints
    - Also provides browsable APIs so that we can test our API endpoints directly in browser.
4. **Docker**:
    - helps us Isolate project dependencies from the machine
    - Lightweight virtual machine
    - Single image: will wrap all our project using docker to create a single image that can be run on any m/c
    - Provides consistent dev environment across different machines
    - Helps in Deploying to cloud platform viz MS Azure / Google cloud
5. **Travis CI**:
    - Automated testing and linting
    - Email notification if build is breaking
    - Identify issue early
6. **PostgreSQL**:
    - Production Grade DB
    - Easy to setup with docker

### 1.2 TDD: Test Driven Development
1. **Unit Tests:**
    - Checks that our code works
    - Isolate specific code viz fns, class, API endpoints etc
2. **Test stages:**
    - **Setup**: create sample DB objects
    - **Execution**: Call the code with sample setup we did earlier
    - **Assertion**: Confirm expected o/p
3. **Why write tests?**
    - Expected in most professional dev teams
    - Makes it easier to change code
    - saves time in long run!
    - Testable, better quality code! Since each code block must be written with testing in mind. With specific i/p and o/p. Thus creating an easy to read code.
4. **Traditional dev vs TDD:**
    - Traditional development: implement feature ---> Write tests. TDD: Write tests ---> Implement feature to pass the test.
5. **Why TDD:**
    - Increases Test coverage
    - Ensures tests work
    - Encourages quality code
    - Stay focused

## 2. Project setup
### 2.1 Create Dockerfile, add Docker settings and Create docker image build
1. Create Dockerfile in root.
    - DockerFile contains all the dependencies of our project.
2. We can use existing images and add our dependencies to it instead of creating an entirely new one.
    - Go to https://hub.docker.com/
    - Search for Python
    - From list of tags: select 3.8-alpine (lightweight image of Docker)
3. Add settings to DockerFile
    - `FROM python:3.8-alpine` (Mandatory: which image we are using)
    - `MAINTAINER Kiran Dash` (Optional: who is maintaining the project)
    - `ENV PYTHONUNBEFFERED 1` (To tell Python to run in un buffered mode. ie not to buffer o/ps when running through Docker and print o/p directly)
    - `COPY ./requirements.txt /requirements.txt` (To copy requirements.txt file from our current folder to Docker image path)
    - `RUN pip install -r /requirements.txt` (Install all the requirements from Docker image)
    - `RUN mkdir /app` (Create a directory in docker img path to contain all our source code)
    - `WORKDIR /app` (Make the new app folder the default directory. ie: all our apps we will run using docker container will run starting from this location, unless specified)
    - `COPY ./app /app` (Copy code from our project directory to docker image)
    - `RUN adduser -D user` (Create a user with name user which will be used only to run processes for our project)
    - `USER user` (to switch to the new created user)
        - The reason we are creating a new user to run our docker image and not using the root user is because of security. If in future, the security of this user for our app is compromised then the hacker will have access to only this docker image. If we had used root user, then the hacker will have access to this docker image plus other docker images as well. Thus to limit the damage only to this docker image, create user specific to this Docker File.
4. Create requirements.txt file and add all list of dependencies available in pypi
    - Search for **django** in https://pypi.org/. Check the latest version. https://pypi.org/project/Django/ It is 3.0.6 right now.
    - Add `Django>=3.0.6,<3.1.0` to req....txt file. This makes sure that we have the latest Django ie 3.0.6 and in future if any security patches comes: we will still be using that. Thus we added support till 3.1.0. But we don't want any version upgrade as that might cause our app to break. Thus, avoiding 3.2 version.
    - Search for **djangorestframework** in pypi (python package index) Note: don't search for django-rest-framework. It wl give other results.
    - We will use djangorestframework 3.11.0 https://pypi.org/project/djangorestframework/
    - Add `djangorestframework>=3.11.0,<3.12.0` to get latest version + all latest minor versions till next major version
5. Create empty folder app in project directory. Note: running docker without the folder will throw an error.
6. **Build docker**: In terminal run: `cd recipes-rest-api-django` and `docker build .`.
    - The build will be relatively faster bcoz we are using alpine image which is a lightweight docker image for python.
    
### 2.2 Configure Docker Compose (docker-compose.yml file)
1. Dockercompose: A tool that helps us run our docker image easily from our project location.
    - Helps us run all the services that our project uses. Ex: python, DB etc
2. Create docker-compose.yml file.
    - yml file with all the services that our project will contain.
3. Add code
    - `version: "3"` latest docker compose version can be verified at: https://docs.docker.com/compose/compose-file/
    - `context: .` build context should be current directory
    - `ports: 8000:8000` map port 8000 from project to 8000 docker image
    - `volume - ./app:/app` maps app directory from our project into app directory on docker image. This is to make sure that when we change anything in our code base, it automatically reflects on docker image.
    - `sh -c "python manage.py runserver 0.0.0.0:8000"` shell run command python server.
4. **build docker-compose**: Go to terminal and run: `docker-compose build`
    - It builds our image using docker-compose configuration.
    - o/p should be `Successfully tagged recipes-rest-api-django_app:latest`. Thus our docker image is tagged to our project.
    
### 2.3 Create Django Project using docker-compose
1. From root, recipes-rest-api-django where docker-compose file is present: Run: `docker-compose run app sh -c "django-admin.py startproject app ."`
    - Running the command on app service (the only service we have now). And then executing shell command to create a django project with name app in the current working directory WORKDIR which is app as mentioned in Dockerfile.
    
### 2.4 Enable Travis CI for project on github
1. Travis is a Continuous integration tool that helps us run some automation testing every time we push some code on github.
2. Setting up Travis CI:
    - https://travis-ci.org sign up with github
    - https://travis-ci.org/account/repositories: select the project from github and activate
    - Now our project will be automatically picked up

### 2.5 Create Travis CI configuration file for project
1. Travis ci conf file tells travis what to do when we push any commit from our project
2. Create .travis.yml file in root. and add settings:
    - `language: python`
    - `python: "3.8"`: check for latest version at: https://docs.travis-ci.com/user/languages/python/
    - `services: docker` we will just run our docker service and docker will handle everything else
    - `before_script: pip install docker-compose`: scripts to run before running main script: in our case install docker-compse
    - `script: docker-compose run app sh -c "python manage.py test && flake8"`: run test and flake8. flake8 is a linting tool
3. Add flake8 to requirements.txt
    - check latest version on pypi: https://pypi.org/project/flake8/
4. Add flake8 conf to root. Create .flake8 file.
    - Exclude certain files that we don't need to check
5. Check the build at: https://travis-ci.org/github/kirandash/recipes-rest-api-django
6. Also run a build locally for flake8 to install: `docker-compose build`. Note: every time a new requirement is added, run build once for installation.

## 3. Intro to TDD
### 3.1 Writing a simple Unit test using Django TestCase
1. Create app/calc.py file to write basic addition
2. Create a new file app/tests.py file for unit tests
    - Note: Django unit test script by default looks for any file/folder that begins with test and runs them.
    - Create CalcTests class inherited from TestCase
    - Note: all methods in class also must start with test_ Ex: test_add_numbers
3. Terminal: `docker-compose run app sh -c "python manage.py test"`

### 3.2 Writing a unit test with TDD
1. TDD Approach: Write test first and then build the functionality.
2. Add test case to app/tests.py. Run test with `docker-compose run app sh -c "python manage.py test"`. Make sure test fails.
3. Add subtract method to app/calc.py. Run test to make sure test pass.
4. To check linting issues as well: Run test with flake `docker-compose run app sh -c "python manage.py test && flake8"`
5. Pros of TDD: 
    - We now know that our test is working. as we start with a failed test and then write code to make it pass
    
## 4. Configure Django Custom User model
### 4.1 Create core app
1. Core app: will contain all the central code which will then be used/shared in the sub apps. Ex: Migrations, DB etc.
2. Create app: `docker-compose run app sh -c "python manage.py startapp core"`
    - Add 'core' to INSTALLED_APPS list in settings.py file
3. Clean up: 
    - core/tests.py: later will add tests in separate tests/folder. Note: for running tests, either have test file or test folder. Having both will create error. So, we will use the folder approach.
    - core/views.py: we don't need any view in core app. Since we will not serve anything
4. Create core/tests/__init__.py: will add tests here.

### 4.2 Add tests for Custom user model using django TestCase
1. The default user model from Django needs username, email, password to create a new user. We will customize User model to not require username and just create new user with email and password. As per TDD, first 
2. core/test/ - create test_models.py file
3. Add test case for test_create_user_with_email_successsful fn
4. Run test and make sure it is failing with message username is required. Since default create_user method needs username.

### 4.3 Implement Custom user model
1. Let's create custom user model so our test case can pass.
2. core/models.py
    - create UserManager extending from BaseUserManager
    - Create User model class
3. app/settings.py file: add settings for custom user model
4. Run migrations: `docker-compose run app sh -c "python manage.py makemigrations core"`. Note: always better to mention app name in migration command. It will create the migrations/ files which will then be used to create fields in DB.
5. Run test: `docker-compose run app sh -c "python manage.py test && flake8"`

### 4.4 Normalize Email address
1. Create test in test_models.py file for the feature: normalizing email address. By default, email field is case sensitive. We want to change that feature and make it case insensitive by transforming the entered data into lowercase.
    - Add test_new_user_email_normalized fn
    - Run test to make sure it fails
2. Implement feature in core/models.py file
    - Run test to make sure it pass
    
### 4.5 Add validation for email field
1. Add test in test_models.py for validation. Feature: If no email is provided during user creation, django must return a ValueError.
    - Add test_new_user_invalid_email test case
    - Run test to fail with "AssertionError: ValueError not raised"
2. Implement feature in core/models.py
    - if there is no email, raise a ValueError
    - Run test to check for pass
    
### 4.6 Add support for creating super user
1. By default we can create a super user using terminal. Now, we will add this functionality in our custom model, so that we can create a super user using user manager. And it should be set as staff by default.
2. Add test to test_models.py file
    - test case: test_create_new_superuser
    - Run test to fail with "AttributeError: 'UserManager' object has no attribute 'create_superuser'"
3. Implement feature in core/models.py

## 5. Setup Django Admin
### 5.1 Add tests for listing users in admin
1. Create tests/test_admin.py
    - Create AdminSiteTests class. Create test case test_users_listed: to see if users are listed on an admin page: admin:core_user_changelist
    - In setup: create a test client. Read more at https://docs.djangoproject.com/en/2.2/topics/testing/tools/#overview-and-a-quick-example
    - Read more about Django admin at: https://docs.djangoproject.com/en/2.1/ref/contrib/admin/
    - Run test. Should fail with "NoReverseMatch: Reverse for 'core_user_changelist' not found. 'core_user_changelist' is not a valid view function or pattern name."


