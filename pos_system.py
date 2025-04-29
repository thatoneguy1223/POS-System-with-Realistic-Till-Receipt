import os
from datetime import datetime

# Products database (product name -> price)
products = {
    "apple": 1.00,
    "banana": 0.50,
    "milk": 2.50,
    "bread": 3.00,
    "eggs": 2.00
}

# Cart to store selected items
cart = {}

# Sales tax rate (e.g., 7% tax)
TAX_RATE = 0.07

# Sales report data
sales_report = {
    "transactions": [],  # List to store transactions
    "total_sales": 0,    # Total number of sales
    "till_balance": 0.0  # Total amount collected
}

# Function to clear the console screen
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the menu
def display_menu():
    clear_console()
    print("=" * 40)
    print("          Welcome to POS System          ")
    print("=" * 40)
    print("1. Show Products")
    print("2. Add to Cart")
    print("3. View Cart")
    print("4. Checkout")
    print("5. Exit")
    print("=" * 40)

# Function to display available products
def show_products():
    clear_console()
    print("\nAvailable Products:")
    print("-" * 40)
    for product, price in products.items():
        print(f"{product.capitalize():<10} ${price:.2f}")
    print("-" * 40)
    input("\nPress Enter to return to the menu...")

# Function to add a product to the cart
def add_to_cart():
    clear_console()
    show_products()
    product = input("\nEnter the product name to add to the cart: ").lower()
    if product in products:
        try:
            quantity = int(input(f"Enter quantity of {product.capitalize()}: "))
            if quantity <= 0:
                print("Quantity must be greater than zero.")
            else:
                cart[product] = cart.get(product, 0) + quantity
                print(f"\n{quantity}x {product.capitalize()} added to the cart.")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
    else:
        print("\nProduct not found. Please try again.")
    input("\nPress Enter to return to the menu...")

# Function to view the cart
def view_cart():
    clear_console()
    if not cart:
        print("\nYour cart is empty.")
    else:
        print("\nCart Contents:")
        print("-" * 40)
        subtotal = 0
        for product, quantity in cart.items():
            price = products[product] * quantity
            subtotal += price
            print(f"{product.capitalize():<10} x{quantity:<3} ${price:.2f}")
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        print("-" * 40)
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax ({TAX_RATE * 100:.0f}%): ${tax:.2f}")
        print(f"Total: ${total:.2f}")
    input("\nPress Enter to return to the menu...")

# Function to generate a realistic receipt
def generate_receipt(transaction):
    receipt = []
    receipt.append("=".center(32, "="))
    receipt.append("      STORE RECEIPT      ".center(32))
    receipt.append("=".center(32, "="))
    receipt.append(f"Date: {transaction['date']}")
    receipt.append("-" * 32)
    receipt.append("Items:")
    for product, quantity in transaction["items"].items():
        price = products[product] * quantity
        receipt.append(f"{product.capitalize():<15} x{quantity:<3} ${price:.2f}")
    receipt.append("-" * 32)
    receipt.append(f"Subtotal:".ljust(20) + f"${transaction['subtotal']:.2f}")
    receipt.append(f"Tax ({TAX_RATE * 100:.0f}%):".ljust(20) + f"${transaction['tax']:.2f}")
    receipt.append(f"Total:".ljust(20) + f"${transaction['total']:.2f}")
    receipt.append("=" * 32)
    receipt.append("   Thank you for shopping!   ".center(32))
    receipt.append("=" * 32)

    # Print to console
    for line in receipt:
        print(line)

    # Save to a text file
    file_name = f"receipt_{transaction['date'].replace(':', '-').replace(' ', '_')}.txt"
    with open(file_name, "w") as file:
        file.write("\n".join(receipt))
    print(f"\nReceipt saved as {file_name}!")

# Function to checkout
def checkout():
    global sales_report
    clear_console()
    if not cart:
        print("\nYour cart is empty. Add items before checking out.")
    else:
        print("\nCheckout Summary:")
        print("-" * 40)
        subtotal = 0
        for product, quantity in cart.items():
            price = products[product] * quantity
            subtotal += price
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        print("-" * 40)
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax ({TAX_RATE * 100:.0f}%): ${tax:.2f}")
        print(f"Total: ${total:.2f}")
        print("-" * 40)

        # Save transaction to sales report
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": cart.copy(),
            "subtotal": subtotal,
            "tax": tax,
            "total": total
        }
        sales_report["transactions"].append(transaction)
        sales_report["total_sales"] += 1
        sales_report["till_balance"] += total
        
        # Generate receipt
        generate_receipt(transaction)
        
        # Clear the cart after checkout
        cart.clear()
        print("\nThank you for your purchase!")
    input("\nPress Enter to return to the menu...")

# Function to display sales report on exit
def print_sales_report():
    clear_console()
    print("\nSales Report:")
    print("=" * 40)
    print(f"Total Sales: {sales_report['total_sales']}")
    print(f"Till Balance: ${sales_report['till_balance']:.2f}")
    print("-" * 40)
    for transaction in sales_report["transactions"]:
        print(f"Date: {transaction['date']}")
        print("Items:")
        for product, quantity in transaction["items"].items():
            price = products[product] * quantity
            print(f"- {product.capitalize():<10} x{quantity:<3} ${price:.2f}")
        print(f"Subtotal: ${transaction['subtotal']:.2f}")
        print(f"Tax: ${transaction['tax']:.2f}")
        print(f"Total: ${transaction['total']:.2f}")
        print("-" * 40)
    print("\nGoodbye!")
    input("\nPress Enter to exit.")

# Main Program Loop
def main():
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            show_products()
        elif choice == "2":
            add_to_cart()
        elif choice == "3":
            view_cart()
        elif choice == "4":
            checkout()
        elif choice == "5":
            print_sales_report()  # Print sales report when exiting
            break
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to return to the menu...")

# Run the POS system
if __name__ == "__main__":
    main()
