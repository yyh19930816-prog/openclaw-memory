# Source: https://github.com/israel-dryer/ttkbootstrap
# Date: 2023-11-20
# Description: A demo showing ttkbootstrap theming and widget styling

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def main():
    # Create window with 'superhero' theme (dark theme)
    root = ttk.Window(themename="superhero", title="TTK Bootstrap Demo")
    root.geometry("400x300")
    
    # Create a labeled frame to group widgets
    frame = ttk.Labelframe(
        root, 
        text="Widget Demo", 
        bootstyle=INFO,  # Sets frame color to info blue
        padding=20
    )
    frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
    
    # Create buttons with different styles
    ttk.Button(
        frame,
        text="Primary Button",
        bootstyle=(PRIMARY, OUTLINE),  # Primary color with outline
        command=lambda: print("Primary clicked!")
    ).pack(fill=X, pady=5)
    
    ttk.Button(
        frame,
        text="Danger Button",
 bootstyle=DANGER,  # Red danger button
        command=lambda: print("Danger clicked!")
    ).pack(fill=X, pady=5)
    
    # Add a round toggle button
    ttk.Checkbutton(
        frame,
        text="Round Toggle",
        bootstyle=(SUCCESS, ROUND, TOGGLE),  # Green round toggle
    ).pack(fill=X, pady=5)
    
    # Add themed entry widget
    entry = ttk.Entry(frame, bootstyle=SECONDARY)
    entry.pack(fill=X, pady=5)
    entry.insert(0, "Themed entry...")
    
    # Add a meter widget
    meter = ttk.Meter(
        frame,
        amounttotal=100,
        amountused=25,
        interactive=True,
        bootstyle=WARNING,
        subtext="Storage Used"
    )
    meter.pack(fill=X, pady=5)
    
    # Add a floodgauge
    flood = ttk.Floodgauge(
        frame,
        font="-size 10",
        value=50,
        bootstyle=(SUCCESS, STRIPED),
        mask="Progress: {}%"
    )
    flood.pack(fill=X, pady=5, padx=5)
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()