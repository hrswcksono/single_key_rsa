import math

# Rivest Shamir Adleman (1976)

# rahasia
# p dan q bilangan prima
# d kunci deskripsi
# m plaintext
# totient = (p-1).(q-1)

# tidak rahasia
# e kunci enkripsi , PBB(e, totient) = 1
# c chipertext
# n = p.q

def pbb(a, b):
    temp = 0
    while(1):
        temp = a%b
        if(temp == 0):
            return b
        a = b
        b = temp

def isInteger(a):
    if(a.is_integer()):
        return 1
    return 0

def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))

def split2Ascii(text):
    result = list()
    i = 0
    while i < len(text):
        if(text[i] == '1'):
            result.append(text[i:i+3])
            i+=3
        else:
            result.append(text[i:i+2])
            i+=2
    return result

def toAscii(text):
    ascii_values = [ord(character) for character in text]
    return ascii_values

def toChar(text):
    result = ""
    for idx in text:
        result += chr(int(idx))
        # print(idx)
    return result

def toList(string):
    li = list(string.split(" "))
    return li

def listToString(s): 
    # initialize an empty string
    str1 = "" 
    # traverse in the string  
    for ele in s: 
        str1 += str(ele)  
    # return string  
    return str1

class RSA():

    def getPrivateKey(self, totient, e):
        if(pbb(totient, e) != 1):
            return "Public key tidak memenuhi syarat"
        k = 1
        while(k):
            d = (1 + k*totient)/e
            if(isInteger(d) == 1):
                return int(d)
            k+=1

    def n(self, a, b):
        return a*b

    def totient(self, a, b):
        return (a-1)*(b-1)

    def encrypt(self, m, e, n):
        return pow(m,e,n)

    def decrypt(self, c, d, n):
        return pow(c,d,n)

    def send(self, m, key):
        n = len(str(key.split(" ")[1])) - 1
        temp = split2len(listToString(toAscii(m)), n)
        # print(temp)
        result = ""
        i = 0
        for idx in temp:
            if(i == 0):
                result = str(self.encrypt(int(idx), int(key.split(" ")[0]), int(key.split(" ")[1])))
                i=1
            else:
                result += " " + str(self.encrypt(int(idx), int(key.split(" ")[0]), int(key.split(" ")[1])))
        return result

    def receive(self, c, key):
        temp = list()
        c = toList(c)
        for idx in c:
            temp.append(self.decrypt(int(idx), int(key.split(" ")[0]), int(key.split(" ")[1])))
        return toChar(split2Ascii(listToString(temp)))

# if __name__ == '__main__':
#     p , q = 47, 71
#     encrypt = 79
#     d = RSA()

#     plaintext = "HARI INI"

#     n = d.n(p,q)
    
#     totient = d.totient(p,q)
#     decrypt = d.getPrivateKey(totient, encrypt)

#     privateKey = str(decrypt) + " " + str(n)
#     publicKey = str(encrypt) + " " + str(n)

#     send = d.send(plaintext, publicKey)
#     receive = d.receive(send, privateKey)

#     print(publicKey)
#     print(privateKey)
#     print(send)
#     print(receive)
    # print(pow(3, 79, 3337))
