# Implementing feature FND-03

# This feature will allow users to manage their expenses more effectively.

class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount, category, description):
        expense = {
            'amount': amount,
            'category': category,
            'description': description
        }
        self.expenses.append(expense)
        return expense

    def get_expenses(self):
        return self.expenses

# Example usage
if __name__ == '__main__':
    manager = ExpenseManager()
    manager.add_expense(100, 'Food', 'Dinner at restaurant')
    print(manager.get_expenses())