import csv, re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Constants for menu choices and options
choice_main = 0
choice_check = 0
choice_update = 0
choice_customers = 0
MAIN_MENU = 4
CHECK_OUT = 2
UPDATE_CHARGES = 4
CUSTOMERS_LISTS = 3
TAX_TEXT = "Please, enter the tax rate you want to use in %: "
CHARGE_TEXT = "Please, enter the cost per pound you want to use in $: "

def main(choice_main, choice_check, choice_update, choice_customers):
    # Retrieve initial data values from CSV files
    receipt_number = int(get_value("receipt_number.csv"))
    tax = float(get_value("tax.csv"))
    charge = float(get_value("charge.csv"))
    customer_info = get_dict("customer_info.csv")

    # Reset all choice variables to 0
    choice_main = 0
    choice_check = 0
    choice_update = 0
    choice_customers = 0

     # Main menu loop
    while choice_main != MAIN_MENU:
        main_menu() # Display the main menu
        choice_main = get_choice(MAIN_MENU) # Get the user's menu choice

        if choice_main == 1:

            while choice_check != CHECK_OUT: # If the user selects 'Check-Out'
                check_out_menu() # Show the check-out menu
                choice_check = get_choice(CHECK_OUT)  # Get user's choice for check-out menu

                if choice_check == 1:
                    # Call check-out option and update the receipt number
                    customer_info = check_out_option(tax, charge, receipt_number, customer_info)
                    receipt_number += 1 # Increment the receipt number for the next transaction
            else:
                # If the user chooses to return to the main menu during check-out
                choice_check = return_to_main_menu()

        elif choice_main == 2: # If the user selects 'Update Charges'

            while choice_update != UPDATE_CHARGES:
                update_charges_menu()  # Show the update charges menu
                choice_update = get_choice(UPDATE_CHARGES) # Get user's choice for update charges menu

                if choice_update == 1:
                    # Call update option 1 (to update tax rate)
                    tax = update_option_1()
                elif choice_update == 2:
                    # Call update option 2 (to update charge per pound)
                    charge = update_option_2()
                elif choice_update == 3:
                    # Call update option 3 (to update both tax and charge)
                    tax,charge = update_option_3()
            else:
                # If the user chooses to return to the main menu during charge update
                choice_update = return_to_main_menu()

        elif choice_main == 3: # If the user selects 'Customers Lists'

            while choice_customers != CUSTOMERS_LISTS:
                customers_lists_menu() # Show the customers' list menu
                choice_customers = get_choice(CUSTOMERS_LISTS) # Get user's choice for customer lists menu
                if choice_customers == 1:
                    # Show list of all customers
                    customers_option1(customer_info)
                elif choice_customers == 2:
                    # Show list of top 5 customers
                    customers_option2(customer_info)
            else:
                # If the user chooses to return to the main menu during customers list viewing
                choice_customers = return_to_main_menu()

    else:
        # Once the main menu option is selected as "Quit", save data and exit
        quit_main_menu(tax, charge, customer_info, receipt_number)

def main_menu():
    # Displays the main menu options for the user.
    # Includes options to check out, update charges, view customer lists, or quit.

    print()
    print("==============================")
    print("== Welcome to the Main Menu ==")
    print("==  Available options are:  ==")
    print("==============================")
    print("== 1. Check-Out             ==")
    print("== 2. Update Charges        ==")
    print("== 3. Customers' Lists      ==")
    print("== 4. Quit                  ==")
    print("==============================")
    print()

def check_out_menu():
    # Displays the check-out menu options for the user.
    # Includes options to check out a customer or return to the main menu.

    print()
    print("===================================")
    print("== Welcome to the Check-Out Menu ==")
    print("==    Available options are:     ==")
    print("===================================")
    print("== 1. Check-Out Customer         ==")
    print("== 2. Return to the Main Menu    ==")
    print("===================================")
    print()

def check_out_option(tax, charge, receipt_number,customer_info):
    # Handles the check-out process for a customer.
    # Parameters:
    # - tax: The applicable tax rate.
    # - charge: The cost per pound of laundry.
    # - receipt_number: A unique receipt number for the transaction.
    # - customer_info: A list of dictionaries storing customer details and totals.
    # Returns:
    # - Updated customer_info with new or modified customer details.

    print()
    print("========================================================")
    print('== You have selected the option "Check-Out Customer". ==')
    print("========================================================")
    last_name = get_name() # Retrieves the customer's last name.
    phone_number = get_phone() # Retrieves the customer's phone number.
    customer_id = last_name + str(int(phone_number) % 10000) # Generates a unique customer ID.

    # Display the generated customer ID.
    print()
    print("========================" + "=" * len(customer_id) )
    print(f"== Customer's id is {customer_id}. ==")
    print("========================" + "=" * len(customer_id) )
    print()
    laundry_weight = get_weight() # Retrieves the weight of the laundry.
    subtotal = laundry_weight * charge # Calculates the subtotal.
    tax_total = subtotal * tax  # Calculates the tax amount.
    total = subtotal + tax_total # Calculates the total amount.

    # Display the total cost.
    print("===========================" + "=" * len(str(total)))
    print(f"== Customer's total is ${total:.2f} ==")
    print("===========================" + "=" * len(str(total)))
    print()

    # Print the receipt and update the customer information.
    print("=============================")
    print("== Printing the receipt... ==")
    print("=============================")
    print()
    print_receipt(subtotal, tax_total, total, receipt_number, customer_id)
    print("============================================================")
    print("== Receipt is printed. Returning to the Check-Out Menu... ==")
    print("============================================================")

    # Update customer information with the new transaction details.
    customer_dict = {"customer_id" : customer_id, "last_name" : last_name, "phone_number" : phone_number, "annual_total" : total}
    count = 0
    for customer in customer_info:
        if customer_dict["customer_id"] == customer["customer_id"]:
            customer["annual_total"] = str(float(customer["annual_total"]) + total)
            count = 0
            break
        else:
            count += 1
    if count >= 1:
        customer_info.append(customer_dict)
    return customer_info

def update_charges_menu():
    # Displays the update charges menu options for the user.
    # Includes options to update tax rate, cost per pound, or both.

    print()
    print("============================================")
    print("==   Welcome to the Update Charges Menu   ==")
    print("==         Available options are:         ==")
    print("============================================")
    print("== 1. Update the tax rate                 ==")
    print("== 2. Update the cost per pound           ==")
    print("== 3. Update both, tax and cost per pound ==")
    print("== 4. Return to the Main Menu             ==")
    print("============================================")
    print()

def update_option_1():
    # Handles the process of updating the tax rate.
    # Prompts the user to confirm the new tax rate before saving changes.
    # Returns:
    # - The updated tax rate if the user confirms the change.
    # - None if the user cancels the update.

    print()
    print("=========================================================")
    print('== You have selected the option "Update the tax rate". ==')
    print("=========================================================")
    print()
    tax = get_tax_or_charge(TAX_TEXT) # Retrieves the new tax rate from the user.

    # Display a confirmation message with the new tax rate.
    print()
    print("=====================================================================" + "=" * len(str(tax*100)))
    print(f"== Are you sure that you want to change your current tax rate to {tax*100}%?==")
    print("=====================================================================" + "=" * len(str(tax*100)))
    print()

    # Loop to handle user confirmation or cancellation.
    while True:
        y_n = input('Please, enter "Y" to update your tax rate or "N" to cancel your changes: ').strip().casefold()
        if y_n == "y":
            # Confirm and save the new tax rate.
            print()
            print("=====================================================" + "=" * len(str(tax*100)))
            print(f"== You have succesfully changed your tax rate to {tax*100}% ==")
            print("=====================================================" + "=" * len(str(tax*100)))
            print()
            print("=============================================")
            print("== Returning to the Update Charges Menu... ==")
            print("=============================================")
            print()
            return tax
        elif y_n == "n":
            # Cancel the update and return to the menu.
            print()
            print("=========================================")
            print("== You canceled your updated tax rate. ==")
            print("=========================================")
            print()
            print("=============================================")
            print("== Returning to the Update Charges Menu... ==")
            print("=============================================")
            print()
            break
        else:
            # Handle invalid input.
            print()
            print("=====================================")
            print("== Error! Please, use only Y or N. ==")
            print("=====================================")
            print()




def update_option_2():
    # Handles the process of updating the cost per pound.
    # Prompts the user to confirm the new cost per pound before saving changes.
    # Returns:
    # - The updated cost per pound if the user confirms the change.
    # - None if the user cancels the update.

    print()
    print("===============================================================")
    print('== You have selected the option "Update the cost per pound". ==')
    print("===============================================================")
    print()
    charge = get_tax_or_charge(CHARGE_TEXT) # Retrieves the new cost per pound from the user.

    # Display a confirmation message with the new cost per pound.
    print()
    print("=============================================================================" + "=" * len(str(charge)))
    print(f"== Are you sure that you want to change your current cost per pound to ${charge}? ==")
    print("============================================================================" + "=" * len(str(charge)))
    print()

    # Loop to handle user confirmation or cancellation.
    while True:
        y_n = input('Please, enter "Y" to update your tax rate or "N" to cancel your changes: ').strip().casefold()
        if y_n == "y":
            # Confirm and save the new cost per pound.
            print()
            print("============================================================" + "=" * len(str(charge)))
            print(f"== You have succesfully changed your cost per pound to ${charge} ==")
            print("===========================================================" + "=" * len(str(charge)))
            print()
            print("=============================================")
            print("== Returning to the Update Charges Menu... ==")
            print("=============================================")
            print()
            return charge
        elif y_n == "n":
            # Cancel the update and return to the menu.
            print()
            print("===============================================")
            print("== You canceled your updated cost per pound. ==")
            print("===============================================")
            print()
            print("=============================================")
            print("== Returning to the Update Charges Menu... ==")
            print("=============================================")
            print()
            break
        else:
            # Handle invalid input.
            print()
            print("=====================================")
            print("== Error! Please, use only Y or N. ==")
            print("=====================================")
            print()


def update_option_3():
    # Handles the process of updating both the tax rate and the cost per pound.
    # Prompts the user to confirm the new values for both before saving changes.
    # Returns:
    # - The updated tax rate and cost per pound if the user confirms the change.
    # - None if the user cancels the update.

    print()
    print("=========================================================================")
    print('== You have selected the option "Update both, tax and cost per pound". ==')
    print("=========================================================================")
    print()
    charge = get_tax_or_charge(CHARGE_TEXT) # Retrieves the new cost per pound from the user.
    tax = get_tax_or_charge(TAX_TEXT) # Retrieves the new tax rate from the user.

    # Display a confirmation message with both new values.
    print()
    print("======================================================================================================" + "=" * len(str(charge)) + "=" * len(str(tax*100)))
    print(f"== Are you sure that you want to change your current cost per pound to ${charge} and current tax rate to {tax*100}%? ==")
    print("======================================================================================================" + "=" * len(str(charge)) + "=" * len(str(tax*100)))
    print()

    # Loop to handle user confirmation or cancellation.
    while True:
        y_n = input('Please, enter "Y" to update your tax rate or "N" to cancel your changes: ').strip().casefold()
        if y_n == "y":
            # Confirm and save the new cost per pound and tax rate.
            print()
            print("=============================================================================" + "=" * len(str(charge)) + "=" * len(str(tax*100)))
            print(f"== You have succesfully changed your cost per pound to ${charge} and tax rate to {tax*100}% ==")
            print("=============================================================================" + "=" * len(str(charge)) + "=" * len(str(tax*100)))
            print()
            print("=============================================")
            print("== Returning to the Update Charges Menu... ==")
            print("=============================================")
            print()
            return tax, charge
        elif y_n == "n":
            # Cancel the update and return to the menu.
            print()
            print("============================================================")
            print("== You canceled your updated cost per pound and tax rate. ==")
            print("============================================================")
            print()
            print("=============================================")
            print("== Returning to the Update Charges Menu... ==")
            print("=============================================")
            print()
            break
        else:
            # Handle invalid input.
            print()
            print("=====================================")
            print("== Error! Please, use only Y or N. ==")
            print("=====================================")
            print()

def customers_lists_menu():
    # Displays the customer list menu options for the user.
    # Includes options to view all customers, view the top 5 customers, or return to the main menu.

    print()
    print("==========================================")
    print("== Welcome to the Customers' Lists Menu ==")
    print("==        Available options are:        ==")
    print("==========================================")
    print("== 1. View List of all Customers        ==")
    print("== 2. View List of Top 5 Customers      ==")
    print("== 3. Return to the Main Menu           ==")
    print("==========================================")
    print()

def customers_option1(customer_info):
    # Displays a list of all customers sorted by their annual spending.
    # If there are no customers, it notifies the user.
    # Returns to the customers list menu after displaying the list.

    print()
    print("================================================================")
    print('== You have selected the option "View List of all Customers". ==')
    print("================================================================")
    print()
    if customer_info == []:
        # Notify the user if there are no customers.
        print("================================================================")
        print("==            Your List of all Customers is empty.            ==")
        print("================================================================")
        print()
        print("===============================================")
        print("== Returning to the Customer's Lists Menu... ==")
        print("===============================================")
        print()
    else:
        # Display the list of all customers, sorted by annual spending.
        print("================================================================")
        print("==                    List of all Customers                   ==")
        print("================================================================")
        print("==                                                            ==")
        n = len("================================================================")
        i = 1
        for customer in sorted(customer_info, key=lambda d: float(d["annual_total"]), reverse=True):
            k = 25 + len(customer["customer_id"]) + len(str(customer["annual_total"]))
            j = n - k - 6
            print(f"== {i}. {customer['customer_id']} has spent {float(customer['annual_total']):.2f}$ over time {j * ' '}==")
            i += 1
        else:
            print("==                                                            ==")
            print("================================================================")
        print()
        print("===============================================")
        print("== Returning to the Customer's Lists Menu... ==")
        print("===============================================")
        print()

def customers_option2(customer_info):
    # Displays a list of the top 5 customers sorted by their annual spending.
    # If there are fewer than 5 customers, it displays the available ones.
    # Returns to the customers list menu after displaying the list.

    print()
    print("==================================================================")
    print('== You have selected the option "View List of Top 5 Customers". ==')
    print("==================================================================")
    print()
    if customer_info == []:
        # Notify the user if there are no customers.
        print("==================================================================")
        print("==            Your List of Top 5 Customers is empty.            ==")
        print("==================================================================")
        print()
        print("===============================================")
        print("== Returning to the Customer's Lists Menu... ==")
        print("===============================================")
        print()
    else:
        # Display the list of top 5 customers, sorted by annual spending.
        print("==================================================================")
        print("==                   List of Top 5 Customers                    ==")
        print("==================================================================")
        print("==                                                              ==")
        n = len("==================================================================")
        i = 1
        for customer in sorted(customer_info, key=lambda d: float(d["annual_total"]), reverse=True)[:5]:
            k = 25 + len(customer["customer_id"]) + len(str(customer["annual_total"]))
            j = n - k - 6
            print(f"== {i}. {customer['customer_id']} has spent {float(customer['annual_total']):.2f}$ over time {j * ' '}==")
            i += 1
        else:
            print("==                                                              ==")
            print("==================================================================")
        print()
        print("===============================================")
        print("== Returning to the Customer's Lists Menu... ==")
        print("===============================================")
        print()


def return_to_main_menu():
    # Prints a message indicating return to the main menu and returns a choice (0)
    print()
    print("===================================")
    print("== Returning to the Main Menu... ==")
    print("===================================")
    print()
    choice = 0 # Placeholder for the user's menu choice
    return int(choice)

def get_choice(n):
    # Prompts the user to choose an option from the available options
    while True:
        try:
            choice = int(input("Please, select the option you want to use: "))
            # Checks if the entered choice is valid
            if 0 < choice <= n:
                return choice
            else:
                print()
                print("=====================================================")
                print("== Error! Option does not exist. Please, try again ==")
                print("=====================================================")
                print()
                continue
        except ValueError:
            # Error handling for non-integer inputs
            print()
            print("===================================")
            print("== Error! Please, use an integer ==")
            print("===================================")
            print()

def get_name():
    # Prompts for the customer's last name and ensures it's a valid string with no spaces and alphabetic characters
    while True:
        try:
            print()
            name = input("Please, enter customer's last name: ").strip().capitalize()
            print()
            if " " not in name and name.isalpha() and name != "":
                return name
            else:
                raise TypeError # Raises error if input is invalid
        except TypeError:
            print("======================================")
            print("== Error! Please, use letters only. ==")
            print("======================================")


def get_phone():
    # Prompts for the customer's phone number and validates its format using regular expressions
    while True:
        try:
            phone = input("Please, enter customer's phone number: ")
            # Regular expression to validate phone number format
            matches = re.match(r'(?:\+1)?(?: )*(?:\()?(\d+)(?:\))?(?: )*(?:-)?(?: )*(\d+)(?: )*(?:-| )?(?: )*(\d+)(?: )*', phone)
            phone_number = ""
            phone_number += matches.group(1) + matches.group(2) + matches.group(3)
            # Ensures the phone number has exactly 10 digits
            if len(phone_number) == 10 and phone_number.isdigit():
                return phone_number
            else:
                print()
                print("=========================================")
                print("== Error! The phone number is invalid. ==")
                print("=========================================")
                print()
        except (ValueError, AttributeError):
                print()
                print("=========================================")
                print("== Error! The phone number is invalid. ==")
                print("=========================================")
                print()

def get_weight():
    # Prompts for the customer's laundry weight and ensures the value is a positive float
    while True:
        try:
            weight = float(input("Please, enter customer's laundry weight: ").strip())
            print()
            if weight >= 0:
                return weight
            else:
                continue # Loops again if weight is negative
        except ValueError:
            # Handles invalid weight input
            print()
            print("=====================================================")
            print("== Error! Invalid value. Please, check your input. ==")
            print("== Correct patterns: 0.21 | 11.2 | 10.52 | 0.6 | 1 ==")
            print("=====================================================")
            print()

def print_receipt(subtotal, tax_total, total, receipt_number, customer_id):
    # Generates a PDF receipt using the FPDF library, containing transaction details
    pdf = FPDF(unit="mm", format="A5")  # Set page format to A5 (half of A4)
    pdf.add_page()
    pdf.set_font("Courier", size=12)
    # Adds receipt details including subtotal, tax, total, and customer information
    pdf.cell(0, 8, "===========================", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "==        RECEIPT        ==", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "===========================", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, f" Receipt Number: {receipt_number} ", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, f" Customer ID: {customer_id} ", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "===========================", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "== Service:              ==", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "==    Wash-Dry-Fold      ==", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "== Subtotal:             ==", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, f"   $ {subtotal:.2f}", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "== Tax:                  ==", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, f"   $ {tax_total:.2f}", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "== Total:                ==", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, f"   $ {total:.2f}", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "===========================", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "==      Thank You!!      ==", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "==   Have a Great Day!   ==", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 8, "===========================", new_x=XPos.LEFT, new_y=YPos.NEXT, align='C')
    pdf.output("receipt" + str(receipt_number) + ".pdf") # Saves the receipt as a PDF file

def get_tax_or_charge(text):
    # Prompts the user to enter either a tax rate or a charge value, validates input, and returns the value
    while True:
        try:
            value = input(text).strip() # Accepts input and removes any leading/trailing spaces
            return_value = float(value) # Converts the input value to a float
            if text == "Please, enter the tax rate you want to use in %: " and (return_value < 0 or return_value > 100):
                # Validates that tax rate is between 0 and 100
                raise TypeError
            if text == "Please, enter the tax rate you want to use in %: " and 0 <= return_value <= 100:
                return return_value/100 # Converts percentage to decimal
            else:
               return return_value # Returns the charge value as it is
        except (ValueError,AttributeError):
            # Catches non-numeric input and prompts the user to enter a valid number
            print()
            print("==================================")
            print("== Error! Please, use a number. ==")
            print("==================================")
            print()
        except TypeError:
            # Catches invalid tax rate input (less than 0 or greater than 100)
            print()
            print("====================================================================")
            print("== Error! Tax rate can not be less than 0% and greater than 100%. ==")
            print("====================================================================")
            print()


def get_value(value_file):
    # Reads the first value from a CSV file and returns it as a float
    with open(value_file, "r") as file:
        reader = csv.reader(file)
        for line in reader:
            value = line # Reads the line in the CSV file
            return float(value[0]) # Returns the first value in the line as a float

def get_dict(file_name):
    # Reads a CSV file and returns its contents as a list of dictionaries
    with open(file_name, "r") as file:
        reader = csv.DictReader(file)
        dict_list = [] # List to store dictionary rows
        for row in reader:
            dict_list.append(row)  # Appends each row (as a dictionary) to the list
        return dict_list # Returns the list of dictionaries

def save_value(file_name, value):
    # Saves a single value (as a list) to a CSV file
    with open(file_name, "w") as file:
        writer = csv.writer(file)
        writer.writerow(value) # Writes the value to the CSV file

def save_values(tax, charge, receipt_number):
    # Saves tax, charge, and receipt number to respective CSV files
    tax_list = []
    charge_list = []
    receipt_list = []
    receipt_list.append(receipt_number) # Appends receipt number to the list
    tax_list.append(tax) # Appends tax value to the list
    charge_list.append(charge) # Appends charge value to the list
    save_value("receipt_number.csv", receipt_list) # Saves receipt number
    save_value("tax.csv", tax_list) # Saves tax value
    save_value("charge.csv", charge_list) # Saves charge value

def save_dict(customer_info):
    # Saves a list of customer information (in dictionary format) to a CSV file
    with open("customer_info.csv", "w") as file:
        fieldnames = ["customer_id", "last_name", "phone_number", "annual_total"]
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        writer.writeheader() # Writes the header row with field names
        for customer in customer_info:
            writer.writerow(customer) # Writes each customer's data to the file

def quit_main_menu(tax, charge, customer_info, receipt_number):
        # Handles the "Quit" option in the menu, saves all relevant data, and displays a goodbye message
        print()
        print("=========================================")
        print('== You have selected the option "Quit" ==')
        print("=========================================")
        print("==           Have a Good One!          ==")
        print("==               ByeBye!               ==")
        print("=========================================")
        # Saves tax, charge, and receipt number to CSV files
        save_values(tax,charge,receipt_number)
        # Saves customer information to a CSV file
        save_dict(customer_info)





# Run the Laundry App
if __name__ == "__main__":
    main(choice_main, choice_check, choice_update, choice_customers)

