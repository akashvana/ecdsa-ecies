# this is the webpage which will be used to register a user to the org and create public and private key pairs for the user. 
from ecdsa import SigningKey, SECP256k1
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import json 
from os import path 
import binascii

# ADMIN PUBLIC KEY
# ADMIN_PRIVATE_KEY = "0x8c84d32cc09a04f8b3d9d8c766f647267bf59b9691c693d45cfad80c0e60808c"

print("This is the page that will open for new users")
print("Since you are a new user, we will generate your public keys and private keys")
# generates public and private key pair for the user: 
priv_key = generate_eth_key()
priv_key_hex = priv_key.to_hex()
pub_key_hex = priv_key.public_key.to_hex()

users = [
    {
        "user_name": "",
        "user_id": "",
        "verifying_key": "",
        "public_key": ""
    }
]

user_details = {
        "signing_key": "",
        "verifying_key": "",
        "private_key": "",
        "public_key": ""
    }

# can have more fields for registering the user to the organization. 
user_name = input("Enter your username: \n")
user_id = input("Enter your userId: \n")

#generate a signing key and a verifying key for the given username and userID: 
sk = SigningKey.generate(curve= SECP256k1) #gives SigningKey object
readable_sk = sk.to_string().hex() 
pk = sk.get_verifying_key() #public key corresponding to private key
readable_pk = pk.to_string().hex()

# we will also have to generate a public key and a private key for encrypting and decrypting the message

for user in users:
    user['user_name'] = user_name
    user['user_id'] = user_id
    user['verifying_key'] = readable_pk
    user['public_key'] = pub_key_hex

user_details['signing_key'] = readable_sk
user_details['verifying_key'] = readable_pk
user_details['private_key'] = priv_key_hex
user_details['public_key'] = pub_key_hex


# this is the json file that the admin will have from which it will validate the users 
my_path = 'users.json'

if path.exists(my_path):
    with open(my_path , 'r') as file:
        previous_json = json.load(file)
        users = previous_json + users
        
with open(my_path , 'w') as file:
    json.dump(users, file, indent = 4)


# to store the user details: 
user_path = user_name + user_id + "details.json"

with open(user_path, 'w') as f: 
    json.dump(user_details, f, indent = 4)


print("Registration completed")





# once the public and private keys for the user have been generate, we need to store the public key in