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

After that you are almost ready to go, just run `main.py`.
```bash
cd teaching-platform
python3 main.py / python main.py
```
App runs on `http://127.0.0.1:5000` by default, to change it set attribute
`port` im `main.py` to the desired one in line `23`.
```python
app.run(port=5000)
```

## Api usage

### Endpoints
* `/users`  - **[GET]**
* `/users/me` - **[GET]**
* `/users/remove<user_id>` - **[DELETE]**
* `/users` - **[POST]**

### Endpoint requirments
* **[GET]** `/users` - Requires sender to pass
valid authorization to an account with `ADMIN` role.
* **[GET]** `/users/me` - Requires sender to pass valid 
authorization to an account in order to recive it's information.
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