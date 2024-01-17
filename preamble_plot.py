# -*- coding: utf-8 -*-
"""
Created on Jan 17 20:37:22 2022

@author: l00651623
"""

import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt

# Define preamble element sizes (in OFDM symbols)
legacy_preamble_size = 16
rl_sig_size = 2
u_sig_size = 2
eht_sig_min_size = 4  # Minimum size, can vary depending on features used

# Define fields within each element (corrected calculation order)
legacy_fields = {"L-STF": 8, "L-LTF": 8}  # Define L-STF and L-LTF first
legacy_fields["L-SIG"] = legacy_preamble_size - (legacy_fields["L-STF"] + legacy_fields["L-LTF"])  # Now calculate L-SIG using defined values
rl_sig_fields = {"DBPS": 1, "CBW": 1}
u_sig_fields = {"Bandwidth": 2, "TXOP": 6, "PPDU type": 4}
u_sig_fields ["Reserved"] = u_sig_size - u_sig_fields ["Bandwidth"] - u_sig_fields ["TXOP"] - u_sig_fields ["PPDU type"]
eht_sig_fields = {"MCS": 5, "Num_streams": 4, "MU info": 4}
eht_sig_fields[ "Preamble puncturing"] = eht_sig_min_size - eht_sig_fields["MCS"] - eht_sig_fields["Num_streams"] - eht_sig_fields["MU info"]

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 4))

# ... (rest of the code remains the same)


# Define rectangle coordinates and colors
rectangle_props = [
    {'x': 0, 'y': 0, 'width': legacy_preamble_size, 'height': 1, 'color': 'skyblue', 'label': 'Legacy Preamble'},
    {'x': legacy_preamble_size, 'y': 0, 'width': rl_sig_size, 'height': 1, 'color': 'lightgreen', 'label': 'RL-SIG'},
    {'x': legacy_preamble_size + rl_sig_size, 'y': 0, 'width': u_sig_size, 'height': 1, 'color': 'orange', 'label': 'U-SIG'},
    {'x': legacy_preamble_size + rl_sig_size + u_sig_size, 'y': 0, 'width': eht_sig_min_size, 'height': 1, 'color': 'magenta', 'label': 'EHT-SIG'},
]

# Add rectangles and field annotations to the axis
for props in rectangle_props:
    rectangle = patches.Rectangle(xy=(props['x'], props['y']), width=props['width'], height=props['height'], color=props['color'])
    ax.add_patch(rectangle)
    
    # Extract fields and their positions within the element
    field_positions = [(key, (prop['x'] + sum(prev_field_sizes) / 2, 0.5)) for key, prev_field_sizes in sorted(eval(props['label'] + "_fields").items(), key=lambda x: x[1])]
    
    # Annotate each field
    for field_name, position in field_positions:
        ax.annotate(field_name, position, ha='center', va='center', fontsize=8)

# Add labels and title
ax.set_xlabel('Time (OFDM symbols)')
ax.set_ylabel('Length')
ax.set_title('IEEE 802.11 EHT Preamble Structure with Field Names')

# Add legend
ax.legend()

# Adjust plot margins and grid
ax.margins(x=0)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()
