from ftplib import FTP
from datetime import datetime, timedelta
import json


f = open('ftp_info.json')
data = json.load(f)
host = data['host']
port = data['port']
user = data['user']
password = data['password']


#Connect to FTP Server
ftp = FTP()
ftp.connect(host, port)
ftp.login(user, password)

ftp.dir()

#Create base folders and pathways
folders = []
files = []


#Function to get file timestamps, if available
def getDate(dateString):
    temp_date_mod = datetime(year=int(dateString[0:4]),month=int(dateString[4:6]),day=int(dateString[6:8]))
    return temp_date_mod



#Function to create the folders and files lists!
def sort_items(items):
    for item in items:
        parentDir = ftp.pwd()
        if len(parentDir) >= 2:
                parentDir += '/'
        if item[1].get('type') == 'dir' and item[0] not in folders:
            folders.append(parentDir + item[0])
        elif item[1].get('type') == 'file' and item[0] not in files:
            try:
                date_mod = getDate(item[1].get('modify'))
            except:
                date_mod = datetime.now()
            files.append({'File':parentDir + item[0], 'Modified Date':date_mod})

mylist = list(ftp.mlsd(path="", facts=["type", "modify"]))
sort_items(mylist)

print('\n')


for item in mylist:
    print(item)
    
count = 0

#Here is where the above function is called
for folder in folders:
    ftp.cwd(folder)
    temp = list(ftp.mlsd(path="", facts=["type", "modify"]))
    sort_items(temp)
    count += 1
    if count >= 1000:
        break

print('\n')


#Now the timestamp comparison!
new_files = []
today = datetime.now()
time_range = timedelta(weeks=2)
print('The following file(s) may need to be updated!\n')
for file in files:
    if '/TV/webOS' in file.get('File') or '/STB' in file.get('File'):
        if file.get('Modified Date') >= (today - time_range):
            print(file.get('File'), '***',file.get('Modified Date'))
            print('#'*25)
            new_files.append(file.get('File'))

#Define Download Behavior
def download_file(file):
    file_parts = file.split('/')
    file_to_dl = file_parts.pop()
    file_path = "/".join(file_parts) + "/"
    ftp.cwd(file_path)
    try:
        ftp.retrbinary("RETR " + file_to_dl,open(file_to_dl, 'wb').write)
        print("{} has been downloaded!\n".format(file_to_dl))
    except:
        print("Cannot find this file!\n")

#Run Download Script
for file in new_files:
    ftp.cwd('/')
    response = input('Would you like to download {}? Yes/No\n'.format(file))
    if response == 'Yes':
        download_file(file)
    print("")

print('\nAll done!')

#Close the connection
print("")
ftp.quit()
