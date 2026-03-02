#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source: https://github.com/israel-dryer/ttkbootstrap
Created on: 2023-11-20
Description: A simple demo of ttkbootstrap showing basic widgets with superhero theme
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def main():
    """Create and run a ttkbootstrap themed application"""
    
    # Create window with superhero theme (dark theme)
    root = ttk.Window(
        title="TTK Bootstrap Demo",
        themename="superhero",
        size=(400, 300),
        resizable=(True, True)
    )
    
    # Create a label widget
    lbl = ttk.Label(
        master=root,
        text="TTK Bootstrap Example",
        font=('Helvetica', 16),
        bootstyle=PRIMARY  # Use primary color
    )
    lbl.pack(pady=10)
    
    # Create a button with primary style
    btn_primary = ttk.Button(
        master=root,
        text="Primary Button",
        bootstyle=(PRIMARY, OUTLINE),  # Outline style
        command=lambda: print("Primary clicked!")
    )
    btn_primary.pack(pady=5, padx=10, fill=X)
    
    # Create a button with success style
    btn_success = ttk.Button(
        master=root,
        text="Success Button",
        bootstyle=SUCCESS,
        command=lambda: print("Success clicked!")
    )
    btn_success.pack(pady=5, padx=10, fill=X)
    
    # Create a danger button with round toggle style
    btn_danger = ttk.Button(
        master=root,
        text="Danger Button",
        bootstyle=(DANGER, TOGGLE),  # Toggle button style
        command=lambda: print("Danger clicked!")
    )
    btn_danger.pack(pady=5, padx=10, fill=X)
    
    # Create a progressbar
    progress = ttk.Progressbar(
        master=root,
        bootstyle=(SUCCESS, STRIPED),
        maximum=100,
        value=50
    )
    progress.pack(pady=10, padx=10, fill=X)
    
    # Create checkbox
    checkbox = ttk.Checkbutton(
        master=root,
        text="Check this box",
        bootstyle=INFO,
        variable=ttk.BooleanVar(value=True)
    )
    checkbox.pack(pady=5, padx=10)
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()