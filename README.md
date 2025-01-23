# Laundry-Management-System-Python

Here’s the full README file with all the information in one place:

## Overview
This is a simple Python-based Laundry Management System that allows users to manage customers' laundry check-out, update charges, and view customer information. The system includes features like setting tax rates, charge rates, checking out customers, and saving customer data to CSV files.

### Features
- **Main Menu**: Choose between check-out, update charges, or view customers.
- **Check-Out**: Allows you to process a customer's laundry, calculate totals, and generate receipts.
- **Update Charges**: Change tax rates and charge per pound.
- **Customer Lists**: View customer information.
- **PDF Receipt Generation**: After check-out, generate a receipt for the customer in PDF format.
- **Data Persistence**: Customer information, receipts, and rates are saved to CSV files.

## Technologies Used
- Python
- `csv` for data storage
- `re` for regular expressions (for phone number validation)
- `fpdf` for generating PDF receipts

## Files
1. `main.py`: Main script that runs the menu system and interacts with the user.
2. `customer_info.csv`: Stores customer information (ID, last name, phone number, and annual total).
3. `tax.csv`: Stores the current tax rate.
4. `charge.csv`: Stores the cost per pound for laundry.
5. `receipt_number.csv`: Stores the receipt number for tracking.
6. `fpdf` library: Used for generating PDF receipts.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. You also need to install the following Python libraries:

```bash
pip install fpdf
```

##Functions

1.
``` python
main(choice_main, choice_check, choice_update, choice_customers)
```
Main function that starts the menu-driven program and keeps track of user choices.

``` python
get_choice(n)
```
Prompts the user to choose an option and returns the valid option.

4.
``` python
get_name()
```
Prompts for the customer's last name and ensures it is valid.

5.
``` python
get_phone()
```
Prompts for the customer's phone number and ensures it matches a valid format.

6.
``` python
get_weight()
```
Prompts for the customer's laundry weight and ensures it's a valid number.

7.
``` python
print_receipt(subtotal, tax_total, total, receipt_number, customer_id)
```
Generates and saves a PDF receipt with details of the transaction.

8.
``` python
get_tax_or_charge(text)
```
Prompts the user for a tax or charge value, ensuring it is a valid number.

9.
``` python
get_value(value_file)
```
Reads a value (e.g., tax or charge rate) from a CSV file.

10.
``` python
get_dict(file_name)
```
Reads customer information from a CSV file and returns it as a list of dictionaries.

11.
``` python
save_value(file_name, value)
```
Saves a value (e.g., receipt number, tax, or charge) to a CSV file.

12.
``` python
save_values(tax, charge, receipt_number)
```
Saves tax rate, charge rate, and receipt number to CSV files.

13.
``` python
save_dict(customer_info)
```
Saves customer information to a CSV file.

14.
``` python
quit_main_menu(tax, charge, customer_info, receipt_number)
```
Displays a goodbye message and saves all data before quitting the program.

##Example Usage

When the program runs, the user is presented with a menu. The user can choose from the following options:

- Check Out: Process a customer's laundry, including calculating costs, taxes, and generating a PDF receipt.
- Update Charges: Change the tax rate or charge rate for laundry services.
- Customers List: View a list of customers.
- Quit: Exit the program and save all current data.
Each operation is accompanied by appropriate prompts to gather user input.
