"""CodeTrace test file: Bank Account Management System with intentional bugs.

Run: python codetrace_bank_buggy.py
Expected: several self-checks fail because the implementation is intentionally wrong.
"""

class BankAccount:
    def __init__(self, account_id, initial_balance=0):
        self.account_id = account_id
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        # BUG 1: accepts negative deposits.
        if amount == 0:
            return False
        self.balance += amount
        self.transactions.append(("deposit", amount))
        return True

    def withdraw(self, amount):
        # BUG 2: does not reject negative withdrawal amounts.
        if amount > self.balance:
            return False
        self.balance -= amount
        self.transactions.append(("withdraw", amount))
        return True

    def get_balance(self):
        # BUG 3: returns the first recorded transaction amount, not current balance.
        if self.transactions:
            return self.transactions[0][1]
        return self.balance

    def get_transaction_history(self):
        # BUG 4: filters out deposits, so history is incomplete.
        return [tx for tx in self.transactions if tx[0] == "withdraw"]

    def transfer_to(self, other, amount):
        # BUG 5: subtracts from this account but never credits the destination.
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        self.transactions.append(("transfer_out", amount, other.account_id))
        return True


def run_checks():
    checks = []

    a = BankAccount("A", 100)
    checks.append(("Negative deposit rejected", a.deposit(-20) is False))
    checks.append(("Balance unchanged after rejected deposit", a.balance == 100))

    b = BankAccount("B", 100)
    checks.append(("Negative withdrawal rejected", b.withdraw(-10) is False))
    checks.append(("Balance unchanged after rejected withdrawal", b.balance == 100))

    c = BankAccount("C", 100)
    c.deposit(50)
    c.withdraw(20)
    checks.append(("Current balance is 130", c.get_balance() == 130))

    d = BankAccount("D", 100)
    d.deposit(25)
    checks.append(("History includes deposit", ("deposit", 25) in d.get_transaction_history()))

    sender = BankAccount("S", 100)
    receiver = BankAccount("R", 40)
    sender.transfer_to(receiver, 30)
    checks.append(("Receiver credited after transfer", receiver.balance == 70))
    checks.append(("Sender balance after transfer", sender.balance == 70))

    passed = 0
    print("BankAccount Buggy Implementation - Self Checks")
    print("--------------------------------------------")
    for name, ok in checks:
        status = "PASS" if ok else "FAIL"
        print(f"{status}: {name}")
        passed += int(ok)
    print(f"\nResult: {passed}/{len(checks)} checks passed")
    return passed, len(checks)


if __name__ == "__main__":
    run_checks()
