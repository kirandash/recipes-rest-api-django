# RECIPES - REST API with Django

## 1. Intro
### 1.1 Tech Stack
1. **Python**:
    - Programming language
    - v 3.8.3
    - We will use python for writing Application logic and tests
    - Will use PEP-8 best practice guidelines to write python code. ex: max 79 chars per line etc
    - Automated code linting
    - https://www.python.org/
2. **Django**:
    - Python web framework, easy to learn and helps build web apps rapidly
    - v 3.0.6
    - We will use **ORM** (Object Relational Mapper) from django to help in REST API creation. 
        - ORM helps us convert objects to database rows.
    - **Django Admin**: 
        - Provides out of the box admin site
        - Manage models
        - Visualize DB
    - https://www.djangoproject.com/
3. **Django REST Framework**:
    - Extension to Django with tons of feature related to REST framework
    - Built in Authentication that can be used with endpoints
    - Viewsets: for creating REST API structure for all API endpoints
    - Serializers: 
        - for converting Django DB models into JSON objects and vice versa 
        - to add validations to API endpoints
    - Also provides browsable APIs so that we can test our API endpoints directly in browser.
    - https://www.django-rest-framework.org/
4. **Docker**:
    - helps us Isolate project dependencies from the machine
    - Lightweight virtual machine
    - Single image: will wrap all our project using docker to create a single image that can be run on any m/c
    - Provides consistent dev environment across different machines
    - Helps in Deploying to cloud platform viz MS Azure / Google cloud
    - https://www.docker.com/
5. **Travis CI**:
    - Automated testing and linting
    - Email notification if build is breaking
    - Identify issue early
    - https://travis-ci.org/
6. **PostgreSQL**:
    - Production Grade DB
    - Easy to setup with docker
    - https://www.postgresql.org/

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
7. Read more about:
    - Dockerfile at https://docs.docker.com/engine/reference/builder/
    - Docker Hub at https://hub.docker.com/
    - Python package index at https://pypi.org/

### 2.2 Configure Docker Compose (docker-compose.yml file)
1. Docker Compose: A tool that helps us run our docker image easily from our project location.
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
5. More about Docker compose at: https://docs.docker.com/compose/

### 2.3 Create Django Project using docker-compose
1. From root, recipes-rest-api-django where docker-compose file is present: Run: `docker-compose run app sh -c "django-admin.py startproject app ."`
    - Running the command on app service (the only service we have now). And then executing shell command to create a django project with name app in the current working directory WORKDIR which is app as mentioned in Dockerfile.
2. Read more about 
    - `startproject` at: https://docs.djangoproject.com/en/3.0/ref/django-admin/#startproject
    - `docker-compose run` at: https://docs.docker.com/compose/reference/run/
    
### 2.4 Enable Travis CI for project on github
1. Travis is a Continuous integration tool that helps us run some automation testing every time we push some code on github.
2. Setting up Travis CI:
    - https://travis-ci.org sign up with github
    - https://travis-ci.org/account/repositories: select the project from github and activate
    - Now our project will be automatically picked up
3. Read more at: https://travis-ci.org/

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
7. More at: 
    - travis tutorial: https://docs.travis-ci.com/user/tutorial/
    - flake8: https://flake8.pycqa.org/en/latest/

## 3. Intro to TDD
### 3.1 Writing a simple Unit test using Django TestCase
1. Create app/calc.py file to write basic addition
2. Create a new file app/tests.py file for unit tests
    - Note: Django unit test script by default looks for any file/folder that begins with test and runs them.
    - Create CalcTests class inherited from TestCase
    - Note: all methods in class also must start with test_ Ex: test_add_numbers
3. Terminal: `docker-compose run app sh -c "python manage.py test"`
4. Read more abt:
    - Django unit tests at: https://docs.djangoproject.com/en/3.0/internals/contributing/writing-code/unit-tests/
    - assert methods at: https://docs.python.org/3/library/unittest.html#assert-methods
    - test methods at: https://docs.djangoproject.com/en/3.0/ref/django-admin/#test

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
5. Read more abt:
    - startapp at: https://docs.djangoproject.com/en/3.0/ref/django-admin/#startapp
    - https://docs.djangoproject.com/en/3.0/ref/settings/#installed-apps

### 4.2 Add tests for Custom user model using django TestCase
1. The default user model from Django needs username, email, password to create a new user. We will customize User model to not require username and just create new user with email and password. As per TDD, first 
2. core/test/ - create test_models.py file
3. Add test case for test_create_user_with_email_successsful fn
4. Run test and make sure it is failing with message username is required. Since default create_user method needs username.
5. Read more abt custom user model at: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model

### 4.3 Implement Custom user model
1. Let's create custom user model so our test case can pass.
2. core/models.py
    - create UserManager extending from BaseUserManager
    - Create User model class
3. app/settings.py file: add settings for custom user model
4. Run migrations: `docker-compose run app sh -c "python manage.py makemigrations core"`. Note: always better to mention app name in migration command. It will create the migrations/ files which will then be used to create fields in DB.
5. Run test: `docker-compose run app sh -c "python manage.py test && flake8"`
6. Docs:
    - `check_password`: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.check_password
    - `get_user_model`: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.get_user_model
    - **PermissionsMixin**: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.models.PermissionsMixin
    - **AbstractBaseUser**: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser
    - **BaseUserManager**: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager
    
### 4.4 Normalize Email address
1. Create test in test_models.py file for the feature: normalizing email address. By default, email field is case sensitive. We want to change that feature and make it case insensitive by transforming the entered data into lowercase.
    - Add test_new_user_email_normalized fn
    - Run test to make sure it fails
2. Implement feature in core/models.py file
    - Run test to make sure it pass
3. Docs:
    - https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager.normalize_email
    
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
4. Docs:
    - https://docs.djangoproject.com/en/3.0/ref/django-admin/#createsuperuser

## 5. Setup Django Admin
### 5.1 Add tests for listing users in admin
1. Create tests/test_admin.py
    - Create AdminSiteTests class. Create test case test_users_listed: to see if users are listed on an admin page: admin:core_user_changelist
    - In setup: create a test client. Read more at https://docs.djangoproject.com/en/3.0/topics/testing/tools/#overview-and-a-quick-example
    - Read more about Django admin at: https://docs.djangoproject.com/en/2.1/ref/contrib/admin/
    - Run test. Should fail with "NoReverseMatch: Reverse for 'core_user_changelist' not found. 'core_user_changelist' is not a valid view function or pattern name."
2. Docs:
    - https://docs.djangoproject.com/en/3.0/ref/contrib/admin/

### 5.2 Modify Django admin to list our custom user model
1. Go to core/admin.py file and make changes.
    - Read more at: https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    - Create UserAdmin extended from BaseUserAdmin. (To modify defauly django admin view)
    - Register custom user model with UserAdmin
    - Test again to check for pass

### 5.3 Modify Django Admin to support changing user model
1. test_admin.py:
    - Add test to check if user edit page loads
    - Run test. Should fail with FieldError since it is still using default fields from django and not our new custom user model.
2. Implement in core/admin.py file
    - Fieldsets: https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    - Run test

### 5.4 Modify Django Admin to support creating user
1. test_admin.py:
    - Add test to check if add user page works
    - Should fail with error: "FieldError: Unknown field(s) (username) specified for User." Because default django add user page is expecting a username, but in our case we have used email and don't have username.
2. Add fieldsets for add user page in test_admin.py to overwrite default fields of django to show only email, pwd1 and pwd2 and ignore username.
    - Run test

## 6. Setting up DataBase
### 6.1 Add postgres to Docker compose
1. Django by default uses sqlite db. We will configure our project to use postgres.
2. docker-compose.yml
    - Add db service
    - `image: postgres:12-alpine`: to use an image of postgresql v12 of alpine(lighter version).
        - Read more at https://hub.docker.com/_/postgres/
    - Add environment details. Read more at: https://docs.docker.com/compose/environment-variables/
    - For postgres password: use something simple for local. But in prod, use a secure password from jenkis/travis etc.
    - Add environment settings to app service.
    - Add dependency of db service on app. So that
        - db service loads before app service
        - db service is accessible through app service
3. Docs:
    - depends_on: https://docs.docker.com/compose/compose-file/#depends_on
    - postgres on docker hub: https://hub.docker.com/_/postgres/

### 6.2 Add postgres to Dockerfile
1. Will add some dependencies so that Django can communicate with Docker
2. requirements.txt - Add dependencies
    - **Psycopg:** is the most popular PostgreSQL database adapter for the Python programming language. Read more at: https://pypi.org/project/psycopg2/
3. Add dependencies to Dockerfile
    - `RUN apk add --update --no-cache postgresql-client`. It uses the package manager apk from apline to add postgresql-client package. --update means: update the registry before we add the package. --no-cache: means don't store the registry index on dockerfile. To minimize the no of packages that we store in our docker container. To maintain docker container with smaller footprint with no unnecessary dependencies.
    - Add temporary dependencies for postgres client
        - `RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev`
        - --virtual: so it can be remove lates
        - .tmp-build-deps: alias for temporary build dependencies for all our packages
        - To have smaller footprint
4. Remove temporary dependecies:
    - `RUN apk del .tmp-build-deps`
5. Build: `docker-compose build` and make sure image is built successfully

### 6.3 Configure database in Django
1. settings.py
    - modify DB configuration
    - os.environ.get will get environment variables from docker-compose.yml
    - In future, when deploying to different servers: we need to just modify the env info in docker-compose.yml
2. Docs:
    - environ: https://docs.python.org/3/library/os.html#os.environ
    - django db setting: https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-DATABASES
    - Django postgresql notes: https://docs.djangoproject.com/en/3.0/ref/databases/#postgresql-notes
    
## 7. Waiting for postgres to start
### 7.1 Mocking with unit tests
1. **Mocking**:
    - Means Change behavior of dependencies of the code that we are testing
    - We use mocking to Avoid unintended side effects
    - We use mocking to isolate the specific code to be tested
    - Ex: sending email. Send mock email instead of real one by modifying real email dependency with mock dependency
2. When writing unit tests,
    - Never depend on external services. (since can't guarantee liability of 3rd party service is up or not)
    - Always use mock and not real services (to avoid spamming, clogging)

### 7.2 Add tests for wait_for_db_command
1. To avoid any exception, and improve reliability of our project it is better to first load the postgres db and wait for it to fully load and once loaded, start the django project.
2. Add test for new feature.
    - create test_commands.py file
    - Add test case for test_wait_for_db_ready, test_wait_for_db
    - Test should fail with error: "Unknown command: 'wait_for_db'"
3. Docs: 
    - command: https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/#module-django.core.management
    - https://stackoverflow.com/questions/52621819/django-unit-test-wait-for-database
    - GitHub Django code for connection handler: https://github.com/django/django/blob/11b8c30b9e02ef6ecb996ad3280979dfeab700fa/django/db/utils.py#L195

### 7.3 Create wait_for_db management command
1. Create management/commands/wait_for_db.py file. (Note: Folder path names are django std recommendation)
2. Create Command class extended from django BaseCommand.
    - Read more here: https://docs.djangoproject.com/en/2.1/ref/django-admin/#django.core.management.call_command
3. Run test
4. Docs:
    - https://docs.djangoproject.com/en/3.0/ref/django-admin/#django.core.management.call_command
    - https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/#module-django.core.management
    
### 7.4 Make Docker Compose wait for db
1. Will use wait_for_db command in docker-compose.yml file.
2. docker-compose.yml file
    - Modify command under app services
    - wait_for_db ---> migrate ---> run_server
3. Run docker: `docker-compose up`: should setup DB, Migrate and run server
4. Run test: `docker-compose run app sh -c "python manage.py test && flake8"`

### 7.5 Run app on browser and create super user
1. Run docker: `docker-compose up`
2. Docker will start app at: `0.0.0.0:8000` which will be translated by docker compose for us to localhost:8000 or 127.0.0.1:8000
3. Create super user: `docker-compose run app sh -c "python manage.py createsuperuser"`
    - Note: This will not ask for username unlike default django super user creation. Since we modified user management code to only ask for email, password.
4. Login to django admin.

## 8. Create user management endpoints
### 8.1 Create users app
1. Will create endpoints for users creation, change password etc
2. Run: `docker-compose run --rm app sh -c "python manage.py startapp user"`
    - --rm will remove the container after the command is run. For cleaner container (optional: since docker-compose down will remove it anyway) Just a better practice
3. Cleanup:
    - remove migrations - will add to core
    - remove admin.py - will add to core
    - remove models.py - will add to core
    - remove tests.py - will add to user/tests/ folder
    - create user/tests/__init__.py file
4. Add rest_framework, rest_framework.authtoken and users app to settings.py file

### 8.2 Add tests for Create User API
1. Will add test for Create Users API endpoint
2. settings.py, make sure INSTALLED_APP has `user` app added.
3. user/tests/test_user_api.py
    - Add test cases for: test_create_valid_user_success, test_user_exists, test_password_too_short.
    - **Note**: While running tests, after each test case, the data from DB is refreshed and removed. So, data from one test case will not effect other test case
    - Test: `docker-compose run --rm app sh -c "python manage.py test && flake8"`. The `--rm` option is to make sure that our docker container is removed after performing the test and not linger in the system.
    - should fail with "NoReverseMatch: 'user' is not a registered namespace". Because we have not created the user url yet in our project
4. Docs:
    - get_user_model: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.get_user_model

### 8.3 Implement Create User API
1. Create serializer for create user request ---> Create view to handle the request ---> bind the view to a URL which we can access as an endpoint.
2. Create user/serializers.py file
    - Create UserSerializer class extended from serializers.ModelSerializer
    - The default create method will take a plain password. Make sure to encrypt it before passing to django
    - Docs: modelserializer: https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
3. user/views.py
    - create CreateUserView extended from rest_framework generics CreateAPIView
    - Docs: CreateAPIView: https://www.django-rest-framework.org/api-guide/generic-views/#createapiview
4. Create user/urls.py:
    - Map view to url
5. Include the user/urls.py in app/urls.py
6. Run test for pass
    - Also can be verified on browser at http://127.0.0.1:8000/api/user/create/ 
7. Note: # is for comment """""" is for doc string.

### 8.4 Add tests for creating a new token
1. Will create an end point to generate an auth token to authenticate future requests for any API.
    - Thus no need of sending username and pwd with each requests and just keep sending the token.
    - The token can be reverted any time from the DB for suspicious users.
2. Add unit tests to: user/tests/test_user_api.py
    - Create test cases for Public view: test_create_token_for_user, test_create_token_invalid_credentials, test_create_token_no_user, test_create_token_missing_field
3. Test should fail with: django.urls.exceptions.NoReverseMatch: Reverse for 'token' not found. 'token' is not a valid view function or pattern name. 
    - Since we have not created the url yet

### 8.5 Implement Create Token API
1. Serializers ---> View ---> url
2. user/serializers.py
    - create AuthTokenSerializer extended from serializers.Serializer. Thus, we will use the default django auth serializer.
    - Docs: AuthTokenSerializer: https://github.com/encode/django-rest-framework/blob/a628a2dbce8f8f3047d30fe5345f86ae843bcdcc/rest_framework/authtoken/serializers.py#L7
3. user/views.py
    - Create CreateTokenView extended from ObtainAuthToken
    - Docs: ObtainAuthToken: https://www.django-rest-framework.org/api-guide/authentication/#by-exposing-an-api-endpoint
4. user/urls.py:
    - Map view to url
5. Run test `docker-compose run --rm app sh -c "python manage.py test && flake8"`
6. Test on browser:
    - Restart docker: `docker-compose down` & `docker-compose up`
    - Test if token is generated by providing username and pwd to : http://127.0.0.1:8000/api/user/token/
    - The token can then be stored in cookie and used for authentication for future uses

### 8.6 Tests for Manage User endpoint
1. Manage user endpoint will allow user to update their profile. Endpoint: "user/me/"
2. user/tests/test_user_api.py
    - Add test cases: test_retrieve_user_unauthorized under PublicUserAPITests
    - PrivateUserAPITests: test_retrieve_profile_success, test_post_not_allowed, test_update_user_profile
3. Run test `docker-compose run --rm app sh -c "python manage.py test && flake8"`
    - should fail with "NoReverseMatch: Reverse for 'me' not found. 'me' is not a valid view function or pattern name."

### 8.7 Create Manage user endpoint
1. user/views.py
    - Create ManageUserView extended from generics.RetrieveUpdateAPIView
    - Docs: RetrieveUpdateAPIView: https://www.django-rest-framework.org/api-guide/generic-views/#retrieveupdateapiview
2. user/serializers.py
    - Add update method to UserSerializer
3. user/urls.py:
    - Map view to url
4. Run test `docker-compose run --rm app sh -c "python manage.py test && flake8"`
5. Test on browser: 
    - Visit: http://127.0.0.1:8000/api/user/me/ Should throw invalid token error
    - http://127.0.0.1:8000/api/user/token/ - Copy token from here
    - Install modheader chrome extension: ModHeader allows us to modify header of API request directly from browser. 
    - URL: https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj
    - Open modheader and add, name value pair as: Authorization, Token 34kk.....
    - Reload http://127.0.0.1:8000/api/user/me/ should return the user data
    - Try updating the data from Raw data tab using PATCH. Since form will ask for password. (form works on PUT method, so all fields must be provided)
    - **PUT vs PATCH:** PUT: Updates and replaces the entire object. So we must provide all the fields. While PATCH: Updates the specific field mentioned in JSON structure. So only required to provide specific fields.

## 9. Create Tags endpoint
1. Tags endpoint will allow us to add tags to our recipes and help us sorting/filtering them.
### 9.1 Create recipe app
1. All recipe related endpoints will be stored in recipes app
    - recipe, tags, ingredients endpoint
2. Create recipe app:
    `docker-compose run --rm app sh -c "python manage.py startapp recipe"`
3. Cleanup:
    - Remove migrations/: present in core
    - Remove admin.py: present in core
    - Remove models.py: present in core
    - Remove tests.py: will add in recipe/tests folder
    - Add tests/__init__.py

### 9.2 Create Tag model
1. Will create Tag DB model to handle tag objects
    - will accept name of tag and user that owns tag
2. Add test case: test_tag_str
    - core/tests/test_models.py
3. Run test should fail with: "AttributeError: module 'core.models' has no attribute 'Tag'"
4. Create model
    - core/models.py file: create Tag class extended from models.Model
5. Register Tag model in core/admin.py
6. Create migration
    - `docker-compose run --rm app sh -c "python manage.py makemigrations"`
    - will create migration files under core/migrations/0002_tag.py
7. Apply migration
    - `docker-compose run --rm app sh -c "python manage.py migrate"`
8. Run test: `docker-compose run --rm app sh -c "python manage.py test && flake8"` - pass
9. Docs:
    - DJ model str: https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model.__str__
    - DJ admin register: https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin
    - DJ Foreign key: https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ForeignKey
    - DJ Foreign key on_delete: https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ForeignKey.on_delete
    - Http status codes: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html

### 9.3 Add Tests for Listing tags
1. Create recipes/tests/test_tags_api.py
    - Create test cases: test_login_required, test_retrieve_tags, test_tags_limited
2. Run test: `docker-compose run --rm app sh -c "python manage.py test && flake8"` Should fail with "No module named 'recipe.serializers'"

### 9.4 Implement endpoint to List Tags
1. Create recipe/serializers.py file
    - Create TagSerializer class extended from serializers.ModelSerializer
2. recipes/views.py file
    - Create TagViewSet
3. Create recipe/urls.py file
4. Include recipe/urls.py in app/urls.py file
5. Docs:
    - DRF Model Serializer: https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
    - DRF GenericViewSet: https://www.django-rest-framework.org/api-guide/viewsets/#genericviewset
    - DRF GenericViewSet example: https://www.django-rest-framework.org/api-guide/viewsets/#example_3

### 9.5 Implement create tags endpoint
1. recipe/tests/test_tags_api.py
    - add test cases: test_create_tag_successful, test_create_tag_invalid - Run test to fail
2. recipe/views.py:
    - Add CreateModelMixin to TagViewSet
3. Run test: `docker-compose run --rm app sh -c "python manage.py test && flake8"`

## 10. Create Ingredient endpoint
### 10.1 Add ingredient model
1. Test for ingredient model: core/tests/test_models.py file:
    - Create test case: test_ingredients_str
    - Run test case: Should fail with "AttributeError: module 'core.models' has no attribute 'Ingredient'"
2. Create model: core/models.py file:
    - Create Ingredient model
3. Make migrations: `docker-compose run --rm app sh -c "python manage.py makemigrations core"`
4. Apply migrations: `docker-compose run --rm app sh -c "python manage.py migrate core"`
5. Register ingredient model for admin. @core/admin.py file
6. Run test: `docker-compose run --rm app sh -c "python manage.py test && flake8"` - Pass

### 10.2 Add tests for Listing Ingredients endpoint
1. Create recipe/tests/test_ingredients_api.py
    - add test cases: 
        - Public: test_login_required
        - Private: test_retrieve_ingredient_list, test_ingredients_limited_to_user
    - Run test: fail with "ImportError: cannot import name 'IngredientSerializer' from 'recipe.serializers' (/app/recipe/serializers.py)"

### 10.3 Implement feature for List Ingredients endpoint
1. recipe/serializers.py file
    - Create IngredientSerializer and map Ingredient model to serializer
2. recipe/views.py file:
    - Create IngredientViewSet
3. Register the view in recipe/urls.py file:
    - `router.register('ingredients', views.IngredientViewSet)`
4. Test: `docker-compose run --rm app sh -c "python manage.py test && flake8"`

### 10.4 Implement feature for creating Ingredients with endpoint
1. Add test: recipe/tests/test_ingredients_api.py
    - Add test cases for: test_create_ingredient_successful, test_create_ingredient_invalid
    - Run test - Fail
2. recipe/views.py:
    - Modify IngredientViewSet to add create method
3. Test: `docker-compose run --rm app sh -c "python manage.py test && flake8"` with pass
4. Test on browser:
    - http://localhost:8000/api/recipe/ingredients/
    
### 10.5 Refactor Tags and Ingredients viewsets
1. Refactor to handle common code b/w both viewsets using a base class. And run test to make sure nothing is breaking.
    - Test cases helps a lot and gives assurance while code refactoring
2. recipe/views.py:
    - Create BaseRecipeViewSet and extend TagViewSet, IngredientViewSet from it
3. Run test: `docker-compose run --rm app sh -c "python manage.py test && flake8"` with pass

## 11. Create Recipe Endpoints
### 11.1 Create Recipe Model
1. We will create a new model to handle recipe objects
2. Add test for the new model. core/tests/test_models.py
    - Create test case: test_recipe_str
    - Run test: `docker-compose run --rm app sh -c "python manage.py test && flake8"` Fail with "AttributeError: module 'core.models' has no attribute 'Recipe'"
3. core/models.py file
    - Create model: Recipe
4. Make migrations: `docker-compose run --rm app sh -c "python manage.py makemigrations core"`
5. Apply migration: `docker-compose run --rm app sh -c "python manage.py migrate core"`
6. Register recipe model to core/admin.py
7. Test with pass
8. Docs:
    - ManyToMany field: https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ManyToManyField

### 11.2 Add Test for Listing recipes endpoint
1. create recipe/tests/test_recipe_api.py file:
    - Add test cases: 
        - Public: test_auth_required
        - Private: test_retrieve_recipes, test_recipes_limited_to_user, 
    - Test fail with "ImportError: cannot import name 'RecipeSerializer' from 'recipe.serializers' (/app/recipe/serializers.py)"

### 11.3 Implement listing recipes endpoint
1. recipe/serializers.py
    - Create RecipeSerializer
2. recipe/views.py
    - Create recipe view set: RecipeViewSet extended from ModelViewSet
3. Map new viewset to recipe/urls.py file
    - `router.register('recipes', views.RecipeViewSet)`
4. Docs: 
    - primarykeyrelatedfield: https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield

### 11.4 Add test for Recipe detail endpoint
1. recipe/tests/test_recipe_api.py
    - Add test case
    - Run test: should fail with: "ImportError: cannot import name 'RecipeDetailSerializer' from 'recipe.serializers'"
2. Docs:
    - get_serializer_class: https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
    - getattr: https://docs.python.org/3/library/functions.html#getattr

### 11.5 Implement feature for Recipe detail endpoint
1. recipe/serializers.py
    - Create RecipeDetailSerializer extended from RecipeSerializer
2. recipe/views.py
    - Add RecipeDetailSerializer to RecipeViewSet
3. Docs:
    - associating-snippets-with-users: https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#associating-snippets-with-users

### 11.6 Add test for Create recipe endpoint
1. recipe/tests/test_recipe_api.py
    - Create test cases: Private: test_create_basic_recipe, test_create_recipe_with_tags, test_create_recipe_with_ingredients
    - Test fail: 'IntegrityError: null value in column "user_id" violates not-null constraint'

### 11.7 Implement feature for Create recipe endpoint
1. recipe/views.py
    - overwrite perform_create to assign recipe to a user
2. Run test - pass
3. Test on browser: 
    - http://127.0.0.1:8000/api/user/token/ login and get token
    - Add Authorization: Token sss to ModHeader extension
    - Create tags: http://127.0.0.1:8000/api/recipe/tags/
    - Create ingredients: http://127.0.0.1:8000/api/recipe/ingredients/
    - Create a Recipe: http://127.0.0.1:8000/api/recipe/recipes/

### 11.8 Add Test for Updating recipe endpoint
1. Optional: since update feature comes built in with DRF ModelViewSet. Will do just for concept.
2. Put vs Patch: Patch is used to update the specific fields that are provided in the payload. While with PUT, the whole object is replaced with payload.
3. recipe/test_recipe_api.py:
    - Add test cases: test_partial_update_recipe, test_full_update_recipe

## 12. Add Upload Image endpoint
### 12.1 Add Pillow requirement
1. Install Pillow python package. (required to handle images in django)
    - https://pypi.org/project/Pillow/
    - Add Pillow to requirements.txt file
2. Add Pillow dependencies in Dockerfile
    - app dependencies:(needed to run app) `jpeg-dev`: add support for jpeg binaries in Dockerfile
    - build dependencies:(needed to run build and can be removed) `musl-dev zlib zlib-dev`
3. Create directory for upload using Dockerfile `RUN mkdir -p /vol/web/media` and `RUN mkdir -p /vol/web/static` for static files: viz HTML, CSS, JS etc. (-p tells docker to create all the sub directories if they does not exist eg: create vol or web if it doesn't exist)
4. Add permission for user to the vol directory
    - `RUN chown -R user:user /vol/` (-R: recurisve: covers vol + all sub directories) user has all the permission
    - `RUN chmod -R 755 /vol/web` (Others has read permission)
5. Configure settings.py file: 
    - map folders to url: `STATIC_URL = '/static/' MEDIA_URL = '/media/'` tells django where to serve static and media files
    - `MEDIA_ROOT = '/vol/web/media'`: tells django where all the media files are stored.
    - `STATIC_ROOT = '/vol/web/static'`: tells django where all the static files are stored.
6. app/urls.py: add url for media file. Note: Django by default will serve all static files at /static/ path. But the media files need to be added manually.    - `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`
7. Build docker: `docker-compose down`, `docker-compose build`, `docker-compose up` to create a build by installing pillow and all dependencies we added.

### 12.2 Modifying recipe model to accept image field
1. Note: during image upload, change the image name to avoid conflict with existing names.
2. core/test_models.py
    - Add test case: test_recipe_file_name_uuid
3. Test should fail with "AttributeError: module 'core.models' has no attribute 'recipe_image_file_path'"
4. core/models.py
    - Create fn: recipe_image_file_path
    - Add image field to recipe model
5. makemigrations: `docker-compose run --rm app sh -c "python manage.py makemigrations core"`
6. apply migration: `docker-compose run --rm app sh -c "python manage.py migrate core"`
7. Run test: `docker-compose run --rm app sh -c "python manage.py test && flake8"` - pass

### 12.3 Add tests for uploading image to recipe
1. recipe/test_recipe_api.py
    - Add test cases: test_upload_image_to_recipe, test_upload_image_bad_request
2. Run test - fail "django.urls.exceptions.NoReverseMatch: Reverse for 'recipe-upload-image' not found. 'recipe-upload-image' is not a valid view function or pattern name."
