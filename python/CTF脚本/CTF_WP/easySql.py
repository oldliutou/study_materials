import hashlib
import random

# salt = random('Aa0', 40)
# print(salt)
string1 = "admin"

out1 = hashlib.sha256(string1.encode('utf-8')).hexdigest()

print(out1)