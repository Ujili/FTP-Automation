from ftplib import FTP
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

print("Please enter the file to be downloaded:\n")
file_with_path = input()



def download_file(file):
    file_parts = file.split('/')
    file_to_dl = file_parts.pop()
    file_path = "/".join(file_parts) + "/"
    ftp.cwd(file_path)
    try:
        ftp.retrbinary("RETR " + file_to_dl,open(file_to_dl, 'wb').write)
        print("{} has been downloaded!\n".format(file_to_dl))
    except:
        print("Cannot find this file!")
