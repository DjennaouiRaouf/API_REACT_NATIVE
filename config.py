from cryptography.fernet import Fernet

key = Fernet.generate_key()

while True:
    NAME= input('Database Name : \n').encode()
    if len(NAME) != 0:
        break
while True:

    USER= input('Database User Name : \n').encode()
    if len(USER) != 0:
        break

while True:
    PASSWORD= input('Database Password : \n').encode()
    if len(PASSWORD) != 0:
        break

while True:
    HOST= input('Database Host Name : \n').encode()
    if len(HOST) != 0:
        break

while True:
    PORT= input('Database Port : \n').encode()
    if len(PORT) != 0:
        break

# Generate a key for encryption
cipher = Fernet(key)

NAME= cipher.encrypt(NAME)
USER= cipher.encrypt(USER)
PASSWORD= cipher.encrypt(PASSWORD)
HOST= cipher.encrypt(HOST)
PORT= cipher.encrypt(PORT)

with open("API_REACT_NATIVE/.env", "w") as file:
    file.write(f"{'NAME'}= {NAME.decode()}\n")
    file.write(f"{'USER'}= {USER.decode()}\n")
    file.write(f"{'PASSWORD'}= {PASSWORD.decode()}\n")
    file.write(f"{'HOST'}= {HOST.decode()}\n")
    file.write(f"{'PORT'}= {PORT.decode()}\n")
    file.write(f"{'KEY'}= {key.decode()}\n")

