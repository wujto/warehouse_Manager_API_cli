from time import sleep
import requests
import os

HELP = """METHODS: get, post, put, delete 
FIRST PARAM: users, products, localizations, confirmations, categories
<id> for detail, put or delete methods
--page <num> for get method without <id>
--filters <key> <value> ... for get method  without <id>
    FILTER PARAMS:
    -for users (first_name, last_name)
    -for localizations (name, details)
    -for other (name)
EXAMPLE:
    get products --filter name Szlifierka

OTHER COMMANDS:
    q - quit
    cls - clear screan
"""

def experimental_menu(token):
    # <method(get, post, put, delete)> <users, products, localizations, confirmations> [id for details] | --page <value> | --filter <key(first_name, last_name for users) (name, details for localizations) (name for others)> <value> 
    # "http://localhost:8000/api/products/?limit=10&offset=10"    PAGINATION
    # http://localhost:8000/api/products?name=Szlifiera         FILTERING
    inp = input("> ")
    if inp.lower() == 'q':
        print("See you later.")
        exit()
    elif inp.lower() == 'cls':
        os.system('cls')
        return
    elif inp.lower() == 'help':
        print('')
        print(HELP)
        return
    
    is_page = inp.find('--page')        # Check page flag exist
    is_filter = inp.find('--filters')   # Check filters flag exist
    inp = inp.split(' ')
    meth = inp.pop(0)
    sub_link = inp.pop(0)

    url = f'http://localhost:8000/api/{sub_link}/'

    # Set id for detail view
    if is_filter < 0 and is_page < 0 and len(inp):
        detail = inp.pop(0)
        url = f'http://localhost:8000/api/{sub_link}/{detail}/'

    if meth != 'get' and meth != 'delete':
        print("Put or post")

    meth = meth.lower()

    print('Loading data ...')
    try:
        if meth == 'get':
            # Calculating offset for page
            if is_page > 0:
                page = inp[inp.index('--page') + 1]
                url = f"http://localhost:8000/api/{sub_link}/?limit=10&offset={0+10*(int(page)-1)}"

            # Add filters in to url
            if is_filter > 0:
                keys = ['name', 'first_name', 'last_name', 'description']
                f_values = inp[inp.index('--filters')+1 :]
                print(f_values)
                f_keys = [f_values.pop(f_values.index(x)) for x in f_values if x in keys]
                print(f_keys)
                print(f_values)
                url = f'http://localhost:8000/api/{sub_link}?'
                for i, key in enumerate(f_keys):
                    url = url+f'{key}={f_values[i]}' 

            print(f'get: {url}')
            res = requests.get(url, headers={'Authorization' : token})

        elif meth == 'post':
            print(f'post: {url}')
            # res = requests.post(url,data=data, headers={'Authorization' : token})
        elif meth == 'put':
            print(f'put: {url}')
            # res = requests.put(url,data=data, headers={'Authorization' : token})
        elif meth == 'delete':
            a = input(f"Are you sure to delete {sub_link[0:-1]} {detail}? [Y/n] >")
            if a.lower() == 'y':
                print(f'delete: {url}')
                # res = requests.delete(url, headers={'Authorization' : token})
            else:
                print(f"{sub_link[0:-1]} {detail} was not deleted.")
        else:
            print('Method not allowed')
            print("Use 'help' to see usage")
            return

    except:
        print("Something was wrong!")
        print("Use 'help' to see usage")
        return

    if res.status_code == 200:
        print('Success!!')
        data = res.json()
        if meth == 'get':
            data = data['results']
            for x in data:
                for key in x.keys():
                    print(f"< {key} : {x[key]}")
                print('-'*25)
        
        print('')
    else:
        print(f'[ERROR] Status Code: {res.status_code}')

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
        print('Type "help" for usage')
    while True:
        # menu(auth_token)
        experimental_menu(auth_token)


if __name__ == "__main__":
    main()