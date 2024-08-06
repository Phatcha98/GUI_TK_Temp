import os
import csv
import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime,timedelta
# from time import strftime
import sys
import tkinter.messagebox as messagebox
from matplotlib.figure import Figure
import traceback

output_data = r"D:\ui\smt_temp\output_smt_temp"


def handle_exception(exc_type, exc_value, exc_traceback):
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    # Do something with the error message, such as logging it or displaying it in a dialog box
    print(error_msg)

class App(tk.Frame):
    def __init__(self, master=None, product_name=""):
        super().__init__(master)
        self.pack() 
        self.master = master
        self.product_name = product_name 
        self.create_widgets()
        self.create_canvas()
        self.data = []
        self.last_update = None

    def report_callback_exception(self, exc, val, tb):
        traceback.print_exception(exc, val, tb)
   
    def create_canvas(self):
        self.fig = Figure(figsize=(19, 10), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

    def fetch_data(self, product_name, mot_line):
        csv_file = os.path.join(output_data,'output_smt_temp.csv')
        df = pd.read_csv(csv_file)
        df['time'] = pd.to_datetime(df['time'])

        last_week = datetime.now() - timedelta(days=7)
        filtered_df = df[(df['product'] == product_name) & (df['mot_Line'] == mot_line) & (df['time'] >= last_week)]
        return filtered_df


    def show_chart(self, product_name, mot_line):
        filtered_df = self.fetch_data(product_name, mot_line)
        time_col = filtered_df['time'].apply(lambda x: x.strftime('%d-%m-%Y %H:%M'))
        temp_df = filtered_df[['sampling1', 'sampling2', 'sampling3']]


        # Compute the mean temperature for the selected product
        mean_temp = 35
        mean_ucl = 30

        # Plot the data
        self.ax.clear()
        for col in temp_df.columns:
            self.ax.plot(time_col, temp_df[col], label=col)
            self.ax.scatter(time_col, temp_df[col], s=10)

        self.ax.set_xlabel('Time')
        self.ax.set_title(product_name)
        self.ax.set_ylabel('Temperature (°C)')
        self.ax.axhline(y=mean_temp, color='r', linestyle='-', label=f'USL ({mean_temp:.2f})')
        self.ax.axhline(y=mean_ucl, color='r', linestyle='--', label=f'UCL ({mean_ucl:.2f})')
        self.ax.legend()

        self.canvas.draw()

    def create_widgets(self):
        # Create the product label and entry widgets
        tk.Label(self, text="Product Name",font=('Tahoma',15)).grid(row=0, column=0)
        self.product_entry = tk.Entry(self,font=('Tahoma',15))
        self.product_entry.grid(row=0, column=1,padx=3, pady=3, ipadx=3, ipady=3)
        self.product_entry.focus_set()

        # Create the MOT line label and entry widgets
        tk.Label(self, text="MOT Line",font=('Tahoma',15)).grid(row=1, column=0)
        self.mot_entry = tk.Entry(self,font=('Tahoma',15))
        self.mot_entry.grid(row=1, column=1,padx=3, pady=3, ipadx=3, ipady=3)

        # Create the sampling 1 temperature label and entry widgets
        tk.Label(self, text="Sampling 1 Temp (°C)",font=('Tahoma',15)).grid(row=2, column=0)
        self.sampling1_temp_entry = tk.Entry(self,font=('Tahoma',15))
        self.sampling1_temp_entry.grid(row=2, column=1,padx=3, pady=3, ipadx=3, ipady=3)

        # Create the sampling 2 temperature label and entry widgets
        tk.Label(self, text="Sampling 2 Temp (°C)",font=('Tahoma',15)).grid(row=3, column=0)
        self.sampling2_temp_entry = tk.Entry(self,font=('Tahoma',15))
        self.sampling2_temp_entry.grid(row=3, column=1,padx=3, pady=3, ipadx=3, ipady=3)

        # Create the sampling 3 temperature label and entry widgets
        tk.Label(self, text="Sampling 3 Temp (°C)",font=('Tahoma',15)).grid(row=4, column=0)
        self.sampling3_temp_entry = tk.Entry(self,font=('Tahoma',15))
        self.sampling3_temp_entry.grid(row=4, column=1,padx=3, pady=3, ipadx=3, ipady=3)

        self.Label1 =tk.Label(self)
        self.Label1.grid(row=5)

        self.Label2 =tk.Label(self)
        self.Label2.grid(row=8)

    
        # Create the save button
        tk.Button(self, text="Save",bg="#00FF66",font=('Tahoma',15), command=self.save_data).grid(row=7, column=0,sticky='E')

        tk.Button(self, text="Reset",bg="#FF9900",font=('Tahoma',15), command=self.on_clear_button_click).grid(row=7, column=1)
        # Create the chart button
        tk.Button(self, text="Chart",bg="#00bcd4",font=('Tahoma',15), command=self.on_show_chart_button_click).grid(row=7, column=4)

    def get_current_time(self):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
        return current_time

    def save_data(self):
             # Get data from entries
        product = self.product_entry.get()
        mot_line = self.mot_entry.get()
        sampling1_temp = self.sampling1_temp_entry.get()
        sampling2_temp = self.sampling2_temp_entry.get()
        sampling3_temp = self.sampling3_temp_entry.get()
        # Get current time
        current_time = self.get_current_time()

        # Create a dictionary with the data
        data = {'time': current_time,
                'product': product,
                'mot_Line': mot_line,
                'sampling1': sampling1_temp,
                'sampling2': sampling2_temp,
                'sampling3': sampling3_temp}

        # Define the path to the CSV file
        csv_file = os.path.join(output_data,'output_smt_temp.csv')

        # Write the header row if the file doesn't exist
        if not os.path.exists(csv_file):
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                writer.writeheader()

        # Append the data to the CSV file
        with open(csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writerow(data)

        # self.product_entry.delete(0, tk.END)
        # self.mot_entry.delete(0, tk.END)
        self.sampling1_temp_entry.delete(0, tk.END)
        self.sampling2_temp_entry.delete(0, tk.END)
        self.sampling3_temp_entry.delete(0, tk.END)

    def on_show_chart_button_click(self):
        product_name = self.product_entry.get()
        mot_line = self.mot_entry.get()  
        if product_name and mot_line:  
            self.show_chart(product_name, mot_line)  
        else:
            messagebox.showerror("Error", "Please enter a product name and mot line.")

    def on_clear_button_click(self):
        # Clear the entry fields and time labels
        self.product_entry.delete(0, tk.END)
        self.mot_entry.delete(0, tk.END)
        self.sampling1_temp_entry.delete(0, tk.END)
        self.sampling2_temp_entry.delete(0, tk.END)
        self.sampling3_temp_entry.delete(0, tk.END)

    def destroy(self):
        if self.master is not None:
            for c in list(self.children.values()): 
                c.destroy()
                c.destroy(self)

window = App()
window.mainloop()


