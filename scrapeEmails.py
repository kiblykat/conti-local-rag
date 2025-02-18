import extract_msg
import os 
import re

msg_folder_path = "conti/mails"
vault_file = "vault.txt"

def extract_emails_from_email_folder(msg_folder):
  for filename in os.listdir(msg_folder):
    if filename.endswith(".msg"):
      # get message text
      msg = extract_msg.Message(msg_folder + "/" + filename)
      # write into vault
      with open(vault_file, "a", encoding="utf-8") as f:
        # f.write(msg.sender + "\n")
        # f.write(msg.to + "\n")
        # - # Normalize whitespace and clean up text
        text = re.sub(r'\s+', ' ', msg.body).strip()
        f.write(text + "\n" + "\n")
        # f.write(msg.cc + "\n")
        # f.write(msg.bcc + "\n")
        # f.write(str(msg.date) + "\n")
        # f.write(msg.subject + "\n")
        # f.write("\n")

extract_emails_from_email_folder(msg_folder_path)
