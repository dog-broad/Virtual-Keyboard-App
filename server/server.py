import os
import socket
import pyautogui
from datetime import datetime
import threading
import tkinter as tk
import pystray
from PIL import Image, ImageTk
from pystray import MenuItem as item
SERVER_HOST = '0.0.0.0'  # Listen on all available interfaces
SERVER_PORT = 12345

def handle_client(client_socket, client_address):
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

def start_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)  # Listen for up to 5 connections
    print(f"Server is running and listening on:")
    print(f"Host: {socket.gethostbyname(socket.gethostname())}")
    print(f"Port: {SERVER_PORT}")
    print("Waiting for incoming connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def stop_server(icon, item):
    global server_socket
    print("\nServer is stopping...")
    server_socket.close()
    print("Server stopped.")
    icon.stop()

def setup_system_tray():
    image = Image.open("server_icon.png")
    icon = pystray.Icon("server_icon", image, "Server App")

    # Create menu items
    menu = (item('Start Server', lambda: threading.Thread(target=start_server).start()),
            item('Stop Server', stop_server))

    # Set the menu
    icon.menu = pystray.Menu(*menu)

    # Run the system tray
    icon.run()

def main():
    setup_system_tray()

if __name__ == "__main__":
    main()
