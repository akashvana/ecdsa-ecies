#this is the webpage that the client will use to send a message to the admin
from ecdsa import SigningKey, SECP256k1
from ecies import encrypt, decrypt
import binascii
import admin
import json
from os import path 

print("This is the page that will open for the people in the organization if they have already registered")

def user_login(user_name, user_id, signing_key, message):
    details = {}
    file_name = user_name + str(user_id) + "details.json"

    if path.exists(file_name):
        with open(file_name , 'r') as file:
            details = json.load(file)        
    else:
         return False


    ADMIN_PUBLIC_KEY = "0x81945326ddff050bfde04840593a3c84ea22f93427d0cb3e0d33a1097f8e0e10558d3893bf0ddffa4287fc2b9ff5aa75b042fff77d5c3863e22af8220e4c25fa"

    # message which will be sent by the user and encrypted
    message = bytes(message, 'utf-8')

    signing_key = details["signing_key"]
    readable_sk = signing_key
    sk_string = bytes.fromhex(readable_sk)
    print(sk_string)
    sk = SigningKey.from_string(sk_string, curve = SECP256k1)
    print(sk)

    signature = sk.sign(message)
    signature_hex = signature.hex()
    encrypted = encrypt(ADMIN_PUBLIC_KEY, message)
    encrypted_message = encrypted.hex()


    # now store the username, userid and encrypted message for the admin to verify:

    print("Your message has been sent to the admin")

    valid = admin.check_user_valid(user_name, user_id, signature_hex, encrypted_message)
    return valid
