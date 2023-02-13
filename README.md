# Teaching Platform - Database Controller
This part of Teaching-Platfrom project is responsible for
managing database operations.

## Setup (Linux / Windows)
After pulling the code onto your machine, start  off by creating a
`postgresql` database and puting it's credentials in 
[config.yaml](https://github.com/Czupryn013/Teaching-Platform/blob/develop/config.yaml). 
Then create a `Python Virtual Enviroment`.

```bash
python3 -m venv ".env"
source ".env/bin/activate" / source ".env/Scripts/activate"
```


Then use pip to install all dependencies.
```bash
pip install .
```
In the main directory create `.env` file like in example below and fill
it in with correct data.
```.env
db_password = "postgresql_password123"
email_password = "outlook_password123"
email_login = "example@outlook.com"
secret_key = "SECRET_KEY"
salt = "SALT"
```


After that you are almost ready to go, just run `main.py`.
```bash
cd teaching-platform
python3 main.py / python main.py
```
App runs on `http://127.0.0.1:5000` by default, to change it set attribute
`port` in `main.py` to the desired one in line `23`.
```python
app.run(port=5000)
```

## Api usage

### Endpoints
Users:
* `/users`  - **[GET]**
* `/users/me` - **[GET]**
* `/users/<user_id>` - **[GET]**
* `/users/remove/<user_id>` - **[DELETE]**
* `/users` - **[POST]**
* `/users/password` - **[PATCH]**
* `/users/password/<token>` - **[POST]**
* `/users/password` - **[POST]**
* `/users/confirm/<token>` - **[GET]**
* `/users/confirm` - **[GET]**

Lessons:
* `/lessons`  - **[GET]**
* `/lessons/<lesson_id>` - **[GET]**
* `/lessons/remove/<lesson_id>` - **[DELETE]**
* `/lessons` - **[POST]**
* `/lessons/<lesson_id>/remove` - **[PATCH]**
* `/lessons/<lesson_id>/add` - **[PATCH]**
* `/lessons/<lesson_id>` - **[PATCH]**

Projects:
* `/projects`  - **[GET]**
* `/projects/<project_id>` - **[GET]**
* `/projects` - **[POST]**
* `/projects/remove/<project_id>` - **[DELETE]**
* `/projects/<project_id>/remove` - **[PATCH]**
* `/projects/<project_id>/add` - **[PATCH]**
* `/projects/<project_id>` - **[PATCH]**
* `/projects/<project_id>/mentor` - **[PATCH]**
* 
### Endpoint requirments
**Users:**
* **[GET]** `/users` - Requires sender to pass
valid authorization to an account with `ADMIN` role.
* **[GET]** `/users/me` - Requires sender to pass valid 
authorization to an account in order to recive it's information.
* **[GET]** `/users/me` - Requires sender to pass valid 
authorization to an account with `ADMIN` role in order to recive 
information of user with `<user_id>`.
* **[PATCH]** `/users/me` - Requires sender to pass both valid 
authorization to an account and valid body in order to update username 
or password. To update password pass `password` atribute in body, to 
`username`. Both password and username need to follow their requirments.
update username pass. To update password/username send the following body.
  ```json
      {
          "username/password" : "USERNAME/PASSWORD"
      }
  ```
* **[PATCH]** `/update/<user_id>` - Requires sender to pass valid 
authorization to an accounts with `ADMIN` role. To update role of user 
with id passed in url (`<user_id>`). Role that you wish to change to
should be passed in body in `role` parameter. Role needs to bo one of
the following `ADMIN`, `STUDENT`, `TEACHER`.
  ```json
      {
          "role" : "ADMIN/STUDENT/TEACHER"
      }
  ```
* **[DELETE]** `/users/remove<user_id>` - Requires sender to pass valid 
authorization to an accounts with `ADMIN` role. To remove user with id
passed in url (`<user_id>`).
* **[POST]** `/users` - Doesn't require any form of authorization, 
in order to add new user to the system. Body should
follow this template: 
    ```json
    {
        "username" : "USERNAME",
        "password" : "PASSWORD"
    }
    ```
* **[GET]** `/users/confirm/<token>` - Requires being logged to an
account with `email` to which confirmation link was sent. After logging
in with correct credentials, `Role` will be set to `STUDENT` if it
was `UNCOMFIRMED` before. Otherwise, nothing will change.
* **[GET]** `/users/confirm` - Requires being logged in. Resends
confirmation email if `Role` is `UNCOMFIRMED`.
* **[POST]** `/users/password` - Doesn't require being logged in.
In body pass `email` to which reset link should be sent. `email`
must be email of an actual user.
* **[POST]** `/users/password/<token>` - Doesn't require being logged in.
In body pass `new_password`, password will be changed to 
this value, if it meets all the requirments. Password will be changed
for user with `email` that is coresponding to hashed `<token>` in the
url.

**Lessons:**
* **[GET]** `/lessons` - Requires being logged in, returns all lessons.
* **[GET]** `/lessons/<lesson_id>` - Requires being logged in, returns 
lesson with `<lesson_id>`.
* **[DELETE]** `/lessons/<lesson_id>` - Requires being logged in,
as admin or teacher who teaches this lesson. Removes lesson with given id.
* **[POST]** `/lessons` - Takes `teacher_id` and `info` values in request body.
Adds new lesson. `teacher_id` needs to be an id of `User` with `TEACHER` role.
* **[PATCH]** `/lessons/<lesson_id>/remove` - Requires authorization as
Admin or teacher who teaches this class. Removes student with given id from lesson.
Parameter `student_id` should be passed in request body.
* **[PATCH]** `/lessons/<lesson_id>/add` - Requires authorization as
Admin or teacher who teaches this class. Adds student with given id to lesson.
Parameter `student_id` should be passed in request body.
* **[PATCH]** `/lessons/<lesson_id>` - Requires authorization as
Admin or teacher who teaches this class. Updates lesson's details. To
update pass 1 or more of following values: `info`, `homework`, `pre_lesson`
in request body.

**Projects:**
* **[GET]** `/projects` - Requires being logged in, returns all projects.
* **[GET]** `/projects/<project_id>` - Requires being logged in, returns 
lesson with `<project_id>`.
* **[DELETE]** `/projects/<project_id>` - Requires being logged in,
as admin or teacher who teaches this lesson. Removes lesson with given id.
* **[POST]** `/projects` - Takes `mentor_id` and `name` values in request body.
Adds new lesson. Variable `status` is set to "In development." by default. 
`mentor_id` needs to be an id of a `User` with `TEACHER` role.
* **[PATCH]** `/projects/<project_id>/remove` - Requires authorization as
Admin or mentor who leads this project. Removes student with given id from project.
Parameter `student_id` should be passed in request body.
* **[PATCH]** `/projects/<project_id>/add` - Requires authorization as
Admin or mentor who leads this project. Adds student with given id to the 
project. Parameter `student_id` should be passed in request body.
* **[PATCH]** `/projects/<project_id>/mentor` - Requires authorization as
Admin or mentor leading this project. Reasigns mentor to user with `<mentor_id>`,
this user must have role `ADMIN` or `TEACHER`.
* **[PATCH]** `/projects/<project_id>` - equires authorization as
Admin or mentor who leads this project. Updates project details. To
update pass one or more of the following values: `name`, `status`, `info`
in request body. Values of `Project` will be updated acordingly.
### Password and username requirments
#### Password:
* Length 5 to 50
* Uppercase, special characters - 1
* Numbers and nonletters - 2
#### Username:
* Can't contain whitespaces nor be empty.
* Max 90 characters long.

### First usage
#### First user
After you created the database and had run the application it's time to
start using it. First thing you would want to do is to create the first
user. It's fairly simple, just send a **POST** requst to `/users`
endpoint (for more details look into above sections).

#### Giving the first user the `ADMIN` role
By default, all users are created with role the `STUDENT` role. For now
the only way to assign `ADMIN` to the first user it throu database's 
query tool or client like `pgAdmin4`. You need to change the value of
column "role" from "STUDENT" to "ADMIN".

#### Adding and managing more users
After we have the first admin in the system we are able to change roles
of other users throu `/update` endpoint (again all details listed above).
We can also perform other operations such as deleting users, fetching 
user data and each user can update their password as well as username
after logging in (all of them are described above). 