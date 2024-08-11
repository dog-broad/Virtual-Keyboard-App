# 🖥️ Virtual Keyboard App

Welcome to the **Virtual Keyboard App**! This app lets you type on your PC using text written into your Android device. 🎉  
It's a fun way to send messages to your PC without touching the keyboard! 🚀

The app takes text input from the user and sends it to the PC over a **TCP network connection**. The PC then types the text in real time! 📬

## 📱 Key Features

- **Dynamic IP and Port**: Easily connect to your PC by entering the IP address and port. 🌐
- **Last Used Memory**: The app remembers the last IP address you used, so no need to enter it every time! 🧠
- **Text Speed Control**: Adjust how fast you want to send text with a handy SeekBar. ⚡
- **Progress Bar**: See the progress of your message being sent in real time! 📊

## 💻 Python Server

To use the Virtual Keyboard App, you’ll need to run a Python server on your PC. This server handles incoming messages from the app and types them out on your computer. 🖥️

### Server Features

- **TCP Listener**: Receives text messages from the app.
- **Typing Automation**: Types out the received text on your PC.
- **System Tray Icon**: Easily start and stop the server with a convenient tray icon.

## 🛠️ Getting Started

1. **Clone the Repository**:

   First, clone the repository to get the code.
   ```bash
   git clone https://github.com/dog-broad/VirtualKeyboardApp.git
   ```

   Alternatively, you can fork the repository and clone your fork.

2. **Set Up the Server**:

   - If you don't have Python installed, download and install it from the [official website](https://www.python.org/downloads/).

   Follow these steps to set up the Python server:

   - **Create a Virtual Environment**:
     ```bash
     cd VirtualKeyboardApp/server
     python -m venv venv
     venv\Scripts\activate  # For Windows
     source venv/bin/activate  # For macOS/Linux
     ```

   - **Install Dependencies**:
     ```bash
     pip install -r requirements.txt
     ```

   - **Run the Server**:
     ```bash
     python server.py
     ```

   - This will start the GUI server application. You can start and stop with the options provided. 🚀
   - Closing the GUI will minimize the server to the system tray.  
   
   
   *Note: To stop the server, right-click the system tray icon and select "Exit".*
   
3. **Install the App**:

   Open the project in Android Studio, build the app, and install it on your Android device.

4. **Connect and Type**:

   - Open the app on your Android device.
   - Enter your PC’s IP address and port number.
   - Type your message and hit "Send".

## 📜 How to Use

1. Launch the app on your Android device. 📱
2. Input your PC’s IP address and port number.
3. Compose your message in the text box.
4. Adjust the text speed if desired.
5. Tap the "Send Text" button and watch the magic unfold! 🪄

## 📝 Important Notes

- Ensure both your PC and Android device are on the same network for seamless operation.

## ⚠️ Known Issues

I’m aware that the UI could use some polish, and I’m actively working on improvements. 😅 If you have any suggestions or want to contribute, please reach out!

## 🎉 Contributing

Want to help out? Awesome! Feel free to open issues or submit pull requests. Let's make this app even better together! 🚀

## 📬 Contact

For questions, feedback, or suggestions, don’t hesitate to reach out! Social links are available in my profile. 🌟

---

Happy typing! 🎉🖥️✌️