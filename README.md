py_backup_pfsense
===============
This program will login to your pfSense router and download the latest backup of your configuration file.  It then will attempt to git commit/git push that file, should your directory where the file is saved be a git repository.

This program is an adaptation of Nextraztus's most excellent port of my original shell script to do pfSense backups from the command line.  As of the latest pfSense, they now use CSRF validation which meant that the earlier method of saving cookies via curl would not work properly.  This script properly works around the issue.

Syntax
======
This command expects four arguments, in the following order:

`py_backup_pfsense username password router_ip_port filepath`

Where:
  - username - user that you log into pfSense with
  - password - password for aforementioned user
  - router_ip_port - The ip and port of your https service on the pfSense system
  - filepath - path and filename to where you want the xml backup saved.
  
Example: `py_backup_pfsense admin adminpass 10.0.0.1:443 /opt/pfSense_Backup/mybackup.xml`

**Don't like your password to show in the command line?**  You can opt to define these arguments as environment variables instead:
  - PBP_USER - analog for username
  - PBP_PASS - analog for password
  - PBP_ROUTER - analog for router ip and port
  - PBP_FILEPATH - analog for filepath

In the below example, `top`/`ps` will not show any of the arguments for the program call, saving your password from a casual discovery via those commands:

```
#!/bin/bash
PBP_USER=myuser
PBP_PASS=mypass
PBP_ROUTER=10.0.0.1:443
PBP_FILEPATH=/opt/pfSense_Backup/mybackup.xml
py_backup_pfsense
```


Requirements
============
This script installs the following required modules:

  - requests (used to abstract the ssl communication with the pfSense router)
  - sh (a more self-documenting way to instantiate shell commands inside python)


Thanks
======
[Nextraztus](https://github.com/nextraztus) for providing a port of the original shell script into python.
