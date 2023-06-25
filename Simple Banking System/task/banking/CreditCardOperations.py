import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
list_of_tables = cur.execute("""SELECT name \
                                FROM sqlite_master \
                                WHERE type='table' AND name='card'; """).fetchall()
#Creates Database if it does not exist yet
if list_of_tables == []:
    cur.execute('Create Table card (\
                id INTEGER,\
                number TEXT,\
                pin TEXT,\
                balance INTEGER Default 0\
                );')
    conn.commit()


def is_card_in_database(card_number):
    new_card = cur.execute(f"Select \
                                pin,       \
                                balance    \
                            From            \
                                card        \
                            WHERE           \
                                number = {card_number};").fetchall()
    if not new_card:
        return False
    else:
        return True


def add_leading_zeros (number, str_length):
    number = str(number)
    while len(number)<str_length:
        number = '0' + number
    return number


def is_card_valid(number):
    luhn_number = 0
    counter = 1
    for num in number:
        num = int(num)
        if counter % 2 == 1:
            num *= 2
        if num > 9:
            num -= 9
        luhn_number += num
        counter = counter + 1
    luhn_number = luhn_number % 10
    if luhn_number != 0:
        return False
    return True


def create_Luhn_number(number):
    luhn_number = 0
    counter = 1
    for num in number:
        num = int(num)
        if counter % 2 == 1:
            num *= 2
        if num > 9:
            num -= 9
        luhn_number += num
        counter = counter + 1
    luhn_number = luhn_number % 10
    if luhn_number == 0:
        return str(luhn_number)
    return str(10 - luhn_number)


class CreditCards:
    CreditCardList = {}

    def __init__(self, status,card_number):
        if status == 'new':
            print('Your card is being created')
            help_number = '400000' + add_leading_zeros(random.randint(0, 999999999), 9)
            self.card_number = help_number + create_Luhn_number(help_number)
            print('Your card number:')
            print(self.card_number)
            self.Pin = add_leading_zeros(random.randint(0, 9999), 4)
            print(f'Your card PIN:')
            print(self.Pin)
            self.balance = 0
            cur.execute(f"INSERT INTO card \
                           Values(0,{self.card_number},{self.Pin},{self.balance});")
        else:
            new_card = cur.execute(f"Select \
                                        pin,       \
                                        balance    \
                                    From            \
                                        card        \
                                    WHERE           \
                                        number = {card_number};").fetchone()
            self.card_number = card_number
            self.Pin = new_card[0]
            self.balance = new_card[1]
        conn.commit()


    def check_balance(self):
        print(f'The account balance is {self.balance}')

    def log_in(self, pin):
        #input_pin = input('Enter your PIN')
        if pin == self.Pin:
            print('You have successfully logged in!')
            self.account_menu()
            return
        else:
            print('Wrong card number or PIN!')
            return

    def transfer_money(self):
        transfer_number = input('Enter card number: \n')
        if transfer_number == self.card_number:
            print("You can't transfer money to the same account!")
            return
        if not is_card_valid(transfer_number):
            print("Probably you made a mistake in the card number. Please try again!")
            return
        if not is_card_in_database(transfer_number):
            print('Such a card does not exist.')
            return
        transfer_amount = int(input('Enter how much money you want to transfer:'))
        if transfer_amount > self.balance:
            print('Not enough money!')
            return
        transfer_balance = cur.execute(f"Select \
                                balance   \
                            From\
                                card \
                            Where number = {transfer_number}  ;").fetchone()
        transfer_balance = transfer_balance[0]
        transfer_balance += transfer_amount
        self.balance -= transfer_amount
        cur.execute(f"UPDATE card SET balance = {transfer_balance} Where number = {transfer_number} ")
        cur.execute(f"UPDATE card SET balance = {self.balance} Where number = {self.card_number} ")
        conn.commit()

    def input_money(self):
        self.balance += int(input('Enter income'))
        cur.execute(f"Update card \
                                            Set balance = {self.balance}\
                                        where number = {self.card_number} ;")
        conn.commit()

    def close_account(self):
        cur.execute(f"Delete From card Where number = {self.card_number}")
        conn.commit()
        exit_account = True
        print('The account has been closed!')

    def log_out(self):
        exit_account = True
        print('You have succesfully logged out')

    def account_menu(self):
        exit_account = False
        while not exit_account:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close Account')
            print('5. Log out')
            print('0. Exit')
            input_code = int(input())
            match input_code:
                case 1:
                    self.check_balance()
                case 2:
                    self.input_money()
                case 3:
                    self.transfer_money()
                case 4:
                    self.close_account()
                case 5:
                    self.log_out()
                case 0:
                    print('Bye')
                    exit(0)
                case other:
                    print('Invalid input')