from ecdsa import SigningKey, VerifyingKey, SECP256k1

sk = SigningKey.generate(curve=SECP256k1)
vk = sk.verifying_key

print('Private key: ', sk.to_string().hex())
print('Public key: ', vk.to_string().hex())

# Tạo Key