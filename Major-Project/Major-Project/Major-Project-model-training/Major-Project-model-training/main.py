import cipherImplementation.vigenere as vg
import cipherImplementation.playfair as pf


t = vg.encrypt_message("hello","how are you doing this my friend")
print(t)
dt = vg.decrypt_message("hello",t)
print(dt)

t2 = pf.encode("how are you doing this my friend","bello")
print(t2)
dt2 = pf.decode(t2,"bello")
print(dt2)

