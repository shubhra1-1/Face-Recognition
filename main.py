import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import util
import os 
import datetime
import subprocess


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1000x500+200+100")
        self.main_window.title("Face Recognition App")

        # Set log path and database directory in __init__
        self.db_dir = './db'
        self.log_path = './log.txt'

        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        # Create log file if it doesn't exist
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close()


        # Main window buttons
        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=250)

        self.register_new_user_button_main_window = util.get_button(
            self.main_window, 'Register New User', 'gray', self.register_new_user, fg='black'
        )
        self.register_new_user_button_main_window.place(x=750, y=350)

        # Webcam label for main window
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
        else:
            self.update_main_webcam()

    def login(self):
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]).decode('utf-8')
        name = output.split(",")[1].strip().split()[0]  # Extracts only the name, removing extra parts

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box("Ups...", "Unknown user. Please register new user or try again.")
        else:
            util.msg_box("Welcome back!", f"Welcome, {name}.")  # Display only the name
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close()


        os.remove(unknown_img_path)

    def update_main_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self.most_recent_capture_arr = frame

            # Update main window webcam label
            self.webcam_label.imgtk = imgtk
            self.webcam_label.configure(image=imgtk)

        # Schedule next update
        self.main_window.after(10, self.update_main_webcam)

    def register_new_user(self):
        # Create a new window for registration
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1000x500+200+100")  # Same size & position
        self.register_new_user_window.title("Register New User")
        self.register_new_user_window.grab_set()  # Block interaction with main window

        # Label for captured image
        self.capture_label = tk.Label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        # Display the most recent captured image
        self.add_img_to_label(self.capture_label)

        # Label for username input
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, input username:')
        self.text_label_register_new_user.place(x=750, y=70)

        # Entry field for username input
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        # Accept button (Green)
        accept_button = tk.Button(
            self.register_new_user_window, text="Accept", bg="green", fg="white",
            font=("Helvetica", 14, "bold"), width=15, height=2, command=self.accept_register_new_user
        )
        accept_button.place(x=750, y=250, width=200, height=50)

        # Try Again button (Red)
        try_again_button = tk.Button(
            self.register_new_user_window, text="Try Again", bg="red", fg="white",
            font=("Helvetica", 14, "bold"), width=15, height=2, command=self.try_again_register_new_user
        )
        try_again_button.place(x=750, y=350, width=200, height=50)

    def add_img_to_label(self, label):
        """ Updates the given label with the most recent captured image """
        if hasattr(self, 'most_recent_capture_pil'):
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            label.imgtk = imgtk
            label.configure(image=imgtk)
        
        self.register_new_user_capture = self.most_recent_capture_arr.copy() 

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.most_recent_capture_arr)

        util.msg_box('Success!', 'USER WAS REGISTERED SUCCESSFULLY!!!')
        self.register_new_user_window.destroy()


    def try_again_register_new_user(self):
        print("Try Again button pressed")
        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
