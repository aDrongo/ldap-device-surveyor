﻿# LDAP Device Surveyor
The purpose of this program is to easily scan AD computers and see their status by their location.
* Python for API, scanning module, ldap and SQL interaction.
* Vue.JS SPA frontend, makes async API calls for data.
* Periodically scans all devices, pulls device information from LDAP if configured.
* Displays devices by subnet locations with an overview and collapsed tables.
* Device changes logged.
* Docker build optional
* HTTPS optional
* Users

Work in progress  

## Example  

https://ibb.co/H4Byyrq  
https://ibb.co/rcGnZj8  
https://ibb.co/WDQ3MRc  


## Install via Docker

```
git clone this repo

docker-compose up

#Config:
#   Fill in backend/json.config details with your own, default will work out of the box.

#For SSL:
#    Create SSL Certs as server.crt & server.key and place in router/etc/
#    Commented sections in router/nginx.conf and docker-compose.yml show SSL directions.

```
