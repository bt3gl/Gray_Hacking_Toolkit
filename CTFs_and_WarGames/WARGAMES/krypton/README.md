# Cryptography War: Beating Krypton

The problems are very straightforward and very similar to those from the last [CSAW CTF] ([see my post here]).


**Disclaimer**: if you haven't played WarGames, but you are planning to, PLEASE DON'T READ ANY FURTHER. If you don't try to solve the problems by yourself first, you will be wasting your time.




[Cryptol]: http://www.cryptol.net/
[Wargames]: http://overthewire.org/wargames/
[Krypton]: http://overthewire.org/wargames/krypton/
[CSAW CTF]: https://ctf.isis.poly.edu/



## Level 0: Base64 Transformation


This level starts with:

 > The following string encodes the password using Base64:
 S1JZUFRPTklTR1JFQVQ=
 > Use this password to log in to krypton.labs.overthewire.org with username krypton1 using SSH. You can the files for other levels in /krypton/.


[Base64] is just a way to represent binary data in ASCII, by translating it into a radix-64. Linux provides a built-in Base64 encoder/decoder tool, so all we need to do is:

```
$ base64 -d KRYPTON0.txt

```


[Base64]: http://en.wikipedia.org/wiki/Base64

----

## Level 1: Classic Caesar Cypher

The second level starts with:

 > The password for level 2 is in the file ‘krypton2’. It is ‘encrypted’ using a simple rotation. It is also in non-standard ciphertext format. When using alpha characters for ciphertext it is normal to group the letters into five letter clusters, regardless of word boundaries. This helps obfuscate any patterns. This file has kept the plain text word boundaries and carried them to the ciphertext. Enjoy!


This is the classic [Caesar Cypher] (they really love this thing :).

 In Caesar’s cipher, the letters in the plaintext are shifted by a fixed number of elements down the alphabet. For example, if the shift is 3, A becomes D , B becomes E , and so on. Once we run out of letters, we circle back to A.

We can solve this challenge in a few lines using Linux's built-in [tr] (translate tool):

```
krypton1@melinda:/krypton/krypton1$ VAR=$(cat krypton2)
krypton1@melinda:/krypton/krypton1$ echo $VAR
YRIRY GJB CNFFJBEQ EBGGRA
krypton1@melinda:/krypton/krypton1$ alias rot13="tr A-Za-z N-ZA-Mn-za-m"
krypton1@melinda:/krypton/krypton1$ echo "$VAR" | rot13
```

[Caesar Cypher]: http://en.wikipedia.org/wiki/Caesar_cipher
[tr]: http://linux.die.net/man/1/tr


-----

## Level 2

The third level starts with:

 > ROT13 is a simple substitution cipher.

 > Substitution ciphers are a simple replacement algorithm. In this example of a substitution cipher, we will explore a 'monoalphabetic' cipher. Monoalphebetic means, literally, "one alphabet" and you will see why.

 > This level contains an old form of cipher called a 'Caesar Cipher'.
 > A Caesar cipher shifts the alphabet by a set number. For example:

 > plain: a b c d e f g h i j k ...
 > cipher: G H I J K L M N O P Q ...

 > In this example, the letter 'a' in plaintext is replaced by a 'G' in the ciphertext so, for example, the plaintext 'bad' becomes 'HGJ' in ciphertext.

 > The password for level 3 is in the file krypton3. It is in 5 letter group ciphertext. It is encrypted with a Caesar Cipher. Without any further information, this ciphertext may be challenging to break. You do not have direct access to the key, however, you do have access to a program that will encrypt anything you wish to give it using the key. If you think logically, this is completely easy.


First, we make a file filled with the alphabet, so we can test the binary:

```sh
$ ln -s /krypton/krypton2/keyfile.dat keyfile.dat
$ echo {A..Z} {a..z} > file
$ cat file
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z
```

Running the binary:
```
$ /krypton/krypton2/encrypt file
$ cat ciphertext
MNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKL
```

We see a ROT14 (since ROT13 starts in N).

As a second way to find the rotation, we could use [ltrace]:
```
$ ltrace /krypton/krypton2/encrypt file | less
```

Which shows things such as:

```
fgetc(0x602250) = 'A'
toupper('A') = 'A'
isalpha(65, 65, 0x7ffff7dd0d00, -1, 0xffffffff) = 1024
fputc('M', 0x602490) = 77
```


Now that we know the rotation number, we can decrypt the password in the same way as we did in the previous level:

```sh
krypton2@melinda:/tmp$ alias rot14="tr A-Z O-ZA-N"
krypton2@melinda:/tmp$ echo "$VAR" | rot14

```


[ltrace]: http://linux.die.net/man/1/ltrace

---

## Level 3: Frequency Analysis

This level starts with:

 > Well done. You've moved past an easy substitution cipher.

 > Hopefully you just encrypted the alphabet a plaintext to fully expose the key in one swoop.

 > The main weakness of a simple substitution cipher is repeated use of a simple key. In the previous exercise, you were able to introduce arbitrary plaintext to expose the key. In this example, the cipher mechanism is not available to you, the attacker.

 > However, you have been lucky. You have intercepted more than one message. The password to the next level is found in the file 'krypton4'. You have also found three other files. (found1, found2, found3)


This time we have to use [frequency analysis] to count the number of times each letter appears in our message. The results are compared to the frequency in each we see letters in English. This is enough to break this type of cipher.

For this purpose, I wrote the following script:


```python
import string
import sys
import operator

FREQ_ENGLISH = [0.0749, 0.0129, 0.0354, 0.0362, 0.1400, 0.0218, 0.0174, 0.0422, 0.0665, 0.0027, 0.0047, 0.0357,0.0339, 0.0674, 0.0737, 0.0243, 0.0026, 0.0614, 0.0695, 0.0985, 0.0300, 0.0116, 0.0169, 0.0028, 0.0164, 0.0004]

def find_frequency(msg):
 dict_freq = dict([(c, 0) for c in string.lowercase])
 total_letters = 0.0
 for c in msg.lower():
 if 'a'<= c <= 'z':
 dict_freq[c] += 1
 total_letters += 1
 list_freq = sorted(dict_freq.items(), key=operator.itemgetter(1))
 return [(c, freq/total_letters) for (c, freq) in list_freq]

def main(filename):
 with open(filename, 'r') as f:
 cipher = f.readlines()
 cipher = cipher[0].strip()
 flist = find_frequency(cipher)
 elist = dict((k, value) for (k, value) in zip(string.lowercase, FREQ_ENGLISH))
 elist = sorted(elist.items(), key=operator.itemgetter(1))
 trans, key = '', ''
 for i, f in enumerate(flist):ls
 trans += f[0]
 key += elist[i][0]
 print "CIPHER: %s -> %.5f, ENGLISH: %s -> %.5f" %(f[0], f[1], elist[i][0], elist[i][1])
 print "Key is " + key + " for " + trans

 # print key sorted to translate to a-z
 res = zip(trans, key)
 res.sort()
 trans, key = '', ''
 for letter in res:
 trans += letter[1].upper()
 key += letter[0].upper()
 print "tr [" + key + "] [" + trans + "]"

if __name__ == "__main__":
 main(str(sys.argv[1]))
```


Running it gives us the key:

```
$ cat /krypton/krypton3/found1 > cipher
$ cat /krypton/krypton3/found2 >> cipher
$ cat /krypton/krypton3/found3 >> cipher
$ /krypton/krypton3$ python freq.py cipher
$ alias rotvi='tr ABCDEFGHIJKLMNOPQRSTUVWXYZ BOIHPKNQVTWGURXZAJEYSLDFPU'
$ cat /krypton/krypton3/krypton4 | rotvi
```

We could also use [this online tool] to find the frequencies.

[this online tool]: http://www.richkni.co.uk/php/crypta/freq.php

[frequency analysis]: http://en.wikipedia.org/wiki/Frequency_analysis

----

## Level 4: Vigenere Cipher I

The fifth level starts with:

 > So far we have worked with simple substitution ciphers. They have also been ‘monoalphabetic’, meaning using a fixed key, and giving a one to one mapping of plaintext (P) to ciphertext (C). Another type of substitution cipher is referred to as ‘polyalphabetic’, where one character of P may map to many, or all, possible ciphertext characters.

 > An example of a polyalphabetic cipher is called a Vigenère Cipher. It works like this:

 > If we use the key(K) ‘GOLD’, and P = PROCEED MEETING AS AGREED, then “add” P to K, we get C. When adding, if we exceed 25, then we roll to 0 (modulo 26).

 > P P R O C E E D M E E T I N G A S A G R E E D\
 > K G O L D G O L D G O L D G O L D G O L D G O\
 > becomes:

 > P 15 17 14 2 4 4 3 12 4 4 19 8 13 6 0 18 0 6 17 4 4 3\
 > K 6 14 11 3 6 14 11 3 6 14 11 3 6 14 11 3 6 14 11 3 6 14\
 > C 21 5 25 5 10 18 14 15 10 18 4 11 19 20 11 21 6 20 2 8 10 17\
 > So, we get a ciphertext of:

 > VFZFK SOPKS ELTUL VGUCH KR
 > This level is a Vigenère Cipher. You have intercepted two longer, english language messages. You also have a key piece of information. You know the key length!

This is a classic case of [Vigenere cipher], which is a variation on Caesar’s cipher. In this case, one uses multiple shift amounts according to a keyword.

To solve this, we use the [pygenere] library in Python. First, we need to find the key:

```pyhton
import sys
from pygenere import Vigenere, VigCrack

def get_key(msg):
 # Vigenere Cypher
 key = VigCrack(msg).crack_codeword()
 dec_msg = VigCrack(msg).crack_message()
 dec_msg = dec_msg.replace(" ", "")
 return key, dec_msg

if __name__ == '__main__':
 # getting the key
 with open('cipher', 'r') as f:
 msg = f.readlines()
 msg_in = msg[0].strip()
 key, answer = get_key(msg_in)
 print 'Message: ' + msg_in
 print
 print 'Answer: ' + answer
 print '(key: ' + key + ')'
```

The deciphered text is:
 > THESOLDIERWITHTHEGREENWHISKERSLEDTHEMTHROUGHTHESTREETSOFTHEEMERALDCITYUNTILTHEYREACHED
THEROOMWHERETHEGUARDIANOFTHEGATESLIVEDTHISOFFICERUNLOCKEDTHEIRSPECTACLESTOPUTTHEMBACK
INHISGREATBOXANDTHENHEPOLITELYOPENEDTHEGATEFOROURFRIENDSWHICHROADLEADSTOTHEWICKEDWITCHOF
THEWESTASKEDDOROTHYTHEREISNOROADANSWEREDTHEGUARDIANOFTHEGATESNOONEEVERWISHESTOGOTHATWAY
HOWTHENAREWETOFINDHERINQUIREDTHEGIRLTHATWILLBEEASYREPLIEDTHEMANFORWHENSHEKNOWSYOUAREIN
THECOUNTRYOFTHEWINKIESSHEWILLFINDYOUANDMAKEYOUALLHERSLAVESPERHAPSNOTSAIDTHESCARECROWFOR
WEMEANTODESTROYHEROHTHATISDIFFERENTSAIDTHEGUARDIANOFTHEGATESNOONEHASEVERDESTROYEDHER
BEFORESOINATURALLYTHOUGHTSHEWOULDMAKESLAVESOFYOUASSHEHASOFTHERESTBUTTAKECAREFORSHEIS
WICKEDANDFIERCEANDMAYNOTALLOWYOUTODESTROYHERKEEPTOTHEWESTWHERETHESUNSETSANDYOUCANNOT
FAILTOFINDHERTHEYTHANKEDHIMANDBADEHIMGOODBYEANDTURNEDTOWARDTHEWESTWALKINGOVERFIELDS
OFSOFTGRASSDOTTEDHEREANDTHEREWITHDAISIESANDBUTTERCUPSDOROTHYSTILLWORETHEPRETTYSILKDRESS
SHEHADPUTONINTHEPALACEBUTNOWTOHERSURPRISESHEFOUNDITWASNOLONGERGREENBUTPUREWHITETHERIB
BONAROUNDTOTOSNECKHADALSOLOSTITSGREENCOLORANDWASASWHITEASDOROTHYSDRESSTHEEMERALDCITYW
ASSOONLEFTFARBEHINDASTHEYADVANCEDTHEGROUNDBECAMEROUGHERANDHILLIERFORTHEREWERENOFARMSN
ORHOUSESINTHISCOUNTRYOFTHEWESTANDTHEGROUNDWASUNTILLEDINTHEAFTERNOONTHESUNSHONEHOTINTHEI
RFACESFORTHEREWERENOTREESTOOFFERTHEMSHADESOTHATBEFORENIGHTDOROTHYANDTOTOANDTHELIONWER
ETIREDANDLAYDOWNUPONTHEGRASSANDFELLASLEEPWITHTHEWOODMANANDTHESCARECROWKEEPINGWATCH


Finally, we use the key to decipher the password:

```python
def solve(msg, key):
 dec_msg = Vigenere(msg).decipher(key)
 dec_msg = dec_msg.replace(" ", "")
 return dec_msg

if __name__ == '__main__':
 # deciphering
 key = 'FREKEY'
 with open('pass', 'r') as f:
 msg = f.readlines()
 answer = solve(msg[0].strip(), key)
 print "The answer is: " + answer
```

[Vigenere cipher]: http://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
[pygenere]: http://smurfoncrack.com/pygenere/pygenere.py




----

## Level 5: Vigenere Cipher II

The sixth level starts with:


 > Frequency analysis can break a known key length as well. Let's try one last polyalphabetic cipher, but this time the key length is unknown.

This is another example of Vigenere Cipher. Using the same method as before, we first get the key and then the password.


