from cryptography.fernet import Fernet

key = "cCqy_Jc4rSnxoySgu7sMf75-jTZ12_HuvXB3wPCx8ws="
system_information_e = "e_system_info.txt"
clipboard_information_e = "e_clipboard_info.txt"
key_information_e = "e_keys_information.txt"

encrypted_files = [system_information_e, clipboard_information_e, key_information_e]
count = 0

for decrypting_file in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], 'wb') as f:
        f.write(decrypted)

    count += 1