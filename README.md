# Encryptor
A password encryptor package for Linux written in Python.
Credit for project goes to ScorchingShade.

>This is a powerful software to be used only at user's risk.
>RSA and AES encrytion techniques ensure that your data is secure and safe. 
>A menu driven program to easily begin using The Encryptor.
>It takes one username and password at a time and encrypts them in a secure file. Further versions will see an addition to the number of pairs that can be added.
>The method ensures that while sending any credentials to authorised users, only they have the access to it.
>Adding such methods allows you to provide true end to end encryption, without revealing any sensitive info.
>Some features are explained below
>DISCLOSURE: This is not a substitute for a fully vetted program such as veracrypt. USE AT YOUR OWN RISK AND DISCRETION. THIS COMES WITH ABSOLUTELY NO WARRANTY!!!!
#### Commands to run on Terminal
Use the following commands on Linux to run the Program
```sh
$ python3 Source.py 
```

### Understanding The Encryptor
  - The Encryptor uses AES and RSA encryption.

  - Optimal asymmetric encryption padding used for sturdier encryption.
  - 'Nonce' to ensure AES encryption.
  - Does not leave any trace of the file on the disk unencrypted as that is NOT SECURE. All operations are done in RAM to prevent Disk Leak.
  

## Dependencies
You must have Python 3.x and Pycryptodome installed. In addition to this, several custom packages are included in the bin folder of the Repository.. 
```sh
 pip install pycryptodome 
 ```
Modifications by Marlin H.