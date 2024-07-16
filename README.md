# 🖥️ Virtual Keyboard App

Welcome to the **Virtual Keyboard App**! This app lets you type on your PC using text written into your Android device. 🎉  
It's a fun way to send messages to your PC without touching the keyboard! 🚀

The app takes text input from the user and sends it to the PC over a **TCP network connection**. The PC then types the text in real time! 📬

## 📱 Features

- **Dynamic IP and Port**: Easily connect to your PC by entering the IP address and port. 🌐
- **Last Used Memory**: The app remembers the last IP address you used, so no need to enter it every time! 🧠
- **Text Speed Control**: Adjust how fast you want to send text with a handy SeekBar. ⚡
- **Progress Bar**: See the progress of your message being sent in real time! 📊

## 💻 Python Server

You’ll need a Python server running on your PC to receive the messages from the app. A simple server code is provided in the `server` directory. 🐍

- It will listen for incoming TCP messages from the app.
- It is responsible for receiving the text and typing it on the PC.
- A Tray Icon is also provided to easily start and stop the server. Access it by right-clicking the icon in the system tray.

## 🛠️ Getting Started

1. **Clone the Repo**:

   Get the code by cloning this repository.
   ```bash
   git clone https://github.com/dog-broad/VirtualKeyboardApp.git
   ```

   Or make a fork and clone instead.

2. **Set Up the Server**:

   Run the Python server code on your PC. Make sure to set the correct port! ⚙️
   > The default port is `12345`.

    - Create a virtual environment and install the required packages.
       ```bash
       cd server
       python -m venv venv
       venv\Scripts\activate
       pip install -r requirements.txt
       ```

    - Run the server in the background.
       ```bash
       cd server
       python server.py
       ```

    - Start the server.
        - Access the System tray icon and click the "Start Server" button.

3. **Install the App**:

   Open the project in Android Studio and build the app on your Android device.

4. **Connect and Type**:

   Enter your PC's IP address and port in the app, type your message, and hit "Send"!

## 📜 Usage

1. Open the app on your Android device. 📱
2. Enter the IP address and port number of your PC.
3. Type your message in the text box.
4. Adjust the text speed if needed.
5. Click the "Send Text" button and watch the magic happen! 🪄

## 📝 Note

Make sure your PC and Android device are on the same network for a smooth connection.

## ⚠️ Known Issues

I know the UI isn't super intuitive right now, but I'm working on it! 😅 If you have suggestions or want to help improve it, please reach out!

## 🎉 Contributing

Want to help out? Awesome! Feel free to open issues or submit pull requests. Let's make this app even better together! 🚀

## 📬 Contact

If you have questions or suggestions, feel free to reach out! Social links are in my profile. 🌟

---

Happy typing! 🎉🖥️✌️
