import shelve, os
from prettytable import PrettyTable

def showOptionsTable():
    db = shelve.open('options')
    table = PrettyTable(['option', 'value'])
    for key in db.keys():
        table.add_row([key, db[key]])
    print table.get_string()
    db.close()

def toggleDebug():
    db = shelve.open('options')
    db['debug'] = not db['debug']
    db.close()

def toggleLastLoginSortOrder():
    db = shelve.open('options')
    db['last_login_sort_order'] = not db['last_login_sort_order']
    db.close()
    
def toggleOnlyWithPhotos():
    db = shelve.open('options')
    db['only_with_photos'] = not db['only_with_photos']
    db.close()

def changeNumberOfLettersPerGirl(number):
    db = shelve.open('options')
    db['number_of_letters_per_one_girl'] = number
    db.close()

def changeLogin(login):
    db = shelve.open('options')
    db['login'] = login
    db.close()

def changePassword(password):
    db = shelve.open('options')
    db['password'] = password
    db.close()

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def printOptions():
    print '[1] Toggle debug mode'
    print '[2] Toggle last login sort order'
    print '[3] Change number of letters per girl'
    print '[4] Change login'
    print '[5] Change password'
    print '[6] Only with photos'
    print '[0] Exit'

if __name__ == '__main__':
    clearTerminal()
    showOptionsTable()
    printOptions()
    choise = raw_input()
    while choise != '0':
        if choise == '1':
            toggleDebug()
        elif choise == '2':
            toggleLastLoginSortOrder()
        elif choise == '3':
            print 'Enter number of letters: ',
            number = raw_input()
            changeNumberOfLettersPerGirl(number)
        elif choise == '4':
            login = raw_input()
            changeLogin(login)
        elif choise == '5':
            password = raw_input(password)
            changePassword(password)
        elif choise == '6':
            toggleOnlyWithPhotos()
        clearTerminal()
        showOptionsTable()
        printOptions()
        choise = raw_input()
