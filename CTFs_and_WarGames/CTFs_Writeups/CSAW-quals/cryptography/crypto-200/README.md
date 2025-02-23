# CSAW CTF 2014 - Cryptography 200 - Psifer School


The problem starts with the following text:

> There's no heartbleed here. Why don't we use these ciphers?
>
> nc 54.209.5.48 12345
>
> Written by psifertex


------

## Stage One: Caesar Cipher


#### Connecting to the Server

We start typing the **netcat** command in the terminal:

```sh
nc 54.209.5.48 12345
```

We get the following message back:

> Welcome to psifer school v0.002
>
> Your exam begins now. You have 10 seconds, work fast.
>
> Here is your first psifer text, a famous ancient roman would be proud if you solve it.
>
> psifer text: **wkh dqvzhu wr wklv vwdjh lv vxshuvlpsoh**
>
>Time's up. Try again later.

This text gives a cipher ``` wkh dqvzhu wr wklv vwdjh lv vxshuvlpsoh``` and the hint *a famous ancient roman would be proud*. That's all we need to decipher it!


#### Frequency Analysis
The famous roman is **Caesar**, and [his cryptographic scheme] is one of the simplest possible. This cipher is also known as  **rotation cipher**, because all we do is rotating the letters by some value (the **key**). A modern version of it is called **ROT13**, meaning **rotation by 13 places**. This is a simple letter substitution cipher which replaces each letter with the 13th letter after it in the alphabet. In this case, we say that the *key is 13*.

In our problem, we don't know the key. However, there is a method to circumvent it: we can count how many times each letter appears in the text and then we use some previous knowledge about the frequency of each letter in the English words. For example, in the English language, *e*, *t*, *a*, *o*, and *n* are frequent letters while *z* or *v* is not. This means that we can analyze the frequency of each character to determine what's the most probable rotation key.

To count the frequency of characters in our cipher, we write a snippet that creates a counter [dictionary (hash table)] with all the (lowercase) characters as the dictionary's keys. Note that we could have used Python's [Counter() data-structure] as well. We then iterate through each character in the message, counting their frequency, and returning a sorted list of these values:


```python
import string

def frequency(msg):
    # Compute the word frequencies
    dict_freq = dict([(c,0) for c in string.lowercase])
    diff = 0.0
    for c in msg.lower():
        if 'a'<= c <= 'z':
            diff += 1
            dict_freq[c] += 1
    list_freq = dict_freq.items()
    list_freq.sort()
    return [b / diff for (a, b) in list_freq]
```




#### Deciphering the Cipher



Using a [well-known table of word frequency values], we write a snippet that does the following:

 1. First, for each of the 26 letters, we subtract its known frequency value from the frequency obtained from our message.
 2. Second, we find what is the minimum value from those subtractions. The closest value is the most probable value for the rotation key.


```python
def delta(freq_word, freq_eng):
    # zip together the value from the text and the value from FREQ
    diff = 0.0
    for a, b in zip(freq_word, freq_eng):
        diff += abs(a - b)
    return diff

def decipher(msg):
    # Decipher by frequency
    min_delta, best_rotation = 20, 0.0
    freq = frequency(msg)
    for key in range(26):
      d = delta(freq[key:] + freq[:key], FREQ_ENGLISH)
        if d < min_delta:
            min_delta = d
            best_rotation = key
    return cipher(msg, -best_rotation)
```




Once we have the key, we just plug it back to the cipher algorithm, inverting the rotation to the other side, with ```cipher(msg, -best_rotation)```. In this cipher function, we iterate through all the character in the message, checking whether it's a letter or a special character. If it is the former case we perform the following operations:

 1. We start getting the integer representing the [Unicode] code point of the character.
 2. To get its position in the alphabet and we subtract it from the Unicode value of *a*, given by **ord('a')** (this is 97).
 3. We add the key value to it to get the (absolute) shift position.
 4. Now we need to remember that this cipher is a ring, *i.e*, adding more stuff should always lead to a *spot* within the 26 letters in the alphabet. That's why we apply an [module] operation to this number to get the *relative* position in the letter's table.
 5. Finally, we just need the value of the shift to the Unicode of *a* to get the position of the character in the cipher.
 6. Remember we are using *-key*, so instead of making a new cipher, we are using the same steps to rotate the cipher to the other side to recover the message.

```python
def cipher(msg, key):
    # Make the cipher
    dec = ''
    for c in msg.lower():
        if 'a' <= c <= 'z':
             dec += chr(ord('a') + (ord(c) - ord('a') + key) % 26)
        else:
             dec += c
    return dec
```

Bingo! The snippets above lead us to our first answer in this problem:

> the answer to this stage is **supersimple**

Netcating several times can return other similar answers such as **hopeyouautomate** or **easypeesy** or **notveryhard**. They are all correct.



#### Automating the Response

To advance forward, we need to send one of the above answers to the socket. However, we only **have 10 seconds** to do this! It's clear that we need to automate this problem with a script.

We can do this in many ways. In Python, for example, we can use the libraries [telnetlib] or [socket] or even writing our [own netcat script]. We will use the former for this exploit. Let us create a telnet connection with:

```python
from telnetlib import Telnet

PORT = 12345
HOST = '54.209.5.48'

tn = Telnet(HOST ,PORT)
```

In this case, socket reading can be done with ```tn.read_until(b'psifer text: ')```, which reads until a given string is encountered,  or ```tn.read_all()```, which reads all data until EOF.

To write a string to the socket we do ```tn.write(mystring.encode() + b'\n')```. Here, the method [encode()] returns an encoded version of the string, *i.e* a translation of a sequence of bytes to a Unicode string.


As a side note, if we had decided to use the [socket] library to create a *TCP socket*, the process would be easy as well:

```python
s = socket(AF_INET, SOCK_STREAM)
s.connect(HOST)
```

Here ```socket.AF_UNIX, socket.AF_INET, socket.AF_INET6``` are constants that represent the address (and protocol) families. The constants ```socket.SOCK_STREAM, socket.SOCK_DGRAM, socket.SOCK_RAW, socket.SOCK_RDM, socket.SOCK_SEQPACKET```represent the socket types.

To read the socket stream we would use commands such as ```s.recv(2048)``` and for writing, we could use ```s.sendall(answer)```.



#### Decrypting and Sending the Answer
Now, back to our problem. After creating the telnet connection, we read whatever comes in:
```python
tn.read_until(b'psifer text: ')
```

We decode and decrypt the text, and then encode it again:
```python
msg_in1 = tn.read_until(b'\n').decode().strip()
dec_msg_in1 = decipher(msg_in1)
answer1 = dec_msg_in1.split()[-1].encode() + b'\n'
```

Finally, we send our answer to the telnet session (the same answer obtained before):
```python
tn.write(answer1)
```

-----------------------------------------

## Stage Two: Offset with Special Characters

The second stage starts with the following message:


> Congratulations, you have solved stage 1. You have 9 seconds left.
>
> Now it's time for something slightly more difficult. Hint, everybody knows it's
> not length that matters.

Together with the hint *length doesn't matter*, we get the following cipher (translated as a Python string variable because of the special characters):

```I'lcslraooh o rga tehhywvf.retFtelh mao ae  af ostloh lusr bTsfnr, epawlltddaheoo  aneviedr ose rtyyng etn aini ft oooey hgbifecmoswuut!oa eeg   ar rr h.u t. hylcg io we ph ftooriysneirdriIa utyco gfl oostif sp u"+'""'+"flcnb  roh tprn.o h```


To crack this cipher we need to deal with special characters to find the rotation shift. We proceed with the following steps:

 1. We start looping over the length of our message, where for each iteration we create a blank list with the size of the message. This is a bit *space-expensive* and it should be optimized if we needed to scale for larger problems. It's fine for our current problem.

 2. We start a second loop, which will tell us about the shifts. This loop iterates again in the length of the message, this time adding the current character to the list we've created before and updated a pointer to the pacing value given in the first loop. Notice that we have a loop inside another, so this solution has *O(n^2) runtime* and it also should be optimized for larger problems.

 3. Inside this second loop, we check whether the pacing pointer is larger than the length of the message, and if this is the case, we register it in a shift counter. The former pointer receives the value of this shift. This is the end of the second loop.

 4. Back to the first loop, we add all the characters so far from our list into the message string. But when should we stop doing this? Until we make sure that had a rotation that produces real words. I tried a few common words, and 'you' worked just fine!


```python
def solve2(msg):
  # Shift cypher, but dealing with special characters
  for j in range(2, len(msg)):

    dec_msg = ['0'] * len(msg)
    idec_msg, shift = 0, 0

    for i in range(len(msg)):
      dec_msg[idec_msg] = msg[i]
      idec_msg += j

      if idec_msg >  len(msg) - 1:
        shift += 1
        idec_msg = shift
    dec_msg = "".join(dec_msg)

    if "you" not in dec_msg: continue
    return dec_msg
```

After decoding this stage's cipher we get the key for the next stage, which is then sent back through the socket:

> I hope you don't have a problem with this challenge. It should be fairly straight forward if you have done lots of basic crypto. The magic phrase for your efforts is "**not not wrong**". For your efforts, you will get another challenge!



----

## Stage Three: Vigenere Cipher

The next message lets us know that we are close to the end:

> Congratulations, you have solved stage 2. You have 9 seconds left.
> Last one.

And comes with the following cipher:
```
MVJJN BQXKF NCEPZ WWVSH YFCSV JEEBB UVRMX HKPIE PMMVZ FOPME ZQIIU EUZZW CGHMV BKBTZ BBHVR MVTQP ENXRM HIRNB WTGDZ CFEDS TKBBW HBFDI KILCM MUUPX WUNIN PWPFJ IEZTP MVQBX ACVKN AEMPV KQXAB ZMDUD ILISV NHKBJ FCIMW HTUVR MNNGU KIFED STLLX XAOUN YVEGV BEXEI BHJNI GHXFI FQFYV VXZFE FXFFH OBVXR MVNLT NHUYY FEZWD GBKEL SGFLM LXBFO NEIOS MZHML XAJUX EIKWH YNAIK SOFLF EEKPI XLSDB PNGHV XHFON MSFOL VMNVX HIRNB XBGTF FOEUZ FZMAS NZEGL HFTPM PDNWM DVKCG WHAFE OKWXF ZIBRQ XCSJI FIMVJ EAFEK MIRXT PBHUC YEEFP MZNMP XZBDV EMMHM VFTQU ABISA EWOMZ NMPXZ BDVPL HGFWF XISSX RMPLB HFRML RHKJU IGXPO OKNHQ TYFKB BWAOS UYKXA OOZNG IXRTK IUIBT ZFOOI LCMMY WEECU FZLMF DMVWK CIHPT BTPES OXYLC HIQII UEUZZ RFKIT RZYUO IMVFT IWITB ENCEP UFFVT XVBUI KNAVH IHYCM MYWUY YETLA PJNHJ MVFGF TMGHF ONBWL HBKCV EMSBT BHJMV FCYOI EGJDH HXTAB JIVLB GUKBX JNBOP NAMGU JJNAE MRFGY GHBBH FHPLB QIIUG HHALV SRSNU FKNAE MDPVG FMZVU SYXBT QUCSM LXFJX BMSYT TVNMS LIDTY LWY
```

This is a **[Vigenere Cipher]**, which is basically several Caesar ciphers in sequence, with different shift values, given by a key-word. Finding these shifts when we don't know the key can be done by writing the alphabet 26 times in different rows. In this case, each alphabet is shifted cyclically to the left compared to the previous alphabet (26 Caesar ciphers).

Although we could use some [online Vigenere cracker] to extract the flag from this text, we will instead write a code. We  use Python's library [pygenere], which has the methods  ```crack_message()``` to decipher the message and ```crack_codeword()``` to find the key (useful because we don't have the key). We then send our cipher to the following function:

```python
def solve3(msg):
  key =  VigCrack(msg).crack_codeword()
  dec_msg = VigCrack(msg).crack_message()
  dec_msg =  dec_msg.replace(" ", "")
  return key, dec_msg
```

This will give us the **key = TOBRUTE** and the deciphered text. After fixing the spaces between the words, we get:

```
THIS TIME WE WILL GIVE YOU MORE PLAINTEXT TO WORK WITH YOU WILL PROBABLY FIND THAT HAVING EXTRA CONTENT THAT IS ASCII MAKES THIS ONE MORE SOLVABLE IT WOULD BE SOLVABLE WITHOUT THAT BUT WE WILL MAKE SURE TO GIVE LOTS OF TEXT JUST TO MAKE SURE THAT WE CAN HANDLE IT I WONDER HOW MUCH WILL BE REQUIRED LETS PUT THE MAGIC PHRASE FOR THE NEXT LEVEL IN THE MIDDLE RIGHT HERE NORMALWORD OK NOW MORE TEXT TO MAKE SURE THAT IT IS SOLVABLE I SHOULD PROBABLY JUST PUT IN SOME NURSERY RHYME OR SOMETHING MARY HADA LITTLE LAMB LITTLE LAMB LITTLE LAMB MARY HADA LITTLE LAMB WHOSE FLEEZE WAS WHITE AS SNOW I DONT WANT TO MAKE THIS HARDER THAN IT NEEDS TO BE IF YOU VE SOLVED A LOT OF SIMPLE CRYPTO CHALLENGES YOU PROBABLY ALREADY HAVE THE CODE AND WILL BREEZE RIGHT THROUGH IT IF IT HELPS MOST OF THE PLAINTEXT IS STATIC AT EACH OF THE LEVELS I M NOT A MASOCHIST THE FUNNY THING IS THAT DEPENDING ON WHICH RANDOMKEY YOU GET THAT POEM MIGHT BE EXACTLY THE RIGHT OFFSET TO SUCCESSFULLY MOUNT AN ATTACK WE LL SEE LITTLE BIT MORE LITTLE BIT MORE THERE,
```
Reading it carefully give us the last answer for the flag: **NORMALWORD**. Sweet!




## Final Words

If you like this solution, take a look at my  [exploit for this problem].

**Hack all the things!**

[his cryptographic scheme]: http://en.wikipedia.org/wiki/Caesar_cipher
[exploit for this problem]: https://github.com/autistic-symposium/sec-pentesting-toolkit/tree/master/CTFs_and_WarGames/2014-CSAW-CTF/cryptography/crypto-200
[scripts from other authors]:https://github.com/go-outside-labs/CTFs-and-Hacking-Scripts-and-Tutorials/tree/master/2014-CSAW-CTF/cryptography/crypto-200/from_the_net
[well-known table of word frequency values]: http://en.wikipedia.org/wiki/Letter_frequency
 [telnetlib]: https://docs.python.org/2/library/telnetlib.html
 [socket]: https://docs.python.org/2/library/socket.html
 [own netcat script]: https://github.com/go-outside-labs/CTFs-and-Hacking-Scripts-and-Tutorials/blob/master/Tutorials/Useful_Scripts/netcat.py
 [pygenere]: http://smurfoncrack.com/pygenere/pygenere.php
 [Vigenere Cipher]: http://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
 [online Vigenere cracker]: http://smurfoncrack.com/pygenere/
[dictionary (hash table)]: https://docs.python.org/2/tutorial/datastructures.html#dictionaries
[Counter() data-structure]: https://docs.python.org/2/library/collections.html#collections.Counter
[ord()]: https://docs.python.org/2/library/functions.html#ord
[module]: http://en.wikipedia.org/wiki/Modulo_operation
[Unicode]: http://en.wikipedia.org/wiki/Unicode
[encode()]: https://docs.python.org/2/library/stdtypes.html#str.encode
