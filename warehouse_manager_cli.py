from time import sleep
from urllib.error import URLError
import requests
import os

global NEXT_PAGE
global PREV_PAGE 
global URL
URL = None
NEXT_PAGE = None
PREV_PAGE = None

def menu(token):
    if NEXT_PAGE:
        print('[N]Next page')
    if PREV_PAGE:
        print('[R]Previous page')

    if URL.split('/')[-2].isdecimal():
        print('[S]Set changes \n[D]Delete')
        
    odp = input("[U]User List \n[P]Product List \n[Q]Quit \n: ")

    os.system('cls')
    print("Loading...")

    if odp.isdecimal():
        getDetails(token, URL + odp)
        
    odp = odp.lower()

    if odp == 'n':
        getList(token, NEXT_PAGE)
    elif odp == 'r':
        getList(token, PREV_PAGE)
    elif odp == 'd':
        deleteRecord(token, URL)
    elif odp == 'u':
        getList(token, 'http://localhost:8000/api/users/')
    elif odp == 'p':
        getList(token, 'http://localhost:8000/api/products/')
    elif odp == 'q':
        print('See you later!')
        exit()

def login():
    while True:
        # email = input('Email: ')
        # password = input('Password: ')
        email = 'su@su.su'
        password = 'su'

        req = requests.post('http://localhost:8000/api/login/',data={'email': email, 'password': password})
        if req.status_code == 200:
            response = req.json()
            token = response['Token']
            return token
        else:
            print("Loggin failed \nBad email or password")

def getList(token, url):
    req = requests.get(url, headers={'Authorization': token})

    os.system('cls')

    if req.status_code == 200:
        res = req.json()
        global NEXT_PAGE
        global PREV_PAGE
        global URL
        NEXT_PAGE = res['next']
        PREV_PAGE = res['previous']
        URL = url
        data = res['results']

        for pos in data:
            id = pos['url'].split('/')[-2]
            if 'name' in pos.keys():
                print(f"[{id}]{pos['name']} \n-{pos['description']}")
            else:
                print(f"[{id}]{pos['first_name']} {pos['last_name']} \n-{pos['phone_number']}\n-{pos['email']}")
            print('-'*25+'\n')
    else:
        print(f"[ERROR] Status code: {req.status_code}")

def getDetails(token, url):
    req = requests.get(url, headers={"Authorization" : token})

    os.system('cls')

    if req.status_code == 200:
        res = req.json()
        global NEXT_PAGE
        global PREV_PAGE
        global URL
        NEXT_PAGE = None
        PREV_PAGE = None
        URL = url

        for key in res.keys():
            print(f'{key} : {res[key]}')

def deleteRecord(token, url):
    odp = input('Are you sure to delete this? [Y/n]')
    if odp == 'y':
        print('Deleting ...')
        res = requests.delete(url, headers={"Authorization": token})

        if res.status_code == 200:
            print('Deleted succesfully!!!')
            global URL
            URL = None
        else:
            print(f'[ERROR] {res.status_code}')
            sleep(1000)
            getDetails(token, URL)
    else:
        print('Item was not deleted')
        sleep(1000)
        getDetails(token, URL)

def main():
    auth_token = "Token " +login()
    print("Hello")
    if auth_token:
        print('Logged in succesfully!!')
    while True:
        menu(auth_token)


if __name__ == "__main__":
    main()