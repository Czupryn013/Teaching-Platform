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