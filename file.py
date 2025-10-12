from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
from binascii import unhexlify

# Define key and IV (both should be bytes)
key = b'0123456789012345'
iv = b'0123456789012345'

# Ciphertext in hex (convert to bytes)
ciphertext = unhexlify('955380124f2e00e0')

# Initialize DES cipher in CBC mode
cipher = DES.new(key, DES.MODE_CBC, iv)

# Decrypt and remove padding
plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)

# Convert to readable format (string if it's text)
print(plaintext.decode('utf-8'))
