# Write your code here
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute(""
            "CREATE TABLE IF NOT EXISTS card ("
            " id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "number TEXT,pin TEXT,"
            "balance INTEGER DEFAULT 0);"
            "")
# y = cur.execute('SELECT * FROM card')
# print(y.fetchall())
conn.commit()
import random


class Banking_System:
    def __init__(self):
        self.first_6 = 400000  # iin (6 digits)
        self.accounts = dict()
        self.card_no = []
        self.card_num = []

    @staticmethod
    def luhn_checker(card_n):
        for t in range(0, 15, 2):
            card_n[t] = card_n[t] * 2
        for i in range(len(card_n)):
            if card_n[i] > 9:
                card_n[i] -= 9
        s1 = sum(card_n)
        mod1 = s1 % 10
        last1 = 0 if mod1 == 0 else (10 - mod1)
        return last1

    def luhn_generate(self):
        self.card_no = [int(i) for i in str(self.first_6)]
        self.card_num = [int(i) for i in str(self.first_6)]
        seventh_15 = random.sample(range(9), 9)  # accno (9 digits)
        for i in seventh_15:
            self.card_no.append(i)
            self.card_num.append(i)
        self.card_num.append(self.luhn_checker(self.card_no))
        return ''.join(str(i) for i in self.card_num)

    def account_info(self):
        global card_num, card_no
        card = self.luhn_generate()
        # card = ''.join([str(i) for i in self.card_num])
        pin = random.randrange(1000, 9999)
        self.accounts[card] = pin
        cur.execute('INSERT INTO card (number,pin) VALUES (?,?)', (card, pin))
        conn.commit()
        print(f'Your card number:\n{card}\nYour card PIN:\n{pin}')
        return True

    def check_info(self, card_in, pin_in):
        try:
            cur.execute(f'SELECT pin FROM card WHERE number={card_in}')
            fetch_pin = cur.fetchone()[0]
            if fetch_pin == str(pin_in):
                print('\nYou have successfully logged in!')
                return True
        except:
            return False

    def take_action(self):
        while True:
            print('\n1. Create an account\n2. Log into account\n0. Exit')
            try:

                x = input('')
            except:
                exit()
            if x == '1':
                print('\nYour card has been created')
                self.account_info()
            if x == '2':
                print('\nEnter your card number:')
                try:
                    card_in = int(input())
                    print(f'Enter your PIN:')
                    pin_in = int(input())
                except:
                    print('Wrong card number')
                    continue

                if self.check_info(card_in, pin_in):
                    while True:
                        print('\n1. Balance\n2. Add income\n3. Do Transfer\n4. Close Account\n5. Log out\n0. Exit\n')
                        login_info = input('')
                        if login_info == '1':
                            cur.execute(f'SELECT balance FROM card WHERE number={card_in}')
                            bal = cur.fetchone()[0]
                            print(f'\nBalance: {bal}')
                        elif login_info == '5':
                            print('You have successfully logged out!')
                            break
                        elif login_info == '0':
                            print('\nBye!')
                            exit()
                        elif login_info == '2':
                            try:
                                add_amount = int(input('Enter income:\n'))
                                cur.execute(f'UPDATE card SET balance=balance+{add_amount} WHERE number={card_in}')
                                conn.commit()
                                print('Income was added!')
                            except:
                                print('Enter Correct Amount')
                        elif login_info == '3':

                            try:
                                sec_acct = int(input('Transfer\nEnter card number:'))
                                if sec_acct == card_in:
                                    print("You can't transfer money to the same account!")
                                    continue
                                sec_amnt = str(sec_acct)
                                lis = [int(i) for i in sec_amnt[:-1]]
                                y = self.luhn_checker(lis)
                                if y != int(sec_amnt[-1]):
                                    print('Probably you made mistake in the card number. Please try again!')
                                    continue

                                else:
                                    cur.execute(f'SELECT number FROM card WHERE number={sec_acct}')
                                    x = cur.fetchone()
                                    conn.commit()
                                    if x == None:
                                        print('Such a card doesnot exists!')
                                        continue
                                    ded_amnt = int(input('Enter how much money you want to transfer:'))
                                    cur.execute(f'SELECT balance FROM card WHERE number={card_in}')
                                    conn.commit()
                                    fetch_bal = cur.fetchone()[0]
                                if ded_amnt <= fetch_bal:
                                    cur.execute(
                                        f'UPDATE card SET balance=balance-{ded_amnt} WHERE number={card_in};')
                                    conn.commit()
                                    cur.execute(
                                        f'UPDATE card SET balance=balance+{ded_amnt} WHERE number={sec_acct};')
                                    conn.commit()
                                    print('Success!')
                                else:
                                    print('Not enough money!')

                            except:
                                # add luhn else
                                print('Probably you made mistake in the card number. Please try again!')
                        elif login_info == '4':
                            cur.execute(f'DELETE FROM card WHERE number={card_in}')
                            conn.commit()
                            print('The account has been closed!')
                            break
                else:
                    print('Wrong card number or PIN!')

            if x == '0':
                print('\nBye!')
                conn.close()
                exit()


Banking_System().take_action()
conn.close()
