from tinyec import registry
from Crypto.Cipher import AES
import secrets, hashlib, binascii

def encryption_AES(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decryption_AES(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

def ecc_to_256_bitkey(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()

curve = registry.get_curve('brainpoolP256r1')

def ECC_Encrytion(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_to_256_bitkey(sharedECCKey)
    ciphertext, nonce, authTag = encryption_AES(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)

def ECC_Decrytion(storedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = storedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_to_256_bitkey(sharedECCKey)
    plaintext = decryption_AES(ciphertext, nonce, authTag, secretKey)
    return plaintext
