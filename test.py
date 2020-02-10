class Table:
    def __init__(self,table=None):
        self.Update.table = table
    class Update:
        table=None
        def __init__(self,arr=[]):
            f = f'UPDATE {self.table} SET '
            i=1
            for column,value in arr:
                f += f"{column}='{value}'"
                if i!=len(arr):
                    f += ', '
                i += 1
            self.Where.update = f
        class Where:
            update=None
            def __init__(self,arr=[]):
                print(self.update)


Table("alias").Update([("hasinstagram","-1"),("nombre","invalida")])
# f.Table("table").update([{"columna":"value"}]).where([{"id":"flamingo"}],"AND")
# # import requests
# # import base64
#
# # from Crypto.PublicKey import RSA
#
#
#
# # # import base64
# # # import hashlib
# # # from Crypto import Random
# # # from Crypto.Cipher import AES
# # #
# # # class AESCipher:
# # #
# # #     def __init__(self, key):
# # #         self.bs = AES.block_size
# # #         self.key = hashlib.sha256(key.encode()).digest()
# # #
# # #     def encrypt(self, raw):
# # #         raw = self._pad(raw)
# # #         iv = Random.new().read(AES.block_size)
# # #         cipher = AES.new(self.key, AES.MODE_CBC, iv)
# # #         return base64.b64encode(iv + cipher.encrypt(raw.encode()))
# # #
# # #     def decrypt(self, enc):
# # #         enc = base64.b64decode(enc)
# # #         iv = enc[:AES.block_size]
# # #         cipher = AES.new(self.key, AES.MODE_CBC, iv)
# # #         return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
# # #
# # #     def _pad(self, s):
# # #         return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
# # #
# # #     @staticmethod
# # #     def _unpad(s):
# # #         return s[:-ord(s[len(s)-1:])]
# # #
# # #
# # #
# # # p = AESCipher("f5a1fdb4e2e032e5d3b42c3350d69918eebdb640e2f9cc0fe1fc55cd7800cf30")
# # # m = p.encrypt("tupapa")
# # # print(m)
# #
# #
# #
# #
# # # from Crypto.Cipher import AES
# # # import binascii, os
# # # import base64
# # # import hashlib
# # #
# # #
# # # pkey = "f5a1fdb4e2e032e5d3b42c3350d69918eebdb640e2f9cc0fe1fc55cd7800cf30"
# # #
# # # def parsePkey(pkey):
# # #     n = []
# # #     for o in range(0,len(pkey),2):
# # #         n.append(int(str(pkey[o:o+2:]),16))
# # #     return bytearray(n)
# # #
# # # def encrypt_AES_GCM(msg, secretKey):
# # #   aesCipher = AES.new(secretKey, AES.MODE_GCM)
# # #   ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
# # #   return (ciphertext, aesCipher.nonce, authTag)
# # #
# # # def decrypt_AES_GCM(encryptedMsg, secretKey):
# # #   (ciphertext, nonce, authTag) = encryptedMsg
# # #   aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
# # #   plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
# # #   return plaintext
# # #
# # # secretKey = parsePkey(pkey)
# # #
# # # print("Encryption key:", binascii.hexlify(secretKey))
# # #
# # # msg = b'tupapa'
# # # encryptedMsg = encrypt_AES_GCM(msg, secretKey)
# # # print(encryptedMsg)
# # # print(base64.b64encode(encryptedMsg))
# # # #
# # # # print("encryptedMsg", {
# # # # 'ciphertext': binascii.hexlify(encryptedMsg[0]),
# # # # 'aesIV': binascii.hexlify(encryptedMsg[1]),
# # # # 'authTag': binascii.hexlify(encryptedMsg[2])
# # # # })
# # # #
# # # decryptedMsg = decrypt_AES_GCM(encryptedMsg, secretKey)
# # # print("decryptedMsg", decryptedMsg)
# # #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# from Crypto.Cipher import AES
# from Crypto.PublicKey import RSA
# from Crypto import PublicKey
# import  numpy as np
# import time,sys,base64,os
#
#
# def enc_password(password,pubkey,keyid,time):
#     if 64 != len(pubkey):
#         sys.exit("public_key invalida")
#     def parsePkey(pkey):
#         n = []
#         for o in range(0,len(pkey),2):
#             n.append(int(str(pkey[o:o+2:]),16))
#         return n
#     def decodeUTF8(n):
#         n = str(n).encode('utf-8').decode('unicode_escape')
#         c = bytearray(len(n))
#         i = 0
#         for t in n:
#             c[i] = ord(t)
#             i += 1
#         return list(c)
#     o = 100
#     u = o + len(password)
#     pubkey = parsePkey(pubkey)
#     key = os.urandom(32)
#     iv = os.urandom(12)
#     tag_length = 16
#     y = bytearray(u)
#     y[0] = 1
#     y[1] = int(keyid)
#
#     aesCypher = AES.new(key, AES.MODE_GCM,mac_len=tag_length)
#     cipherText,cipherTag = aesCypher.encrypt_and_digest(bytearray(password,'utf-8'))
#     cipherText = cipherText + cipherTag
#
#
#     pubkeySeal = bytes(pubkey)
#
#
#     print(pubkey)
#     print(pubkeySeal)
#
#
#     sys.exit()
#
#
#
#     pubkeySeal = PublicKey(bytes(pubkey))
#     privkeySeal = PrivateKey(bytes(key))
#     sealed = SealedBox(pubkeySeal)
#     final_sealed = sealed.encrypt(bytes(key)) # length 80
#     y[2] = 80 # sealed.length >> 8 & 255,
#     js_set(y,final_sealed,4)
#     f = 84
#     s = numpy.frombuffer(cipherText,dtype=numpy.uint8)
#     c = s[-len(password):]
#     h = s[0:len(password)]
#     y[84] = c[0]
#     y[85] = c[1]
#     f = 100
#     y[100] = h[0]
#     y[101] = h[1]
#     #print(s)
#     #print(c)
#     #print(h)
#     final_enc = str(b64encode(y).decode('utf-8'))
#     app = 6
#     return "#PWD_INSTAGRAM_BROWSER"+':'+str(app)+':'+time+':'+final_enc
#
#
#
#
# # print(parsePkey(pkey))
# password = "tupapa"
# pkey = "f5a1fdb4e2e032e5d3b42c3350d69918eebdb640e2f9cc0fe1fc55cd7800cf30"
# pkeyid = "245"
# time = int(time.time()*1000)
# # #
# # #
# # #
# enc_password(password,pkey,pkeyid,time)
# # #
# #
# #
# # """
# # #PWD_INSTAGRAM_BROWSER:
# # 6:
# # 1580001437990:
# # AfVQADwi1Dn1hEcQV4BhNlLa2rVHPOT+qCyUpgaI5+u4FMUrjeWhTcgcZX6vM13QGxmX2RzSIBUMTdgq76USHquJWVk5nHMfjLpukZmJ2U0WaE7aGuCx7cYAA4Oe8MVskVzrFXAOgMzMHg==
# #
# # """
