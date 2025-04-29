import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from reportlab.pdfgen import canvas

# Products database (product name -> price)
products = {
    "Apple": 1.00,
    "Banana": 0.50,
    "Milk": 2.50,
    "Bread": 3.00,
    "Eggs": 2.00
}

# Cart to store selected items
cart = {}

# Sales tax rate
TAX_RATE = 0.07

# Sales report
sales_report = {
    "transactions": [],
    "total_sales": 0,
    "till_balance": 0.0
}

def show_splash_screen():
    """Display a splash screen with Crimson Forge logo."""
    splash = tk.Tk()
    splash.title("Welcome to Crimson Forge")
    splash.geometry("600x400")
    splash.configure(bg="#282828")  # Dark background for branding

    # Load logo image (ensure the file is in the same directory)
    try:
        logo_image = tk.PhotoImage(file="crimson_forge_logo.png")
        logo_label = tk.Label(splash, image=logo_image, bg="#282828")
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.pack(pady=20)
    except Exception as e:
        logo_label = tk.Label(splash, text="Crimson Forge", font=("Helvetica", 32, "bold"), fg="#FF4500", bg="#282828")
        logo_label.pack(pady=20)
        print(f"Could not load logo image. Error: {e}")

    # Add tagline or title
    tagline_label = tk.Label(
        splash,
        text="Innovative POS Solutions for Your Business",
        font=("Arial", 16, "italic"),
        fg="white",
        bg="#282828"
    )
    tagline_label.pack(pady=10)

    # Display splash for 3 seconds
    splash.after(3000, splash.destroy)
    splash.mainloop()

def update_cart():
    """Update the cart view."""
    cart_list.delete(*cart_list.get_children())
    subtotal = 0
    for item, quantity in cart.items():
        price = products[item] * quantity
        subtotal += price
        cart_list.insert("", "end", values=(item, quantity, f"${price:.2f}"))
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
    tax_label.config(text=f"Tax ({TAX_RATE*100:.0f}%): ${tax:.2f}")
    total_label.config(text=f"Total: ${total:.2f}")

def add_to_cart():
    """Add products to the cart."""
    product = product_var.get()
    quantity = quantity_var.get()
    if product and quantity.isdigit() and int(quantity) > 0:
        cart[product] = cart.get(product, 0) + int(quantity)
        update_cart()
        messagebox.showinfo("Success", f"Added {quantity} x {product} to the cart.")
    else:
        messagebox.showwarning("Invalid Input", "Please select a product and enter a valid quantity.")

def checkout():
    """Process checkout and generate receipt."""
    if not cart:
        messagebox.showwarning("Empty Cart", "Your cart is empty. Add items before checkout.")
        return

    subtotal = sum(products[item] * quantity for item, quantity in cart.items())
    tax = subtotal * TAX_RATE
    total = subtotal + tax

    # Create receipt text
    receipt = f"Receipt - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    receipt += "-"*40 + "\n"
    for item, quantity in cart.items():
        price = products[item] * quantity
        receipt += f"{item:<15} x{quantity:<3} ${price:.2f}\n"
    receipt += "-"*40 + "\n"
    receipt += f"Subtotal: ${subtotal:.2f}\n"
    receipt += f"Tax ({TAX_RATE*100:.0f}%): ${tax:.2f}\n"
    receipt += f"Total: ${total:.2f}\n"
    receipt += "-"*40 + "\nThank you for shopping!\n"

    # Save transaction in sales report
    transaction = {
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "items": cart.copy(),
        "subtotal": subtotal,
        "tax": tax,
        "total": total
    }
    sales_report["transactions"].append(transaction)
    sales_report["total_sales"] += 1
    sales_report["till_balance"] += total

    # Generate PDF receipt
    pdf_name = f"receipt_{transaction['date'].replace(':', '-').replace(' ', '_')}.pdf"
    pdf = canvas.Canvas(pdf_name)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 750, "Receipt")
    pdf.drawString(50, 730, f"Date: {transaction['date']}")
    y_position = 710
    for item, quantity in transaction["items"].items():
        price = products[item] * quantity
        pdf.drawString(50, y_position, f"{item} x{quantity} - ${price:.2f}")
        y_position -= 20
    pdf.drawString(50, y_position, f"Subtotal: ${transaction['subtotal']:.2f}")
    pdf.drawString(50, y_position - 20, f"Tax ({TAX_RATE*100:.0f}%): ${transaction['tax']:.2f}")
    pdf.drawString(50, y_position - 40, f"Total: ${transaction['total']:.2f}")
    pdf.save()

    # Show receipt in message box
    messagebox.showinfo("Receipt", f"Receipt saved as {pdf_name}")

    # Clear the cart
    cart.clear()
    update_cart()

def view_sales_report():
    """Display sales report."""
    if not sales_report["transactions"]:
        messagebox.showinfo("Sales Report", "No transactions recorded.")
        return

    report = f"Sales Report\n"
    report += "="*40 + "\n"
    report += f"Total Sales: {sales_report['total_sales']}\n"
    report += f"Till Balance: ${sales_report['till_balance']:.2f}\n"
    report += "-"*40 + "\n"
    for transaction in sales_report["transactions"]:
        report += f"Date: {transaction['date']}\n"
        for item, quantity in transaction["items"].items():
            price = products[item] * quantity
            report += f"- {item:<15} x{quantity:<3} ${price:.2f}\n"
        report += f"Subtotal: ${transaction['subtotal']:.2f}\n"
        report += f"Tax: ${transaction['tax']:.2f}\n"
        report += f"Total: ${transaction['total']:.2f}\n"
        report += "-"*40 + "\n"

    messagebox.showinfo("Sales Report", report)

# Main POS Application
def main_app():
    global product_var, quantity_var, cart_list, subtotal_label, tax_label, total_label

    app = tk.Tk()
    app.title("POS System")
    app.geometry("700x800")
    app.resizable(False, False)
    app.configure(bg="#eaf2f8")

    # Styling
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 12), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#5dade2", foreground="white")
    style.map("Treeview.Heading", background=[("active", "#3498db")])

    # Product selection
    product_frame = tk.LabelFrame(app, text="Add Product to Cart", font=("Arial", 14, "bold"), bg="#d6eaf8")
    product_frame.pack(padx=10, pady=10, fill="x")

    product_var = tk.StringVar(value="")
    quantity_var = tk.StringVar(value="")

    tk.Label(product_frame, text="Product:", font=("Arial", 12), bg="#d6eaf8").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    product_menu = ttk.Combobox(product_frame, textvariable=product_var, values=list(products.keys()), state="readonly", font=("Arial", 12))
    product_menu.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(product_frame, text="Quantity:", font=("Arial", 12), bg="#d6eaf8").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    quantity_entry = ttk.Entry(product_frame, textvariable=quantity_var, font=("Arial", 12))
    quantity_entry.grid(row=1, column=1, padx=5, pady=5)

    add_button = ttk.Button(product_frame, text="Add to Cart", command=add_to_cart)
    add_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Cart view
    cart_frame = tk.LabelFrame(app, text="Cart", font=("Arial", 14, "bold"), bg="#f5b041")
    cart_frame.pack(padx=10, pady=10, fill="both", expand=True)

    cart_list = ttk.Treeview(cart_frame, columns=("Product", "Quantity", "Price"), show="headings", height=12)
    cart_list.heading("Product", text="Product")
    cart_list.heading("Quantity", text="Quantity")
    cart_list.heading("Price", text="Price")
    cart_list.pack(fill="both", expand=True, padx=10, pady=10)

    subtotal_label = tk.Label(cart_frame, text="Subtotal: $0.00", font=("Arial", 12), bg="#f5b041")
    subtotal_label.pack(anchor="w", padx=10)
    tax_label = tk.Label(cart_frame, text="Tax (7%): $0.00", font=("Arial", 12), bg="#f5b041")
    tax_label.pack(anchor="w", padx=10)
    total_label = tk.Label(cart_frame, text="Total: $0.00", font=("Arial", 12), bg="#f5b041")
    total_label.pack(anchor="w", padx=10)

    # Buttons
    button_frame = tk.Frame(app)  # Removed bg color for a seamless design
    button_frame.pack(pady=10)

    checkout_button = ttk.Button(button_frame, text="Checkout", command=checkout)
    checkout_button.grid(row=0, column=0, padx=10)

    report_button = ttk.Button(button_frame, text="Sales Report", command=view_sales_report)
    report_button.grid(row=0, column=1, padx=10)

    # Start the main application loop
    app.mainloop()

# Show the splash screen, then start the main application
show_splash_screen()
main_app()
