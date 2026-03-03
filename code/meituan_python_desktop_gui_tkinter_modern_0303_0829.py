#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ttkbootstrap demo application
Source: https://github.com/israel-dryer/ttkbootstrap
Created: 2023-11-15
Description: A simple demo showing ttkbootstrap's modern themed widgets
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_demo_app():
    """Create and configure the main application window"""
    # Create window with superhero theme (dark)
    root = ttk.Window(
        title="TTK Bootstrap Demo",
        themename="superhero",
        size=(400, 300),
        resizable=(True, True)
    )
    
    # Configure grid layout (3 rows, 3 columns)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    
    # Add themed widgets
    add_widgets(root)
    
    return root

def add_widgets(window):
    """Add demo widgets to the window"""
    
    # Primary button (success style)
    btn1 = ttk.Button(
        window,
        text="Primary",
        bootstyle=PRIMARY,
        command=lambda: print("Primary clicked")
    )
    btn1.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
    
    # Success button
    btn2 = ttk.Button(
        window,
        text="Success",
        bootstyle=SUCCESS,
        command=lambda: print("Success clicked")
    )
    btn2.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)
    
    # Danger outline button
    btn3 = ttk.Button(
        window,
        text="Danger",
        bootstyle=(OUTLINE, DANGER),
        command=lambda: print("Danger clicked")
    )
    btn3.grid(row=0, column=2, padx=5, pady=5, sticky=NSEW)
    
    # Round toggle button
    btn4 = ttk.Button(
        window,
        text="Toggle",
        bootstyle=(TOGGLE, ROUND),
        command=lambda: print("Toggle clicked")
    )
    btn4.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
    
    # Meter widget
    meter = ttk.Meter(
        window,
        metersize=100,
        amountused=25,
        interactive=True,
        bootstyle=INFO,
        textright="%"
    )
    meter.grid(row=1, column=1, padx=5, pady=5)
    
    # Floodgauge widget
    gauge = ttk.Floodgauge(
        window,
        font=("-size", 10),
        value=50,
        bootstyle=WARNING,
        mask="Progress {}%"
    )
    gauge.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=EW)
    
    # Start gauge animation
    gauge.start()

if __name__ == "__main__":
    app = create_demo_app()
    app.mainloop()