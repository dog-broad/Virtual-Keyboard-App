package com.dog_broad.virtualkeyboardapp;

import android.annotation.SuppressLint;
import androidx.appcompat.app.AppCompatActivity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ProgressBar;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    private EditText editText, ipAddress, port;
    private SeekBar textSpeed;
    private TextView textSpeedValue, textProgress;
    private ProgressBar progressBar;

    private static final String PREFS_NAME = "VirtualKeyboardPrefs";
    private static final String LAST_IP_KEY = "last_ip";
    private static final String LAST_PORT_KEY = "last_port";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editText = findViewById(R.id.editText);
        ipAddress = findViewById(R.id.ipAddress);
        port = findViewById(R.id.port);
        textSpeed = findViewById(R.id.textSpeed);
        textSpeedValue = findViewById(R.id.textSpeedValue);
        textProgress = findViewById(R.id.textProgress);
        progressBar = findViewById(R.id.progressBar);
        Button btnSend = findViewById(R.id.btnSend);

        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        ipAddress.setText(prefs.getString(LAST_IP_KEY, ""));
        port.setText(prefs.getString(LAST_PORT_KEY, "12345"));

        textSpeed.setProgress(50);
        textSpeed.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                textSpeedValue.setText("Text Speed: " + progress + " letters/sec");
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
        });

        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = editText.getText().toString();
                String ip = ipAddress.getText().toString();
                int portNum = Integer.parseInt(port.getText().toString());
                int speed = textSpeed.getProgress();

                if (ip.isEmpty()) {
                    Toast.makeText(MainActivity.this, "IP Address cannot be empty", Toast.LENGTH_SHORT).show();
                    return; // Exit the method if IP Address is empty
                }

                savePreferences(ip, portNum);
                sendText(message, ip, portNum, speed);
                Toast.makeText(MainActivity.this, "Text Sent", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void savePreferences(String ip, int port) {
        SharedPreferences.Editor editor = getSharedPreferences(PREFS_NAME, MODE_PRIVATE).edit();
        editor.putString(LAST_IP_KEY, ip);
        editor.putString(LAST_PORT_KEY, String.valueOf(port));
        editor.apply();
    }

    private void sendText(String text, String ip, int port, int speed) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        editText.setEnabled(false);
                        textProgress.setText("");
                        progressBar.setVisibility(View.VISIBLE);
                        progressBar.setMax(text.length());
                        progressBar.setProgress(0);
                    }
                });

                try {
                    Socket socket = new Socket(ip, port);
                    DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
                    for (int i = 0; i < text.length(); i++) {
                        char c = text.charAt(i);
                        dos.writeChar(c);
                        dos.flush();
                        final int progress = i + 1;
                        final String highlightedText = text.substring(0, progress) +
                                "<font color='#FF0000'>" +
                                text.substring(progress) +
                                "</font>";
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                textProgress.setText(android.text.Html.fromHtml(highlightedText));
                                progressBar.setProgress(progress);
                            }
                        });
                        Thread.sleep(1000 / speed);
                    }
                    dos.close();
                    socket.close();
                } catch (IOException | InterruptedException e) {
                    System.out.println("Error: " + e.getMessage());
                } finally {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            editText.setEnabled(true);
                            progressBar.setVisibility(View.GONE);
                        }
                    });
                }
            }
        }).start();
    }
}
