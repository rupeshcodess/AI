import tkinter as tk

# Function to calculate and display the associative law results
def check_associative_law():
    try:
        # Get the user input and convert it to integers
        a = int(entry_a.get())
        b = int(entry_b.get())
        c = int(entry_c.get())

        # Associative law for addition
        add_result1 = (a + b) + c
        add_result2 = a + (b + c)

        # Associative law for multiplication
        mul_result1 = (a * b) * c
        mul_result2 = a * (b * c)

        # Update the result labels with the calculated results
        result_label.config(text=f"Addition: (a + b) + c = {add_result1}\n"
                                 f"Addition: a + (b + c) = {add_result2}\n\n"
                                 f"Multiplication: (a * b) * c = {mul_result1}\n"
                                 f"Multiplication: a * (b * c) = {mul_result2}")

    except ValueError:
        result_label.config(text="Please enter valid integers for a, b, and c")

# Creating the main window
root = tk.Tk()
root.title("Associative Law Checker")

# Labels and entry fields for user input
label_a = tk.Label(root, text="Enter value for a:")
label_a.pack()

entry_a = tk.Entry(root)
entry_a.pack()

label_b = tk.Label(root, text="Enter value for b:")
label_b.pack()

entry_b = tk.Entry(root)
entry_b.pack()

label_c = tk.Label(root, text="Enter value for c:")
label_c.pack()

entry_c = tk.Entry(root)
entry_c.pack()

# Button to calculate the results
button = tk.Button(root, text="Check Associative Law", command=check_associative_law)
button.pack()

# Label to display the results
result_label = tk.Label(root, text="", justify=tk.LEFT, anchor="w")
result_label.pack()

# Start the GUI event loop
root.mainloop()
