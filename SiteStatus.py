from bs4 import BeautifulSoup
import requests
import tkinter as tk
from datetime import datetime
import time

# Define the URL
url = "http://status.banno.com"

# Create a Tkinter window
window = tk.Tk()
window.title("Banno Status History")

# Add a label for the URL
url_label = tk.Label(window, text="URL: " + url, font=("Arial", 14))
url_label.pack()

# Add a canvas for the indicator light
indicator_light = tk.Canvas(window, width=40, height=40)
indicator_light.pack()

# Add a label for the indicator light
indicator_label = tk.Label(window, text="Indicator: Yellow = change in last 6 hours, Red = change in last 24 hours", font=("Arial", 10))
indicator_label.pack()

# Add a text widget for the latest status
latest_status_widget = tk.Text(window, wrap='word', height=5)  # Adjust the height as needed
latest_status_widget.pack()

# Add a label for the status history
history_label = tk.Label(window, text="Status Change History:", font=("Arial", 14))
history_label.pack()

# Add a text widget for the status history
history_widget = tk.Text(window, wrap='word')
history_widget.pack()

# Initialize the status history
status_history = []

def check_status():
    # Use requests to fetch the content
    response = requests.get(url)

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the text content and strip extra white space
    text_content = ' '.join(soup.stripped_strings)

    # Exclude specific text
    text_content = text_content.replace("800-299-4222 | For Clients Portal", "")
    text_content = text_content.replace("Banno Status Banno Platform Status", "")

    # Update the latest status widget
    latest_status_widget.delete('1.0', 'end')
    latest_status_widget.insert('1.0', text_content)

    # Change the color of the top section based on the status
    if "All services are operational" in text_content:
        latest_status_widget.config(bg='green')
    else:
        latest_status_widget.config(bg='red')

    # Check if the status has changed
    if not status_history or status_history[-1][1] != text_content:
        # Add the status to the history
        timestamp = datetime.now()
        status_history.append((timestamp, text_content))

        # Show a popup window
        popup = tk.Toplevel(window)
        popup.title("Status Change")
        message = f"Status changed at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {text_content}"
        tk.Label(popup, text=message).pack()
        tk.Button(popup, text="OK", command=popup.destroy).pack()

    # Keep only the last 10 status changes
    status_history[:] = status_history[-10:]

    # Update the status history widget
    history_widget.delete('1.0', 'end')
    for timestamp, status in status_history:
        history_widget.insert('end', f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {status}\n")

    # Update the indicator light based on the time of the last status change
    if status_history:
        last_change_time = status_history[-1][0]
        time_since_last_change = datetime.now() - last_change_time
        if time_since_last_change.total_seconds() < 6 * 60 * 60:
            indicator_light.config(bg='yellow')
        elif time_since_last_change.total_seconds() < 24 * 60 * 60:
            indicator_light.config(bg='red')
        else:
            indicator_light.config(bg='green')

    # Check the status again in 5 minutes
    window.after(300000, check_status)

# Start checking the status
check_status()

# Run the Tkinter event loop
window.mainloop()

