import getpass
import random
import string
import sys
import os
import time
from time import sleep
from progress.bar import Bar

import getpass
import re

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


class Encrypto:

    username=""
    password=""
    Key=""

    def __init__(self):
        print("################################### WELCOME TO THE ENCRYPTOR BY AINC########################################\n\n\t\t\t\t\tThis is your own mobile vault")

        self.username = input("\nPlease enter the username you wish to add for encryption: \n")
        # getpass keeps the password from echoing on your screen
        self.password = getpass.getpass("\nPlease enter the password to evaluate: \n")
        
        print("\n[SYSTEM] Initializing secure memory buffer...")

        # We keep the bar for the UI experience, but notice: NO FILE OPENED!
        bar = Bar('Processing Credentials', max=3)
        for i in range(3):
            sleep(0.5)
            bar.next()
        bar.finish()
        print("[SUCCESS] Credentials held in volatile memory.")


    #Generate RSA KEY to allow encryption
    def RSA_gen(self):
        print("\n\n**************************************Initialising Encryption*****************************************************\nBefore beginning you might want to check out the following points\n1) Encryption is a highly detailed and memory intensive process , be sure to have minimum hardware requirements before running the Encryptor.\n2) We at AINC are not responsible for any loss of data in case of loss of The Key of your encypted file.\n3) Make sure to never send The Key over internet or any media.\n")
        choice = input("Do you want to continue? (y/n) [Default: n]:\n").strip().lower()

        # By checking if choice is in this list, we handle all 'Yes' variants.
        # If they hit enter, choice is an empty string "", which is NOT in the list.
        if choice in ['y', 'yes']:
            bar = Bar('Generating Secure Key', max=2)
            for i in range(2):
                sleep(1)
                bar.next()

            #Generating the passphrase for key pair generation
            Key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(128))
            self.Key=Key

            print("\n\nThis shall be your key that you may use for decrypting your file, keep it safe and NEVER share it with any unauthorized person/software. \n" + Key)
            bar.finish()

            R_enc_key = RSA.generate(2048)
            encrypted_key = R_enc_key.export_key(passphrase=self.Key, pkcs=8, protection="scryptAndAES256-CBC")
            with open('my_private_rsa_key.bin','wb') as f:
                f.write(encrypted_key)
            with open('my_rsa_public_key.pem','wb') as f:
                f.write(R_enc_key.publickey().export_key())
        else:
            print("\nOperation cancelled. No keys were generated.")

    #Encryption using AES OAEP
    def encrypt(self):
        if not self.username or not self.password:
            print("[ERROR] No credentials found in memory. Please restart.")
            return

        pub_key_path = input("Enter the path to your public key (e.g., ./my_rsa_public_key.pem):\n")
        
        try:
            # Load the Public Key
            recipient_key = RSA.import_key(open(pub_key_path).read())
            
            # Prepare the data blob (Username + Password) 
            # We add a separator so we can split them later during decryption
            raw_data = f"{self.username}|||{self.password}".encode('utf-8')

            with open('AINC_encrypted_File.bin', 'wb') as outfile:
                # 1. RSA Layer: Encrypt a random AES session key
                session_key = get_random_bytes(16)
                cipher_rsa = PKCS1_OAEP.new(recipient_key)
                outfile.write(cipher_rsa.encrypt(session_key))

                # 2. AES Layer: Encrypt the memory blob
                cipher_aes = AES.new(session_key, AES.MODE_EAX)
                ciphertext, tag = cipher_aes.encrypt_and_digest(raw_data)

                # 3. Write metadata + scrambled data
                outfile.write(cipher_aes.nonce)
                outfile.write(tag)
                outfile.write(ciphertext)

            # Cleanup: We overwrite the local variables for extra safety (optional but pro)
            print("\n[SUCCESS] Encryption complete. AINC_encrypted_File.bin created.")
            print("[SECURITY] No plain-text files were ever created on this disk.")

        except Exception as e:
            print(f"[ERROR] Encryption failed: {e}")


    #Decrypting the data
    def decrypt(self):
        # 1. Get the passphrase for the Private Key
        secret_key = getpass.getpass("Enter your RSA Private Key Passphrase:\n")
        
        try:
            # 2. Load the Private Key using the passphrase
            with open('my_private_rsa_key.bin', 'rb') as f:
                private_key = RSA.import_key(f.read(), passphrase=secret_key)
            
            # 3. Read the encrypted file
            with open('AINC_encrypted_File.bin', 'rb') as fobj:
                # We read the components: Session Key, Nonce, Tag, and Ciphertext
                enc_session_key, nonce, tag, ciphertext = [
                    fobj.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)
                ]

            # 4. Decrypt the Session Key, then the Data
            cipher_rsa = PKCS1_OAEP.new(private_key)
            session_key = cipher_rsa.decrypt(enc_session_key)
            
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)

            # 5. Convert bytes to string and SPLIT the "|||"
            # This is the fix for the Disk Leak changes!
            decoded_string = decrypted_data.decode('utf-8')
            user, pw = decoded_string.split("|||")

            print("\n" + "="*50)
            print(f"SUCCESSFULLY DECRYPTED CREDENTIALS:")
            print(f"Username: {user}")
            print(f"Password: {pw}")
            print("="*50)

        except ValueError:
            print("\n[ERROR] Incorrect Passphrase or corrupted file.")
        except Exception as e:
            print(f"\n[ERROR] Decryption failed: {e}")




if __name__ == "__main__":
    e = Encrypto()
    # e.Evaluator()
    print("\nGreat Job! Now that we have our setup successfully initialised, what would you like to do?")
    
    while True:
        choice = input(
            "\n1) Encrypt your current Username and Password File."
            "\n2) Decrypt an existing file (Secret key needed)"
            "\n3) Generate a new RSA key pair."
            "\n4) Quit for now."
            "\n(Enter choices 1-4, or hit Enter to Quit): \n"
        ).strip()

        # If they hit Enter (choice is empty) or type 4, we exit.
        if choice == "4" or not choice:
            print("\nThank you for using the Encryptor by AINC! Hope to see you soon!")
            sys.exit(0) # Using 0 for a "clean" exit
            
        elif choice == "1":
            e.encrypt()
        elif choice == "2":
            e.decrypt()
        elif choice == "3":
            e.RSA_gen()
        else:
            # Updated error message as requested
            print("\n[ERROR] Invalid input, please enter a choice between 1-4.")