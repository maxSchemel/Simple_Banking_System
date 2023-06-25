import CreditCardOperations
from CreditCardOperations import CreditCards
import sqlite3
# Write your code here


def create_an_account():
    CreditCards('new', 0)


def log_into_account():
    card_number = input('Enter your card number')
    pin_code = input('Enter your pin')
    if CreditCardOperations.is_card_in_database(card_number):
        print('card is in database')
        new_card = CreditCards('old', card_number)
        new_card.log_in(pin_code)
        del new_card
    else:
        print('Wrong card number or PIN!')


exit_signal = False
while not exit_signal:
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    input_code = int(input())
    match input_code:
        case 1:
            create_an_account()
        case 2:
            log_into_account()
        case 0:
            exit_signal = True
        case other:
            print('Invalid input')
