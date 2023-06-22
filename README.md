# wow_charcter_online_check
 This package checks whether characters are online in a CMaNGOS wow server

## Install 
Copy and extract this file to somewhere on your computer.
This package makes use of python ensure it is installed.

Open a terminal in the extracted directory and type
```
pip install -r requirements.txt
```

Create a shortcut of client.py and if on Windows copy it to 
```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

Set the following in config.env
```
MYSQL_HOST: ip_address_of_mysql_server
MYSQL_PASSWORD : mysql_password
SSH_HOST: ip_address_to_connect_over_ssh
SSH_USER : ssh_user
SSH_PASSWORD : ssh_password
```
Note that the MYSQL is hard coded to the user wow_character_check, reference below to create



##  SQL User
Most likley you will need to create a new user for this script to use.
This script assumes you are running CmANGOS

Firstly get access to the server which is running CmANGOS and its MYSQL database

Then run the follwing, being sure to change <IP_ADDRESS_HERE> and <PASSWORD_HERE>
```sql
    CREATE USER 'wow_character_check'@'<IP_ADDRESS_HERE>' IDENTIFIED BY '<PASSWORD_HERE>';
```
Then assign permissions
```sql
    GRANT  SELECT `tbccharacters`.'characters' TO 'wow_character_check'@'<IP_ADDRESS_HERE>' WITH GRANT OPTION;

```
Then update permissions
```sql
    FLUSH PRIVILEGES;
```

## Shutting down
By defualt this is configured to shut down a remote server by connecting over ssh


If you are using a ESXI host like myself..
1. Log in to the web access page of your ESXI host
2. Select Manage in the navigator pane in the top left.
3. Click the Services tab on the right side.
4. Select the TSM-SSH entry on the list. The service status shows Stopped. (TSM stands for Tech Support Mode).
5. Click Start to start the SSH service.
6. To ensure SSH after restart:
    - - Select the TSM-SSH entry on the list.
    - - Click Actions - > Policy.
    - - Choose Start and stop with host, and the SSH service will activate after every host restart.

If you are not using ESXI you may wish to change line 63 of client.py to:
```python
    client.exec_command("shutdown -n now")
```
