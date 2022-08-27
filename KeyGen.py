from ecdsa import SigningKey, SECP256k1

privateKey = SigningKey.generate(curve=SECP256k1)
publicKey = privateKey.verifying_key

print('Private key: ', privateKey.to_string().hex())
print('Public key: ', publicKey.to_string().hex())

# Tạo Key