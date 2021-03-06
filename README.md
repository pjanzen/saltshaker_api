# Saltshaker API

Saltshaker is a Web-based configuration management management tool developed by Saltstack. It simplifies the daily use of saltstack, enriches the functions of saltstack, and supports multi-master management. This project is Saltshaker's backend Restful API, which needs to be combined with front-end projects.
## Architecture diagram
![image](https://github.com/pjanzen/saltshaker_api/blob/master/screenshots/Saltshaker_Plus.jpg)
## Dashboard
![image](https://github.com/pjanzen/saltshaker_api/blob/master/screenshots/dashboard.png)

## Installation manual

- [Requirements](#Requirements)
- [Manual deployment](#Manual deployment)

## Requirements

- Python >= 3.6
- Mysql >= 5.7.8 （With json support）
- Redis
- RabbitMQ
- Supervisor (version 4.0.0.dev0 does not support python3) Please use this command to install：pip install git+https://github.com/Supervisor/supervisor@master
- GitLab >= 9.0


### Manual deployment

To install Saltshaker, you need to prepare the Python environment first.

1. Create saltshaker home and clone repo:
    ```sh
    $ cd /opt
    ```

    ```sh
    $ git clone https://github.com/pjanzen/saltshaker_api.git
    ```

2. Install python requirements:
    You can run this from an python virtual env. If you choose to do so, create it first.
    ```sh
    $ python3 -m venv /opt/salt/virtual_envs/python3
    ```

    ```sh
    $ source /opt/salt/virtual_envs/bin/activate
    ```

    ```sh
    $ cd /opt/saltshaker_api
    ```


    ```sh
    $ pip install -r requirements.txt
    ```

3. Set the FLASK_APP environment variable to use the Flask CLI tool, the path to the path of the deployed app

    ```sh
    $ export FLASK_APP=$Home/saltshaker_api/app.py
    ```

4. Initialize the database table and related information, type the super administrator username and password (see the saltshaker.conf for the configuration of the database, please ensure that the database can be connected and the corresponding database has been created)

    ```sh
    $ mkdir /var/log/saltshaker_plus
    $ flask init
    ```
    
    ```
    Output：
        Enter the initial administrators username [admin]: admin
        Enter the initial Administrators password: 
        Repeat for confirmation: 
        Create user table is successful
        Create role table is successful
        Create acl table is successful
        Create groups table is successful
        Create product table is successful
        Create audit_log table is successful
        Create event table is successful
        Create cmd_history table is successful
        Create host table is successful
        Create grains table is successful
        Create period_task table is successful
        Create period_result table is successful
        Create period_audit table is successful
        Create sls table is successful
        Init super administrator role successful
        Init general user role successful
        Init product manager role successful
        Init user administrator role successful
        Init access control administrator role successful
        Init user successful
        Successful
    ```
    You can also directly import the database file saltshaker_plus.sql, initial username: admin password: admin
    ```sh
    mysql> source $HOME/saltshaker_api/saltshaker_plus.sql;
    ```

5. Start Flask App, will listen at port 9000 after succesfull startup.
    - Development mode

        ```sh
        $ cd /opt/saltshaker_api
        $ export HOME=$(pwd)
        $ export $FLAKSAPP=$HOME/app.py
        ```
        activate virtual_env when you use it.
        ```sh
        $ source ../virtual_env/python3/bin/activate
        ```

        ```sh
        $ python $Home/saltshaker_api/app.py
        ```
    - Gunicorn mode
    
        ```sh
        $ cd $Home/saltshaker_api/ && gunicorn -c gun.py app:app
        ```
    - Production mode
    
        ```sh
        supervisord.conf change config to adapt your setup
        $ /usr/local/bin/supervisord -c $Home/saltshaker_api/supervisord.conf
        ```
    
6. Start celery （Ignore this step when you use supervisord）

    ```sh
    $ cd $Home/saltshaker_api/ && celery -A app.celery worker --loglevel=info
    ```
7. Combine front-end projects
    ```
    https://github.com/pjanzen/saltshaker_frontend
    ```

