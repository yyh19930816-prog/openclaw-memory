"""
ttkbootstrap Demo Application
Source: https://github.com/israel-dryer/ttkbootstrap
Created: 2023-11-20
Description: A simple demo showing ttkbootstrap's modern themed widgets
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def main():
    # Create window with superhero theme
    root = ttk.Window(
        title="TTKBootstrap Demo",
        themename="superhero",
        size=(500, 300),
        resizable=(True, True)
    )
    
    # Configure grid layout
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    
    # Create styled widgets
    label = ttk.Label(
        root,
        text="TTKBootstrap Demo",
        font=("Helvetica", 16),
        bootstyle=PRIMARY
    )
    label.grid(row=0, column=0, columnspan=2, pady=10)
    
    # Primary button with outline style
    button1 = ttk.Button(
        root,
        text="Primary",
        bootstyle=(OUTLINE, PRIMARY),
        command=lambda: print("Primary clicked!")
    )
    button1.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
    
    # Danger button with solid style
    button2 = ttk.Button(
        root,
        text="Danger",
        bootstyle=DANGER,
        command=lambda: print("Danger clicked!")
    )
    button2.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)
    
    # Success toggle button
    toggle = ttk.Checkbutton(
        root,
        text="Toggle",
        bootstyle=(SUCCESS, TOGGLE),
        variable=ttk.BooleanVar(value=True)
    )
    toggle.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)
    
    # Meter widget showing progress
    meter = ttk.Meter(
        root,
        metersize=150,
        padding=5,
        amountused=25,
        metertype="full",
        subtext="Progress",
        bootstyle=INFO,
        interactive=True
    )
    meter.grid(row=2, column=1, padx=5, pady=5)
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()