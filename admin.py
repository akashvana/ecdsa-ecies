# this is the webpage that the admin will use to receive the message and verify the user
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecies import encrypt, decrypt
import binascii
import json
from os import path 

print("This is the admin page that will verify the user and can view the message sent by the user")

ADMIN_PRIVATE_KEY = "0x8c84d32cc09a04f8b3d9d8c766f647267bf59b9691c693d45cfad80c0e60808c"


def check_user_valid(user_name, user_id, signature_hex, encrypted_message): 

    # admin loads all the users that have been registered so far to get their details 
    user_file = "users.json"
    users = {}
    with open(user_file, "r") as usr: 
        users = json.load(usr)

    # compare the users json and get the verifying key for the user. First decrypt the message using admin private key and then verify using verifying key of the user
    for usr in users: 
        usr_name = usr["user_name"]
        usr_id = usr["user_id"]

        if(str(usr_name) == str(user_name) and str(usr_id) == str(user_id)):
            
            encrypted = bytes.fromhex(encrypted_message) 
            verifying_key = usr["verifying_key"]
            ver = bytes.fromhex(verifying_key)
            vk = VerifyingKey.from_string(ver, curve = SECP256k1)

            #first decrypt the message sent by the user: 
            decrypted = decrypt(ADMIN_PRIVATE_KEY, encrypted) 

            #verify the signature of the sender: 
            signature = bytes.fromhex(signature_hex)
            check = vk.verify(signature, decrypted)

            if check == True: 
                return True
            else:
                return False
            
        else: 
            continue

    return False