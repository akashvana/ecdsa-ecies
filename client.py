#this is the webpage that the client will use to send a message to the admin
from ecdsa import SigningKey, SECP256k1
from ecies import encrypt, decrypt
import binascii
import json
from os import path 

print("This is the page that will open for the people in the organization if they have already registered")

user_name = input("Enter the username that you used to register: ")
user_id = input("Enter the user id used during registration: ")

file_name = user_name + user_id + "details.json"

with open(file_name, "r") as file: 
    details = json.load(file)

ADMIN_PUBLIC_KEY = "0x81945326ddff050bfde04840593a3c84ea22f93427d0cb3e0d33a1097f8e0e10558d3893bf0ddffa4287fc2b9ff5aa75b042fff77d5c3863e22af8220e4c25fa"


# sends a message to the admin for verification:

# message = b"Some plain-text for encryption"

message = input("Enter the string that you want to encrypt and send to the admin")
message = bytes(message, 'utf-8')

readable_sk = details["signing_key"]
sk_string = bytes.fromhex(readable_sk)
sk = SigningKey.from_string(sk_string, curve = SECP256k1)

signature = sk.sign(message)
signature_hex = signature.hex()
encrypted = encrypt(ADMIN_PUBLIC_KEY, message)
encrypted_hex = encrypted.hex()


# now store the username, userid and encrypted message for the admin to verify: 

messages = [
    {
        "user_name": "",
        "user_id": "",
        "encrypted_message": "",
        "signature": ""
    }
]

for msg in messages:
    msg['user_name'] = user_name
    msg['user_id'] = user_id
    msg['encrypted_message'] = encrypted_hex
    msg['signature'] = signature_hex

my_path = "messages.json"
if path.exists(my_path):
    with open(my_path , 'r') as file:
        previous_json = json.load(file)
        users = previous_json + messages
        
with open(my_path , 'w') as file:
    json.dump(messages, file, indent = 4)


print("Your message has been sent to the admin")
