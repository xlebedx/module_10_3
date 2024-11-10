from random import randint
from time import sleep
import threading


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def deposit(self):
        for i in range(100):
            amount = randint(50, 500)
            sleep(0.001)
            with self.lock:
                self.balance += amount
                print(f'Пополнение: {amount}. Баланс: {self.balance}')
                if self.balance >= 500:
                    self.condition.notify_all()

    def take(self):
        for i in range(100):
            amount = randint(50, 500)
            print(f'Запрос на {amount}.')
            sleep(0.001)

            with self.condition:
                while amount > self.balance:
                    print('Запрос отклонён, недостаточно средств')
                    self.condition.wait()
                self.balance -= amount
                print(f'Снятие: {amount}. Баланс: {self.balance}')


if __name__ == '__main__':
    bk = Bank()

    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))

    th1.start()
    th2.start()
    th1.join()
    th2.join()

    print(f'Итоговый баланс: {bk.balance}')
