import pip
import os

def install(package):
    pip.main(['install', package])

def save_key():
    phantom_key = input("Введите секретную фразу от Phantom: ") + "\n"
    with open("phantom.txt", "w") as f:
        f.write(phantom_key)

def save_password():
    phantom_key = input("Введите пароль от Phantom: ")
    with open("phantom.txt", "a") as f:
        f.write(phantom_key)

if __name__ == '__main__':
    install('selenium')
    os.system('CLS')
    save_key()
    os.system('CLS')
    save_password()
    print ("Всё готово")