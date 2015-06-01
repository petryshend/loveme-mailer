import shelve

options = shelve.open('options')

DEBUG = options['debug']

LOGIN = options['login']

PASSWORD = options['password']

LAST_LOGIN_SORT_ORDER = options['last_login_sort_order']

NUMBER_OF_LETTERS_PER_ONE_GIRL = int(options['number_of_letters_per_one_girl'])

GIRLS_WITH_INTRO_LETTERS = shelve.open('girls-conf')