# SwagShop Notes

## Data 

IP: 
OS:
Arch:
Hostname:
DNS:
Domain:  / Domain SID:
Machine Purpose: 
Services:
Service Languages:
Users:
Email and Username Formatting:
Credentials:



#### Mindmap-per Service

```
sudo tcpdump -nvvvXi tun0 tcp port 80
ls -1tr Screenshots | grep -v ping | awk '{print "![]("HTB")"}\' | xsel -b
```

- OS detect, run generate noting for nmap
- Nuclei 
	- /app
- nikto 
	- /var
- nmap discovery
	- /js

```xml
<key>b355a9e0cd018d3f7f03607141518419</key>
</crypt>
<disable_local_modules>false</disable_local_modules>
<resources>
<db>
<table_prefix></table_prefix>
</db>
<default_setup>
<connection>
<host>localhost</host>
<username>root</username>
<password>fMVWh7bDHpgZkyfqQXreTjU9</password>
<dbname>swagshop</dbname>
<initStatements>SET NAMES utf8</initStatements>
<model>mysql4</model>
<type>pdo_mysql</type>
<pdoType></pdoType>
<active>1</active>
```
- Shoplift to change admin creds
	- 37977 exploitdb (has index.php)
	- https://github.com/Hackhoven/Magento-Shoplift-Exploit/blob/main/magento_rce.py does not - fixed version in this directory
- Auth RCE 
	- https://www.exploit-db.com/exploits/37811
	- https://github.com/Hackhoven/Magento-RCE/blob/main/magento-rce-exploit.py
-
-
-
-
-
-
-
-
-
-
-



#### Todo List


