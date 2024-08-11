import os
import ctypes
import socket
import pyautogui
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import pystray
from pystray import MenuItem as item
from win11toast import notify

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345

# Fix windows taskbar icon not showing
myappid = 'dog-broad.server-app.1.0.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server App")
        self.root.geometry("400x300")  # Adjusted window size
        self.root.resizable(False, False)  # Lock window size

        # Get the directory of the script
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        # Set the icon of the window
        self.root.iconbitmap(os.path.join(self.script_dir, 'server.ico'))

        # Set up customtkinter
        ctk.set_appearance_mode("dark")  # or "light"
        ctk.set_default_color_theme("blue")  # you can choose different themes

        self.server_socket = None
        self.is_running = False
        self.stop_event = threading.Event()

        # Emoji icons
        self.start_icon = "▶"
        self.stop_icon = "■"

        # Start Server Button
        self.start_button = ctk.CTkButton(
            root, text=f"{self.start_icon} Start Server", font=("Arial", 14),
            command=self.start_server
        )
        self.start_button.pack(pady=10)

        # Stop Server Button
        self.stop_button = ctk.CTkButton(
            root, text=f"{self.stop_icon} Stop Server", font=("Arial", 14),
            command=self.stop_server, state=tk.DISABLED
        )
        self.stop_button.pack(pady=10)

        # Status Label
        self.status_label = ctk.CTkLabel(root, text="Server is not running", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # IP Address and Port Label (initially hidden)
        self.info_label = ctk.CTkLabel(root, text="", font=("Arial", 12))
        self.info_label.pack(pady=10)
        self.info_label.configure(text=f"IP: {SERVER_HOST}\nPort: {SERVER_PORT}", text_color="gray")

        # Toggle Button for IP Address and Port
        self.toggle_button = ctk.CTkButton(
            root, text="Show Info", command=self.toggle_info
        )
        self.toggle_button.pack(pady=10)

        # Exit Application Button
        self.exit_button = ctk.CTkButton(
            root, text="Exit Application", font=("Arial", 14),
            command=self.exit_app
        )
        self.exit_button.pack(pady=10)

        # Tray Icon
        self.tray_icon = None

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.info_visible = False  # Track visibility state

    def handle_client(self, client_socket, client_address):
        with client_socket:
            print(f"Connected by {client_address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                received_text = data.decode('utf-8')
                print(f"Received: {received_text}")

                # Simulate typing into another application
                pyautogui.typewrite(received_text)
        print(f"Connection closed by {client_address}")

    def start_server(self):
        if self.is_running:
            messagebox.showinfo("Info", "Server is already running.")
            return

        self.is_running = True
        self.stop_event.clear()
        self.status_label.configure(text="Server is running...")
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((SERVER_HOST, SERVER_PORT))
        self.server_socket.listen(5)
        print(f"Server is running and listening on {socket.gethostbyname(socket.gethostname())}:{SERVER_PORT}")

        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.start()

    def accept_connections(self):
        while self.is_running and not self.stop_event.is_set():
            try:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
            except socket.error:
                # Handle socket errors (e.g., if the socket is closed)
                if self.stop_event.is_set():
                    break
                else:
                    print("Socket error occurred")

    def stop_server(self):
        if not self.is_running:
            messagebox.showinfo("Info", "Server is not running.")
            return

        self.is_running = False
        self.stop_event.set()
        self.status_label.configure(text="Server is not running")
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)

        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

        # Wait for the server thread to finish
        if hasattr(self, 'server_thread'):
            self.server_thread.join()

        print("Server stopped.")

    def hide_window(self):
        # Send a notification when minimizing to tray
        notify('Server App', 'Application minimized to system tray.')  # Show toast notification
        self.root.withdraw()  # Hide the main window
        self.show_tray_icon()

    def show_tray_icon(self):
        # Load the icon
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        image = Image.open(os.path.join(self.script_dir, 'server.ico'))
        self.tray_icon = pystray.Icon("server_app", image, "Server App")
        self.tray_icon.menu = pystray.Menu(
            item('Restore', self.restore_window),
            item('Exit', self.exit_app)
        )
        self.tray_icon.run()

    def restore_window(self, icon, item):
        self.root.deiconify()  # Show the main window
        self.tray_icon.stop()  # Stop the tray icon

    def exit_app(self, icon=None, item=None):
        # Stop server if it's running
        if self.is_running:
            self.stop_server()
        # Destroy the application
        if self.root is not None:
            self.root.quit()  # Stop the main loop
            self.root.destroy()  # Destroy the root window
        # Stop the tray icon
        if self.tray_icon is not None:
            self.tray_icon.stop()

    def toggle_info(self):
        if self.info_visible:
            self.info_label.configure(text=f"IP: {SERVER_HOST}\nPort: {SERVER_PORT}", text_color="gray")  # Hide or blur the text
            self.toggle_button.configure(text="Show Info")
        else:
            self.info_label.configure(text=f"IP: {socket.gethostbyname(socket.gethostname())}\nPort: {SERVER_PORT}", text_color="white")  # Show the text
            self.toggle_button.configure(text="Hide Info")
        self.info_visible = not self.info_visible

def main():
    root = ctk.CTk()  # Use customtkinter's CTk instead of Tk
    app = ServerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
