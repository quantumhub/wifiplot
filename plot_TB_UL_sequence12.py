# -*- coding: utf-8 -*-
"""
Created on Jan 17 19:14:59 2022

@author: free Wi-Fi
"""

import matplotlib.pyplot as plt
import numpy as np

# Define frame data with realistic durations
frame_data = [
    {"type": "Trigger Frame", "timestamp": 0, "node": "AP", "color": "blue", "duration": 0.005},
    {"type": "Data Frame", "timestamp": 0.015, "node": "STA1", "color": "green", "duration": 0.01},
    {"type": "Data Frame", "timestamp": 0.015, "node": "STA2", "color": "green", "duration": 0.01},
    {"type": "Block ACK Frame", "timestamp": 0.035, "node": "AP", "color": "red", "duration": 0.005},
]

# Define frame data for sounding sequence

frame_data = [
    {"type": "NDP Announcement (NDPA)", "timestamp": 0, "node": "AP", "color": "blue", "duration": 0.001},
    {"type": "Null Data Packet (NDP)", "timestamp": 0.0015, "node": "AP", "color": "orange", "duration": 0.002},
    {"type": "Compressed Beamforming (C-BFR)", "timestamp": 0.0035, "node": "STA1", "color": "purple", "duration": 0.001},  # Changed timestamp
    {"type": "Beamforming Report Poll (BRP)", "timestamp": 0.0045, "node": "AP", "color": "red", "duration": 0.001},  # Changed timestamp
    {"type": "Compressed Beamforming (C-BFR)", "timestamp": 0.0055, "node": "STA2", "color": "purple", "duration": 0.001},  # Changed timestamp
]

# Set SIFS value
SIFS = 0.0016  # Adjust as needed

def plot_frame_exchange_sequence(frame_data, sifs):
    """Plots a frame exchange sequence with visual enhancements.

    Args:
        frame_data (list): A list of dictionaries, each representing a frame with
            the following keys:
                - type (str): The type of the frame.
                - timestamp (float): The initial timestamp of the frame.
                - node (str): The node transmitting the frame.
                - color (str, optional): The color for plotting the frame.
                - duration (float): The duration of the frame.
        sifs (float): The SIFS value.
    """

    # Adjust timestamps, ensuring simultaneous Data Frames
    last_end_time = frame_data[0]["timestamp"] + frame_data[0]["duration"]  # Start after Trigger Frame
    for i in range(1, len(frame_data)):
        if frame_data[i]["type"] == "Data Frame":
            frame_data[i]["timestamp"] = last_end_time + SIFS  # Start Data Frames together
        else:
            frame_data[i]["timestamp"] = max(
                frame["timestamp"] + frame["duration"] + SIFS for frame in frame_data[:i]
            )  # Other frames follow SIFS spacing
            last_end_time = frame_data[i]["timestamp"] + frame_data[i]["duration"]  # Update last end time
    
        
    # Determine node transmission order
    node_transmission_order = sorted(
        set([frame["node"] for frame in frame_data]),
        key=lambda node: min(frame["timestamp"] for frame in frame_data if frame["node"] == node),
    )
    
    # Create figure and axes with a larger size
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Define variable for frame height
    frame_height = 0.8
    
    # Plot each frame with visual enhancements and bottom alignment
    for frame in frame_data:
        x = frame["timestamp"]
        y = node_transmission_order.index(frame["node"]) + 1
        ax.add_patch(
            plt.Rectangle(
                (x, y - frame_height / 2),
                frame["duration"],
                frame_height,
                color=frame["color"],
                label=frame["type"],
                alpha=0.8,
            )
        )
        ax.text(
            x + frame["duration"] / 2,
            y,
            frame["type"],
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
        )
    
    head_length=0.0002
    timeline_length = max(frame["timestamp"] + frame["duration"] for frame in frame_data)
    # Add time axes with arrows at the bottom of each frame
    for i, node in enumerate(node_transmission_order):
        node_y = i + 1
        ax.arrow(
            0,
            node_y - frame_height / 2,
            timeline_length+head_length,
            0,
            head_width=0.05,
            head_length=head_length,
            fc="gray",
            ec="gray",
            linewidth=0.5,
        )
    
    # Adjust y-axis limits and ticks based on transmission order
    ax.set_ylim(0, len(node_transmission_order)+frame_height)
    ax.set_yticks(range(1, len(node_transmission_order) + 1))
    ax.set_yticklabels(node_transmission_order)
    
    # Add x-axis limits to show the entire sequence
    ax.set_xlim(0, timeline_length + head_length*2)  # Expand slightly for visibility
    
    # Add labels and title
    ax.set_ylabel("Node (Transmission Order)")
    ax.set_xlabel("Time (seconds)")
    ax.set_title("Wi-Fi ACK Frame Exchange Sequence (Enhanced Visualization)")
    
    # Add grid lines
    #ax.grid(color="gray", linestyle="--", linewidth=0.5)
    
    # Display the plot
    plt.show()

plot_frame_exchange_sequence(frame_data, SIFS)