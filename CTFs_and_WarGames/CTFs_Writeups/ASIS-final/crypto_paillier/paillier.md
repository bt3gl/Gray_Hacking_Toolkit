# On Paillier, Binary Search, and the ASIS CTF 2014


## The Cryptosystem

The challenge was started by netcating to ```nc asis-ctf.ir 12445```:

      > Here we use a well-known cryptosystem, which introduced in late 90s as a part of PhD Thesis. This cryptosystem is a probabilistic asymmetric algorithm, so computer nerds are familiar with the basics. The power of this cryptosystem is based on the fact that no efficient general method for computing discrete logarithms on conventional computers is known. In real world it could be used in a situation where there is a need for anonymity and a mechanism to validate, like election. What's the name of this cryptosystem?

Google promptly gave the answer and this returned back an [oracle]:

[netcating]:http://netcat.sourceforge.net/


```sh
paillier
The secret is: 642807145082286247713777999837639377481387351058282123170326710069313488038832353876780566208105600079151229044887906676902907027064003780445277944626862081731861220016415929268942783162708816500946772808327134830134079094377390069335173892453677535279678315885291394526580800235039893009001625481049390361761336337647597773237774304907266052473708273977012064983893047728185071148350402161227727584760493541436392061714945686426966193498593237383322044894184438689354989491800002299012669235551727100161976426628760839759603818593410342738847167887121724862806632881028892880165650108111619269651597119870237519410
Tell us your choice:
[E]ncrypt: [D]ecrypt:
```

Of course, simply decrypting the secret wouldn't work.



### Pai-what?



The [Paillier cryptosystem] was named after *Pascal Paillier*, its inventor, in 1999. It is a **probabilistic** **asymmetric** algorithm used for applications such as [electronic voting].

Being [probabilistic] means that a message is encrypted with some **randomness**, so it can generate several different ciphers. All the ciphers will be decrypted back to the same message (but not the other way around).

Being [asymmetric] means that it is based on **public-key cryptography**, *i.e.*, two keys  are generated, a public and a private. The public key is used to encrypt the message and the private key is used to decipher a ciphered message.



[asymmetric]: http://en.wikipedia.org/wiki/Asymmetric_algorithm
[electronic voting]:http://en.wikipedia.org/wiki/Pascal_Paillier#Applications
[probabilistic]: http://en.wikipedia.org/wiki/Probabilistic_encryption


### All right, now tell me something interesting...

What matter for us is the fact that this system has a [homomorphic] propriety. Well, from Latin, *homo* means *the same* (like *homogeneous*) and *morphic* means *form* (like *metamorphosis*). So this propriety says that the cipher  conserves the form of the message, even if we play  with it. This propriety in a cryptographic algorithm is also called [malleability].

In other words, if we know only the public key (which is the [modulo]m **n**, a multiplication of two large prime numbers), we can manipulate the cipher and still get the original content of the plain message.

For example, the multiplication of a **cipher 1** by a **cipher 2** is decrypted as a sum of the **message 1** to **message 2**:

[modulo]: http://en.wikipedia.org/wiki/Modulo_operation

![equation](http://www.sciweavers.org/tex2img.php?eq=D%5CBigg%5B%20%5CBig%28E%28m_1%29%20%2A%20E%28m_2%29%20%20%20%5CBig%29%20%5C%25%20n%5E2%20%5CBigg%20%5D%3D%20%5CBig%20%28m_1%20%2B%20m_2%20%5CBig%20%29%20%5C%25%20n&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

And, look at this: we can also exponentiate the cipher by some constant **k**!


![equation](http://bit.ly/1z5KmHi)

Pretty cool, huh? I think so... :)


[malleability]: http://en.wikipedia.org/wiki/Malleability_(cryptography)
[homomorphic]: http://en.wikipedia.org/wiki/Homomorphic_encryption


### Simple implementation of a Paillier system

Let's highlight the implementation of this system in Python. All we need is a large prime number generator, which we can borrow from [pyCrypto].


[pyCrypto]: https://www.dlitz.net/software/pycrypto/

#### Generating the keys

The public key has five elements:

- **n**, which is the multiplication of two large prime numbers (**p** and **q**);

- **g**, which is **n+1**;

- **lambda**, which is the [least common multiple] of **(p-1)** and **(q-1)**; and


- **mu**, which is the [modular multiplicative inverse], to ensure that **n** divides **g**. We use Pythons [gmpy] library for this task.

[gmpy]: https://code.google.com/p/gmpy/
[least common multiple]: http://en.wikipedia.org/wiki/Least_common_multiple
[modular multiplicative inverse]: http://en.wikipedia.org/wiki/Modular_multiplicative_inverse




```python
import Crypto.Util.number cry
import gmpy

def generate_keys(bits):
    p = cry.getPrime(bits//2)
    q = cry.getPrime(bits//2)
    g = n+1
    n = p*q
    l = (p-1)*(q-1)
    mu = gmpy.invert(((p-1)*(q-1)), n)
    return n, g, l, mu
```

#### Encrypting...

The encryption is straightforward. All we need is a random number:

```python
import random
rand = random.randint(n//2, n*2)
```

So we write:

```python
def encrypt(n, g, msg, rand):
    return (pow(g, msg, n**2) *
            pow(rand, n, n**2)) % (n**2)
```

#### Decrypting...

The decryption is the other way around:

```python
def decrypt(n, l, mu, cipher):
    return (((pow(cipher, l, n**2) - 1) // n**2) *mu) % n
```

An interesting fact is that we can actually break the cipher if we have the public key and the random number:

```python
def decrypt_breaking(n, m, g, cipher, rand):
    n_sqr = n * n
    trash = pow(rand, n, n_sqr)
    trash = gmpy.invert(trash, n_sqr)
    norm = (cipher * trash) % n_sqr
    return ((norm - 1) // n) // ((g-1)// n)
```


All right, time to go back to our challenge.

----

## Understand Challenge


Performing some recon in the oracle, I noticed the following:

* Encryption and decryption of any **integer** works...

```
[E]ncrypt: [D]ecrypt: e
Tell us your message to encrypt: 1
Your secret is: 73109965080485247131710209266123910705889636744106672869822932981580432295328645599823550448181731566435402609978665387224898646975403769881196399448975370668935092605229755765060164052771714510987944591017615792396157094596290728393053648253053017939625091326878542241485082342371560710778399247063411414649475517288243167425022137869055256778307340931947663486971023680806406250041891606619955393621120918102708442427400288119511466304393700124201965017764148482926998000012235997591413309617388902575733355188418714479900913342627281937156809563150498906460101268562252351167461233533852277300215020108137992142
Tell us your choice:
------------------------
[E]ncrypt: [D]ecrypt: d
Tell us your secret to decrypt: 73109965080485247131710209266123910705889636744106672869822932981580432295328645599823550448181731566435402609978665387224898646975403769881196399448975370668935092605229755765060164052771714510987944591017615792396157094596290728393053648253053017939625091326878542241485082342371560710778399247063411414649475517288243167425022137869055256778307340931947663486971023680806406250041891606619955393621120918102708442427400288119511466304393700124201965017764148482926998000012235997591413309617388902575733355188418714479900913342627281937156809563150498906460101268562252351167461233533852277300215020108137992142
Your original message is: 1
```

* ... but **up to a size**! I tried to input a ridiculous large number and it was rejected. Anything a bit larger than an encrypted message was rejected. This is important! It means that the we might have a [modulo] here. It also means that we cannot just multiply two ciphers and ask the oracle, since the message would be too large.

* The secret was **changing periodically** (probably each hour). It means that the keys (the module) were changing too. This ruins any plan of **brute forcing** it.


* Remember I said that the Paillier encryption is [probabilistic], *i.e.*, different ciphers can map back to the same value? This was clear from the oracle: if you asked repetitively to encrypt some number, say *1*, it would return different messages each time.  Interesting enough, however, if you restarted the system (leaving the session and netcating again), the *same order* of different ciphers would appear again. Completely deterministic.


* Everything that is **not an integer** number was rejected by the oracle (no shortcuts here).



### Automatizing Responses

Whenever we have a netcat challenge, I like to have a clean script to get and send messages (copying from terminal is lame).

In addition, all the numbers in this challenge were really long (the encrypted messages had 614 chars), so we need to perform operations in a consistent and efficient way.

To work with long numbers in Python, I use the [Decimal] library. For instance, considering that we could want to add two messages, I set the context to 1240 bytes:

```
decimal.getcontext().prec = 1240
```

For now on I will be using modifications of this snippet to interact with the oracle:

```python
import decimal
import socket

def nc_paillier():
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # answer the initial question
    print s.recv(4096)
    s.send(b'paillier')

    # get the secret
    print s.recv(4096)
    m = s.recv(4096)

    # cleaning it
    m = (m.split(": ")[1]).split('\n')[0]

    # it's good to print (because it changes periodically)
    print("The secret is: ")
    print(m)

    # change from str to long decimal
    mdec = decimal.Decimal(m)

    '''
        From here you can do whatever you want.
    '''
    # If you want to encrypt messages
    msg_to_e = '1'

    s.send(b'E')
    print s.recv(4096)
    s.send(msg_to_e)
    me = s.recv(4096)
    me = me.split(": ")[1]

    print("Secret for %s is:" %(msg_to_e))
    print(me)

    medec = decimal.Decimal(me)

    # If you want to decrypt messages
    msg_to_d = me

    s.send(b'D')
    s.recv(4096)
    s.recv(4096)
    s.send(msg_to_d)
    md = s.recv(4096)
    md = md.split(": ")[1].strip()

    print("Decryption is: ")
    print(md)

    mddec = decimal.Decimal(md)

if __name__ == "__main__":
    # really long numbers
    decimal.getcontext().prec = 1240

    PORT = 12445
    HOST = 'asis-ctf.ir'

    nc_paillier()
```


[Decimal]: https://docs.python.org/2/library/decimal.html

----
## Solving the Challenge




### Finding out the Modulo

At this point we know that we cannot do anything in the Paillier system without knowing the modulo, **n**. Of course, this value was not given. However, from the recon we have learned that we can find it from the oracle.

The exactly value when the oracle cycles back to the beginning is our **n**. This value should not return any message since **n%n = 0**. So, we are looking for this **None** result.

What's the 101 way to search for a number? [Binary search], of course! Adapting one of [my scripts], I wrote the snippet below to look for this number:


```python

import decimal
import socket

def bs_paillier(lo, hi, s):
    if hi < lo: return None
    mid = (hi + lo) / 2
    print("We are at: ")
    print(mid)

    s.send(b'E')
    s.recv(4096)
    s.recv(4096)
    s.send(str(mid))
    ans = s.recv(4096)
    print ans

    if 'None' in ans:
        print "Found it!"
        return mid + 1
    elif 'Your message is' in ans:
        return bs_paillier(lo, mid-1, s)
    else:
        return bs_paillier(mid+1, hi, s)

def get_mod_paillier():

    # create socket, answer first question
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.recv(4096)
    s.send(b'paillier')
    s.recv(4096)

    # start binary search
    hi, lo = 11**307, 10**307
    mod = bs_paillier(lo, hi, s)
    print mod

if __name__ == "__main__":

    PORT = 12445
    HOST = 'asis-ctf.ir'

    get_mod_paillier()
```

The script took around 5 minutes to be finished, returning our **n**. We are ready to break this system!



### Convoluting and Decrypting the Answer

We use the first **homomorphic** propriety to craft a message which will give us the flag:

```python
def convolution(e1, e2, m2, mod):
    return (e1 * e2 )%(mod*mod)
```

This returns:

```
112280008116052186646368021111109237871341887479615992317427354059600212357857288108129264030737539972269011409996912208818076010168198529262326772763879996822102998582534816837233418191109543582310863266347760528961946352593880742472731062537568071764692096627743690922908221673060800965135164509962029222789740380393803936034322030637125612078147029021325858011668393839188326210425016990153989714767763564793169128967154011677910768035056556423954036535193602627342043345257626256977045594687342553610052190731351090959432138598081567054374046432685112246445454537701332996220698854386609070078979440083610540257
```

Sending it back with the decrypting option returns our (possible) **flag minus 1** (remember, **this is the message 2**).



### Getting the Flag!

Of all the possible options of decoding our flag, it was obvious that they were hexadecimal values that should be converted to ASCII.

It also helped the fact that I had in mind the ASCII representation of the word *ASIS*, which is given by *41 53 49 53*:

```sh
$ python -c "print '0x41534953'[2:].decode('hex')"
ASIS
```

This is easier with the following script:

```python
def print_hex(secret):
    # cutting L in the end
    a = hex(secret)[:-1]
    # cutting the \x symbol
    b = a[2:].decode('hex')
    return b
```

Running it, we get the hexadecimal form of our flag:
```
32487808320243150435316584796155571093777738593139558163862909500838275925645449950017590
```
And its ASCII decoding returns the flag:
``` sh
The flag is:
ASIS_85c9febd4c15950ab1f19a6bd7a94f87

```



----

[Paillier cryptosystem]: http://en.wikipedia.org/wiki/Paillier_cryptosystem
[here]: https://github.com/autistic-symposium/sec-pentesting-toolkit/tree/master/CTFs_and_WarGames/2014-ASIS-CTF/crypto_paillier
[modulo]: http://en.wikipedia.org/wiki/Modulo_operation
[oracle]: http://en.wikipedia.org/wiki/Oracle_machine
[ASIS CTF]: http://asis-ctf.ir/home/
[Binary search]:http://en.wikipedia.org/wiki/Binary_search_algorithm
[my scripts]: https://github.com/autistic-symposium/master-algorithms-pytree/master/src/searching_and_sorting/searching