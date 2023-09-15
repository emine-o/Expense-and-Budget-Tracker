import sqlite3
import string

db = sqlite3.connect("expense and budget")
cursor = db.cursor()

# Create a table of expense
cursor.execute("""CREATE TABLE expense
               (Category VARCHAR, Amount FLOAT(2), Budget DECIMAL(20,2))""")

# Create a table of income
cursor.execute("""CREATE TABLE income
               (Category VARCHAR, Amount DECIMAL(20,2))""")

# This prevents errors in further operations.
saving_goal = None

while True:

    # Make a list of expense categories.
    cursor.execute("""SELECT Category FROM expense""")
    existing_expense_category = cursor.fetchall()
    expense_category_list = []
    for row in existing_expense_category:
        temp = "{0}".format(row[0])
        expense_category_list.append(temp)

    # Make a list of income categories.    
    cursor.execute("""SELECT Category FROM income""")
    existing_income_category = cursor.fetchall()
    income_category_list = []
    for row in existing_income_category:
        temp = "{0}".format(row[0])
        income_category_list.append(temp)
    
    menu = input('''
Select one of the following options:
1. Add expense
2. View expenses
3. View expenses by category
4. Add income
5. View income
6. View income by category
7. Set budget for a category
8. View budget for a category
9. Set financial goals
10. View progress towards financial goals
11. Quit
''')
    
    # Execute if menu choice is "Add expense".
    if menu == "1":

        # Present a submenu to the user.
        add_menu = input('''
Select an option:
a. Create a new category to add expense
b. Select from existing categories to update expense
c. Delete a category                       
''')

        # Execute if menu choice is "Create a new category to add expense".
        if add_menu == "a":

            valid_option = False
            while valid_option == False:

                expense_category = input("\nEnter a category name for the expense: ")
                # Make sure the format of the text that user entered matches the text in table.
                expense_category = string.capwords(expense_category).strip()

                # Prevent the user to enter an existing category name.
                if expense_category in expense_category_list:
                    print("This category already exists. Try again.")
                else:
                    valid_option = True

            valid_option = False
            while valid_option == False:
                # This try-except block prevents error if the users enters an invalid input.
                try:
                    expense_amount = float(input("Enter the amount of the expense: "))
                    valid_option = True
            
                except ValueError:
                    print("\nInvalid input! Please enter a valid amount.\n")
        
            # Add category name and amount the user entered into the expense table.
            # Budget value is "0" as default.
            cursor.execute("""INSERT INTO expense VALUES (?, ?, ?)""", (expense_category, expense_amount, None))
            db.commit

            # Inform user what happened.
            print(f'''
The expense has been added as below:
Category: {expense_category}
Amount: {expense_amount}
''')

        # Execute if menu choice is "Select from existing categories to update expense".
        elif add_menu == "b":

            # Check if any category name had been added before.
            if expense_category_list == []:
                print("\nThere is no category to select.")
            else:
                # List the category names to select from.
                category_name = input('''
Enter a category name from the list:
{0}
                                    
'''.format("\n".join(expense_category_list)))
                # Make sure the format of the text that user entered matches the text in table.
                category_name = string.capwords(category_name).strip()
                
                valid_option = False
                while valid_option == False:
                    # This try-except block prevents error if the users enters an invalid input.
                    try:
                        expense_amount = float(input("Enter the amount of the expense: "))
                        valid_option = True
                
                    except ValueError:
                        print("\nInvalid input! Please enter a valid amount.\n")
                
                # Update the expense amount in the expense table.
                cursor.execute("""UPDATE expense SET Amount = ? WHERE Category = ?""", (expense_amount, category_name))
                db.commit
                
                # Inform user what happened.
                print(f'''
The expense has been updated as below:
Category: {category_name}
Amount: {expense_amount}
''')

        # Execute if menu choice is "Delete a category".
        elif add_menu == "c":

            # Check if any category name had been added before.
            if expense_category_list == []:
                print("\nThere is no category to delete.")
            else:
                # List the category names to select from.
                category_name = input('''
Enter a category name from the list to delete:
{0}
'''.format("\n".join(expense_category_list)))
                # Make sure the format of the text that user entered matches the text in table.
                category_name = string.capwords(category_name).strip()

                # Delete category the user entered from the expense table.
                cursor.execute("""DELETE FROM expense WHERE Category = ?""", (category_name,))
                db.commit
                # Inform user what happened.
                print(f"\nThe expense category '{category_name}' has been deleted.\n")

        # Make user to enter a valid menu option.
        else:
            print("\nInvalid input! Please enter the index number of an option.\n")

    # Execute if menu choice is "View expense".
    elif menu == "2":

        # Check if any category name had been added before.
        if expense_category_list == []:
            print("\nTotal expense: 0")
        else:
            # Calculate and print total expense..
            cursor.execute("""SELECT SUM(Amount) FROM expense""")
            total_amount = cursor.fetchone()
            print('''\nTotal expense: {0}\n'''.format(total_amount[0]))

        # Print all categories along with respective expense values.
        cursor.execute("""SELECT Category, Amount FROM expense""")
        for row in cursor.fetchall():
            print('''{0} : {1}'''.format(row[0], row[1]))
        db.commit

    # Execute if menu choice is "View expenses by category".
    elif menu == "3":

        # Check if any category name had been added before.
        if expense_category_list == []:
            print("\nThere is no category to view.")
        else:
            category_name = input('''
Enter a category name from the list:
{0}
                              
'''.format("\n".join(expense_category_list)))
            # Make sure the format of the text that user entered matches the text in table.
            category_name = string.capwords(category_name).strip()

            # Print category along with respective expense value.
            cursor.execute("""SELECT Amount FROM expense WHERE Category = ?""", (category_name,))
            category_amount = cursor.fetchone()
            db.commit

            print('''
{0} : {1}
'''.format(category_name, category_amount[0]))
        
    # Execute if menu choice is "Add income".
    elif menu == "4":

        add_menu = input('''
Select an option:
a. Create a new category to add income
b. Select from existing categories to update income
c. Delete a category                       
''')

        # Execute if menu choice is "Create a new category to add income".
        if add_menu == "a":

            valid_option = False
            while valid_option == False:

                income_category = input("\nEnter a category name for the income: ")
                # Make sure the format of the text that user entered matches the text in table.
                income_category = string.capwords(income_category).strip()

                # Prevent the user to enter an existing category name.
                if income_category in income_category_list:
                    print("This category already exists. Try again.")
                else:
                    valid_option = True

            valid_option = False
            while valid_option == False:
                # This try-except block prevents error if the users enters an invalid input.
                try:
                    income_amount = float(input("Enter the amount of the income: "))
                    valid_option = True
            
                except ValueError:
                    print("\nInvalid input! Please enter a valid amount.\n")

            # Add category name and amount the user entered into the income table.
            cursor.execute("""INSERT INTO income VALUES (?, ?)""", (income_category, income_amount))
            db.commit

            # Inform user what happened.
            print(f'''
The income has been added as below:
Category: {income_category}
Amount: {income_amount}
''')
        
        # Execute if menu choice is "Select from existing categories to update income".
        elif add_menu == "b":

            # Check if any category name had been added before.
            if income_category_list == []:
                print("\nThere is no category to select.")
            else:
                # List the category names to select from.
                category_name = input('''
Enter a category name from the list:
{0}
                                  
'''.format("\n".join(income_category_list)))
                # Make sure the format of the text that user entered matches the text in table.
                category_name = string.capwords(category_name).strip()
                
                valid_option = False
                while valid_option == False:
                    # This try-except block prevents error if the users enters an invalid input.
                    try:
                        income_amount = float(input("Enter the amount of the income: "))
                        valid_option = True
                
                    except ValueError:
                        print("\nInvalid input! Please enter a valid amount.\n")
                
                # Update the expense amount in the income table.
                cursor.execute("""UPDATE income SET Amount = ? WHERE Category = ?""", (income_amount, category_name))
                db.commit

                # Inform user what happened.
                print(f'''
The income has been updated as below:
Category: {category_name}
Amount: {income_amount}
''')

        # Execute if menu choice is "Delete a category".
        elif add_menu == "c":

            # Check if any category name had been added before.
            if income_category_list == []:
                print("\nThere is no category to delete.")
            else:
                # List the category names to select from.
                category_name = input('''
Enter a category name from the list to delete:
{0}
                                  
'''.format("\n".join(income_category_list)))
                # Make sure the format of the text that user entered matches the text in table.
                category_name = string.capwords(category_name).strip()

                # Delete category the user entered from the income table.
                cursor.execute("""DELETE FROM income WHERE Category = ?""", (category_name,))
                db.commit
                # Inform user what happened.
                print(f"\nThe income category '{category_name}' has been deleted.\n")

        # Make user to enter a valid menu option.
        else:
            print("\nInvalid input! Please enter the index number of an option.\n")

    # Execute if menu choice is "View income".
    elif menu == "5":

        # Check if any category name had been added before.
        if income_category_list == []:
            print("\nTotal income: 0")
        else:
            # Calculate and print total income..
            cursor.execute("""SELECT SUM(Amount) FROM income""")
            total_amount = cursor.fetchone()
            print('''\nTotal income: {0}\n'''.format(total_amount[0]))

        # Print all categories along with respective income values.
        cursor.execute("""SELECT * FROM income""")
        for row in cursor.fetchall():
            print('''{0} : {1}'''.format(row[0], row[1]))
        db.commit

    # Execute if menu choice is "View income by category".
    elif menu == "6":

        # Check if any category name had been added before.
        if income_category_list == []:
            print("\nThere is no category to view.")
        else:
            category_name = input('''
Enter a category name from the list:
{0}
                              
'''.format("\n".join(income_category_list)))
            # Make sure the format of the text that user entered matches the text in table.
            category_name = string.capwords(category_name).strip()

            # Print category along with respective expense value.
            cursor.execute("""SELECT Amount FROM income WHERE Category = ?""", (category_name,))
            category_amount = cursor.fetchone()
            db.commit

            print('''
{0} : {1}
'''.format(category_name, category_amount[0]))
        
    # Execute if menu choice is "Set budget for a category".
    elif menu == "7":

        # Check if any category name had been added before.
        if expense_category_list == []:
            print("\nThere is no category to view.")
        else:
            # List the category names to select from.
            category_name = input('''
Enter a category name from the list:
{0}
                              
'''.format("\n".join(expense_category_list)))
            # Make sure the format of the text that user entered matches the text in table.
            category_name = string.capwords(category_name).strip()
            budget_amount = input("Enter the budget: ")
            
            # Update the budget value as the user entered.
            cursor.execute("""UPDATE expense SET Budget = ? WHERE Category = ?""", (budget_amount, category_name))
            db.commit

            # Inform user what happened.
            print(f'''
The budget has been added as below:
Category: {category_name}
Budget: {budget_amount}
''')
                
    # Execute if menu choice is "View budget for a category".
    elif menu == "8":

        # Check if any category name had been added before.
        if expense_category_list == []:
            print("\nThere is no category to view.")
        else:
            # List the category names to select from.
            category_name = input('''
Enter a category name from the list:
{0}
                              
'''.format("\n".join(expense_category_list)))
            # Make sure the format of the text that user entered matches the text in table.
            category_name = string.capwords(category_name).strip()
            
            # Select budget amount with respective category.
            cursor.execute("""SELECT Budget FROM expense WHERE Category = ?""", (category_name,))
            budget_amount = cursor.fetchone()
            budget_amount = budget_amount[0]
            db.commit

            # Check if any budget had been set before.
            if budget_amount == None:
                print(f"\nBudget for {category_name} has not been set yet.")
            else:
                # Print the category along with the respective budget value.
                print('''
Budget for {0}: {1}
'''.format(category_name, budget_amount))

    # Execute if menu choice is "Set financial goals".
    elif menu == "9":

        valid_option = False
        while valid_option == False:
            # This try-except block prevents error if the users enters an invalid input.
            try:
                saving_goal = float(input("\nEnter the amount you intend to save: "))
                valid_option = True
            
            except ValueError:
                print("\nInvalid input! Please enter a valid amount.\n")
        
        # Print the saving goal value the user entered.
        print(f"\nSaving goal : {saving_goal}\n")

    # Execute if menu choice is "View progress towards financial goals".
    elif menu == "10":

        # Check if saving goal had been set before.
        if saving_goal != None:

            if expense_category_list == []:
                # Set total expense to "0" if no expense category had been added before.
                expense_total_amount = 0
            
            else:
                # Calculate total expense amount.
                cursor.execute("""SELECT SUM(Amount) FROM expense""")
                expense_total_amount = cursor.fetchone()
                expense_total_amount = expense_total_amount[0]
            
            if income_category_list == []:
                # Set total income to "0" if no expense category had been added before.
                income_total_amount = 0
            
            else:
                # Calculate total income amount.
                cursor.execute("""SELECT SUM(Amount) FROM income""")
                income_total_amount = cursor.fetchone()
                income_total_amount = income_total_amount[0]

            saving = income_total_amount - expense_total_amount

            if saving_goal > saving :
                print(f'''
You have not reached your saving goal yet.
Saving goal : {saving_goal}
Saving : {saving}

Total expense: {expense_total_amount}
Total income: {income_total_amount}
''')
            else:
                print(f'''
You have reached your saving goal.
Saving goal : {saving_goal}
Saving : {saving}
''')
                
        else:
            print("\nSaving goal has not been set yet.")

    # Execute if menu choice is "Quit".
    elif menu == "11":
        db.close()
        print("Goodbye")
        exit()

    # Make user to enter a valid menu option.
    else:
        print("\nInvalid input! Please enter the index number of an option.\n")
