    def delete_message(self, id, event):
        mail = Connect()
        mail = mail.connect(self.user, self.password, "imap.gmail.com")
        mail.select('inbox')
        mail.uid('STORE', str(id), '+FLAGS', '\\Deleted')
        mail.expunge()
        mail.close()
        mail.logout()
        self.subjects()
        self.message['state'] = 'normal'
        self.message.delete(1.0, tk.END)
        self.message['state'] = 'disabled'


# Create the connection class
class Connect:
    # Connect to the server and return
    def connect(self, user, passwd, server):
        mail = imaplib.IMAP4_SSL(server)
        mail.login(user, passwd)
        return mail


# Class for doin operations on the inbox
class GetInbox:
    def get_uids(self, mail):
        mail.select('inbox')
        result, data = mail.uid('search', None, 'ALL')
        return data


# Class for grabbing message headers and uid
class GrabHeader:
    def get_headers(self, mail, uids):
        subjects = []
        for numbers in range(len(uids[0].split())):
            uid = uids[0].split()[numbers]
            result, data = mail.uid('fetch', uid, '(RFC822)')
            raw_data = data[0][1]
            raw_data_string = raw_data.decode('utf-8')
            message = email.message_from_string(raw_data_string)
            subject = str(email.header.make_header(email.header.decode_header(message['subject'])))
            subjects.append({subject: int(uid)})
        return subjects


# Class for retrieving message body
class GetBody:
    def get_body(self, mail, uid):
        result, data = mail.uid('fetch', uid, '(RFC822)')
        raw_data = data[0][1]
        raw_data_string = raw_data.decode('utf-8')
        message = email.message_from_string(raw_data_string)
        for part in message.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                return body.decode()
            else:
                continue


class Application:
    def __init__(self, root):
        self.root = root
        root.title("Mail Application")
        self.frame = tk.Frame(root, padx=30, pady=25)
        self.frame.pack()
        tk.Label(self.frame, text="Sign in to Gmail", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.frame, text="Email address").pack(anchor="w")
        self.email = tk.Entry(self.frame, width=40)
        self.email.pack(pady=5)
        tk.Label(self.frame, text="Google app password").pack(anchor="w")
        self.password = tk.Entry(self.frame, width=40, show="*")
        self.password.pack(pady=5)
        self.login_button = tk.Button(self.frame, text="Sign in", command=self.login)
        self.login_button.pack(pady=15)
        self.email.focus_set()

    def login(self):
        user = self.email.get().strip()
        password = self.password.get().strip()
        if not user or not password:
            messagebox.showerror("Missing details", "Enter your email and app password.", parent=self.root)
            return
        self.login_button.config(state="disabled")
        self.root.update_idletasks()
        try:
            smtp.authenticate(user, password)
        except (smtp.smtplib.SMTPException, OSError):
            messagebox.showerror("Sign-in failed", "Check your email, app password and internet connection.", parent=self.root)
            self.login_button.config(state="normal")
            return
        self.user = user
        self.secret = password
        self.frame.destroy()
        self.frame = tk.Frame(self.root, padx=30, pady=25)
        self.frame.pack()
        tk.Label(self.frame, text="Choose an option", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.frame, text=self.user).pack(pady=5)
        tk.Button(self.frame, text="Send mail", width=25, command=self.compose).pack(pady=10)
        tk.Button(self.frame, text="Open inbox", width=25, command=self.inbox).pack(pady=10)

    def compose(self):
        smtp.Compose(self.root, self.user, self.secret)

    def inbox(self):
        window = tk.Toplevel(self.root)
        window.title("Tkinter Email Client")
        window.configure(padx=10, pady=5)
        try:
            Mail(window, self.user, self.secret)
        except (imaplib.IMAP4.error, OSError, ValueError, TypeError, IndexError) as error:
            window.destroy()
            messagebox.showerror("Inbox unavailable", str(error), parent=self.root)


def main():
    root = tk.Tk()
    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
