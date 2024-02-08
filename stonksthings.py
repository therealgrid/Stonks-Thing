import os
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import plotly.express as px

def display_all_csv_graph():
    folder_path = "(YOUR DIRECTORY HERE)"
    all_files = os.listdir(folder_path)
    combined_df = pd.DataFrame()

    for file_name in all_files:
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            try:
                df = pd.read_csv(file_path)
                if 'High' in df.columns:
                    df['Company'] = file_name.split('.')[0]  # Add a column with company name
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while reading file {file_name}: {e}")

    if combined_df.empty:
        messagebox.showerror("Error", "No valid data found in the CSV files.")
        return

    fig = px.line(combined_df, x=combined_df.columns[0], y='High', color='Company',
                  title="Stock Value Comparison", labels={combined_df.columns[0]: "Date", "High": "High Value"})
    fig.update_layout(xaxis_title=combined_df.columns[0], yaxis_title='High Value')
    fig.show()
    
def display_csv_graph(file_name):
    file_path = "(YOUR DIRECTORY HERE)" + file_name + ".csv"

    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"File {file_name}.csv not found.")
        return

    try:
        df = pd.read_csv(file_path)
        # Check if the csv has at least two columns, as you need two axis for plotting data
        if len(df.columns) < 2:
            messagebox.showerror("Error", "CSV file must contain at least two columns for plotting.")
            return
        # Check if the columns contain numbers, needed to plot on the graph
        numeric_columns = df.select_dtypes(include='number').columns
        if len(numeric_columns) < 2:
            messagebox.showerror("Error", "CSV file must contain numeric data for plotting.")
            return
        # Display graph with highest value per stock share for each month as y-axis & timeline as the x-axis
        fig = px.line(df, x=df.columns[0], y='High')
        fig.update_layout(title=f"{file_name} - Stock Value", xaxis_title=df.columns[0], yaxis_title='High')
        fig.show()
#Error catching, if none of these are met, this is what is shown (e being which error occured)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def display_csv_graph_clicked():
    file_name = file_var.get()
    display_csv_graph(file_name)

def display_csv_table(file_name):
    file_path = "(YOUR DIRECTORY HERE)" + file_name + ".csv"

    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"File {file_name}.csv not found.")
        return

    try:
        # Read CSV file
        df = pd.read_csv(file_path)

        # Create new window
        table_window = tk.Toplevel(root)
        table_window.title(f"{file_name} - Stock Market Data")
        table_window.configure(bg="black")  # Set background color

        # Create treeview widget
        tree = ttk.Treeview(table_window, style="Custom.Treeview")
        style = ttk.Style()
        style.configure("Custom.Treeview", background="black", foreground="green", font=("Arial", 12), fieldbackground="black", borderwidth=0)  # Set text color, font size, and remove border

        # Define columns
        tree["columns"] = tuple(df.columns)

        # Format column headers
        for column in df.columns:
            tree.heading(column, text=column)
            tree.column(column, width=100)

        # Insert data
        for index, row in df.iterrows():
            tree.insert("", tk.END, values=tuple(row))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def display_csv_table_clicked():
    file_name = file_var.get()
    display_csv_table(file_name)

def clean_csv_file(file_name):
    file_path = "(YOUR DIRECTORY HERE)" + file_name + ".csv"

    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"File {file_name}.csv not found.")
        return

    try:
        # Read CSV file
        df = pd.read_csv(file_path)

        # Clean data
        df.dropna(inplace=True)  # Drop rows with missing values

        # Overwrite the original file with cleaned data
        df.to_csv(file_path, index=False)

        messagebox.showinfo("Success", f"Data cleaned successfully. Original file updated.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

def clean_selected_csv():
    file_name = file_var.get()
    clean_csv_file(file_name)

# Create main window
root = tk.Tk()
root.title("Stock Market Data")

# Set window size and position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Set window background color
root.configure(bg="black")

# List of CSV file names
file_names = ["AAPL", "AMZN", "BP", "META", "NFLX"]

# Create dropdown menu for selecting CSV file
file_label = tk.Label(root, text="Select Company:", bg="black", fg="green", font=("Wingdings", 16))  # Set text color and font size
file_label.pack(pady=10)

file_var = tk.StringVar(root)
file_menu = ttk.Combobox(root, textvariable=file_var, values=file_names, style="Custom.TCombobox", font=("Arial", 14))  # Set button style and font size
file_menu.pack(pady=10)

# Create a Frame widget as a container for buttons
button_frame = tk.Frame(root, bg="black")
button_frame.pack(pady=10)

# Create buttons inside the Frame widget
btn_clean_csv = tk.Button(button_frame, text="Clean Data", command=clean_selected_csv, bg="white", fg="green", relief="solid", borderwidth=2, padx=20, pady=10, font=("Arial", 14), highlightbackground="white", highlightcolor="white")  # Set button style, font size, and border with white color
btn_clean_csv.pack(side="top", pady=(0, 10))

btn_display_table = tk.Button(button_frame, text="Display Stock Value Table", command=display_csv_table_clicked, bg="white", fg="green", relief="solid", borderwidth=2, padx=20, pady=10, font=("Arial", 14), highlightbackground="white", highlightcolor="white")  # Set button style, font size, and border with white color
btn_display_table.pack(side="top", pady=(0, 10))

btn_display_graph = tk.Button(button_frame, text="Display Graph", command=display_csv_graph_clicked, bg="white", fg="green", relief="solid", borderwidth=2, padx=20, pady=10, font=("Arial", 14), highlightbackground="white", highlightcolor="white")
btn_display_graph.pack(side="top", pady=(0, 10))

btn_display_all_graph = tk.Button(button_frame, text="Display All Companies Graph", command=display_all_csv_graph, bg="white", fg="green", relief="solid", borderwidth=2, padx=20, pady=10, font=("Arial", 14), highlightbackground="white", highlightcolor="white")
btn_display_all_graph.pack(side="top", pady=(0, 10))

# Run main loop
root.mainloop()




