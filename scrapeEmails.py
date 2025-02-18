import extract_msg
import os 


msg_folder_path = "conti/mails"
vault = "vault.txt"

def extract_emails_from_email_folder(msg_folder):
  for filename in os.listdir(msg_folder):
    if filename.endswith(".msg"):
      msg = extract_msg.Message(msg_folder + "/" + filename)
      with open(vault, "w", encoding="utf-8") as f:
        f.write(msg.sender + "\n")
        f.write(msg.to + "\n")
        # f.write(msg.cc + "\n")
        # f.write(msg.bcc + "\n")
        f.write(str(msg.date) + "\n")
        f.write(msg.subject + "\n")
        f.write(msg.body + "\n")
        f.write("\n")

extract_emails_from_email_folder(msg_folder_path)
