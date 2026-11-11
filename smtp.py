import tkinter as tk
from tkinter import messagebox
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def authenticate(user, password):
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
        server.starttls(context=ssl.create_default_context())
        server.login(user, password)


class Compose:
    def __init__(self, parent, user, password):
        self.user = user
        self.password = password
        self.window = tk.Toplevel(parent)
        self.window.title("Compose email")
        frame = tk.Frame(self.window, padx=25, pady=20)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="From: " + user).pack(anchor="w", pady=5)
        tk.Label(frame, text="To").pack(anchor="w")
        self.recipient = tk.Entry(frame, width=55)
        self.recipient.pack(fill="x", pady=5)
        tk.Label(frame, text="Subject").pack(anchor="w")
        self.subject = tk.Entry(frame, width=55)
        self.subject.pack(fill="x", pady=5)
        tk.Label(frame, text="Message").pack(anchor="w")
        self.body = tk.Text(frame, width=55, height=15)
        self.body.pack(fill="both", expand=True, pady=5)
        self.send_button = tk.Button(frame, text="Send", command=self.sendemail)
        self.send_button.pack(pady=10)
        self.recipient.focus_set()

    def sendemail(self):
        recipient = self.recipient.get().strip()
        if not recipient:
            messagebox.showerror("Missing recipient", "Enter the recipient's email address.", parent=self.window)
            return
        self.send_button.config(state="disabled")
        self.window.update_idletasks()
        try:
            message = MIMEMultipart()
            message["From"] = self.user
            message["To"] = recipient
            message["Subject"] = self.subject.get()
            message.attach(MIMEText(self.body.get("1.0", "end-1c"), "plain", "utf-8"))
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(self.user, self.password)
                server.sendmail(self.user, recipient, message.as_string())
        except (smtplib.SMTPException, OSError, ValueError):
            messagebox.showerror("Send failed", "Check the recipient, credentials and connection before retrying.", parent=self.window)
        else:
            messagebox.showinfo("Sent", "Your email was sent.", parent=self.window)
        finally:
            self.send_button.config(state="normal")


if __name__ == "__main__":
    from main import main
    main()
