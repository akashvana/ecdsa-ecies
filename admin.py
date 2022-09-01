# this is the webpage that the admin will use to receive the message and verify the user
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecies import encrypt, decrypt
import binascii
import json
from os import path 

print("This is the admin page that will verify the user and can view the message sent by the user")

ADMIN_PRIVATE_KEY = "0x8c84d32cc09a04f8b3d9d8c766f647267bf59b9691c693d45cfad80c0e60808c"

# admin loads all the messages that have been sent so far
file_name = "messages.json"

with open(file_name, "r") as msg: 
    messages = json.load(msg)

# admin loads all the users that have been registered so far to get their details 
user_file = "users.json"
with open(user_file, "r") as usr: 
    users = json.load(usr)

# compare the users json and get the verifying key for the user. First decrypt the message using admin private key and then verify using verifying key of the user
for msg in messages: 
    user_name = msg["user_name"]
    user_id = msg["user_id"]
    encrypted_message = msg["encrypted_message"]
    encrypted = bytes.fromhex(encrypted_message)
    signature_hex = msg["signature"]
    for user in users: 
        usr_name = user["user_name"]
        usr_id = user["user_id"]    
        verifying_key = user["verifying_key"]
        ver = bytes.fromhex(verifying_key)
        vk = VerifyingKey.from_string(ver, curve = SECP256k1)

        if user_name == usr_name and user_id == usr_id: 

            #first decrypt the message sent by the user: s
            decrypted = decrypt(ADMIN_PRIVATE_KEY, encrypted) 
            print(user_name + "'s decrypted message is: ")
            print(decrypted)

            #verify the signature of the sender: 
            signature = bytes.fromhex(signature_hex)
            check = vk.verify(signature, decrypted)

            if check == True: 
                print("Verification successful")
            else:
                print("verification failed for the user")
