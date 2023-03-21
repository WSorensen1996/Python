from cryptography.fernet import Fernet




key = Fernet.generate_key()
print(key)


def do_encrypt(message, key):
    fernet = Fernet(key)
    ciphertext = fernet.encrypt(message.encode())
    print("original string: ", ciphertext)
    return ciphertext


def do_decrypt(ciphertext,key):
    fernet = Fernet(key)
    decmessage = fernet.decrypt(ciphertext).decode()
    print("decrypted string: ", decmessage)
    return decmessage

message = "SOME MESSAGE!"
encrypted_msg = do_encrypt(message, key)
decrypted_msg = do_decrypt(encrypted_msg,key)


