import shelve, os
from prettytable import PrettyTable

def showGirlsTable(sort_key='id'):
    db = shelve.open('girls-conf')
    table = PrettyTable(['i', 'id', 'name', 'min', 'max', 'letters_sent'])
    i = 1
    for key in sorted(db.keys()):
        db[key]['letters_sent'] = db[key].get('letters_sent', 0)
        table.add_row([i, key, db[key]['name'], db[key]['min'], db[key]['max'], db[key]['letters_sent']])
        i += 1
    print table.get_string(sortby=sort_key)
    db.close()

def addGirl(id, name, min, max):
    db = shelve.open('girls-conf')
    if id in db.keys():
        return
    db[id] = {
        'name': name,
        'min': min,
        'max':max,
        'letters_sent': 0
    }
    db.close()

def removeGirl(id):
    db = shelve.open('girls-conf')
    if id not in db:
        return
    db.pop(id)
    db.close()

def resetSentLetters():
    db = shelve.open('girls-conf')
    for key in db.keys():
        name = db[key]['name']
        min = db[key]['min']
        max = db[key]['max']
        db[key] = {
            'name': name,
            'min': min,
            'max': max,
            'letters_sent': 0
        }
    db.close

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def printOptions():
    print "[1] Add girl,          [2] Remove girl, [0] Exit"
    print "[3] Sort by Id         [4] Sort by Name"    
    print "[5] Reset Sent Letters"

if __name__ == '__main__':
    sort_by = 'id'
    clearTerminal()
    showGirlsTable(sort_by)
    printOptions()
    choise = raw_input()
    while choise != '0':
        if choise == '1':
            print 'Enter girl id: ',
            girl_id = raw_input()
            print 'Enter girl name: ',
            girl_name = raw_input()
            print 'Enter girl min age range(18): ',
            girl_min = raw_input()
            print 'Enter girl max age range(40): ',
            girl_max = raw_input()
            if not girl_min: girl_min = 18
            if not girl_max: girl_max = 40
            addGirl(girl_id, girl_name, girl_min, girl_max)
        elif choise == '2':
            print 'Enter girl id to remove: ',
            girl_id = raw_input()
            removeGirl(girl_id)
        elif choise == '3':
            sort_by = 'id'
        elif choise == '4':
            sort_by = 'name'
        elif choise == '5':
            resetSentLetters()
        clearTerminal()
        showGirlsTable(sort_by)
        printOptions()
        choise = raw_input()

