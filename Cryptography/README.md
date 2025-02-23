# Cryptography

Often data is just encoded in base64 or hex. Other times it's just compressed (gzip):

* Text 32 characters long --> md5 hash.
* 40 characters long --> SHA1 hash.
* equal signs spread --> base64 encoded string.
* text only letters, without numbers or special characters --> Caesar, Vigenere, or other type of cipher.
*  hints about keys and signing --> likely RSA.



## MD5

- The [MD5 hashing algorithm](http://www.fastsum.com/support/md5-checksum-utility-faq/md5-hash.php) always returns 128 bit values, so the chance that two randomly chosen objects have the same hash is 1:2**128.



* Command Line:

```
$ echo -n password | md5sum
5f4dcc3b5aa765d61d8327deb882cf99
```

* Or you can use Python's md5.md5().digest()

- md5 hashes: [here](http://hash-killer.com/), [here](http://www.md5this.com/), [here](http://www.hashkiller.co.uk/).

- [md5sum](http://linux.about.com/library/cmd/blcmdl1_md5sum.htm)
- [md5 creator](http://www.md5-creator.com/)


### Scripts Available

- Hash length extension attack
- Brute force hex digest chars



------

## SHA

- SHA-1 has output size of 160 bits, so chances of collisions are 2**160.

- [Hash maker](http://ratfactor.com/sha1).

### Scripts
- SHA-256 brute force


### Command Line

- Brute force:
```
import hashlib, itertools
hash = '6307c5441ebac07051e3b90d53c3106230dd9aa128601dcd5f63efcf824ce1ba'
ch = 'abcdef0123456789'
for a, b, c, d, e, f in itertools.product(ch, ch, ch, ch, ch, ch):
    if hashlib.sha256('ASIS_a9%s00f497f2eaa4372a7fc21f0d' % (a + b + c + d + e + f)).hexdigest() == hash:
        print 'ASIS_a9%s00f497f2eaa4372a7fc21f0d' % (a + b + c + d + e + f)
```




--------

## Rotation Ciphers


### Scripts
- Caesar
- Brute force rotation
- Pygenere
- Frequency analysis


### Online tools:

- Frequency analysis: [here](http://www.simonsingh.net/The_Black_Chamber/hintsandtips.html) and [here](http://www.xarg.org/tools/caesar-cipher)

- [Cesar Cipher decryption](http://www.xarg.org/tools/caesar-cipher/) and [here](http://tools.zenverse.net/caesar-cipher/).

- [Vigenere Cipher breaker](http://www.mygeocachingprofile.com/codebreaker.vigenerecipher.aspx) and [here](http://smurfoncrack.com/pygenere/index.php).

### In the terminal...

```sh
$ VAR=$(cat data.txt)
$ echo "$VAR"
$ alias rot13="tr A-Za-z N-ZA-Mn-za-m"
$ echo "$VAR" | rot13
```
### In Python...

In Python [we can use decoding](https://docs.python.org/2/library/codecs.html#codec-base-classes):

```python
"YRIRY GJB CNFFJBEQ EBGGRA".decode(encoding="ROT13")
```

### Readings:

- [How Vigenere works](http://sharkysoft.com/vigenere/).





---

## RSA

* Public-key cryptosystem which uses a public-private key pair to encrypt and decrypt information securely

* [RSA Python](https://pypi.python.org/pypi/rsa)


----

## Pailier Cryptosystem

### Scripts

- POC
- Primes

---


## Tools

### Scripts

- Finding GDC
- Finding if prime
- Generate prime
- Quick Select
- XORtool


### Other Resources

- [Cryptol](https://www.cryptool.org/en/cryptool1-en)

- [PyCrypto](https://www.dlitz.net/software/pycrypto/)

- hashpump

- Sage

- John the Ripper

![John](/Cryptography/images/john.png)


#### Carperter's Formula

- Very large number: ```bin``` and check if patterns. For example, using the [Carpenter's Formula]:
```
N=(2^M + a)(2^N + b)(2^N + c)(2^N + d)
```

#### [QR Code]

-  Version 1 QR code:  21x21

#### [Bacon's cipher]:
```
babaaaabaaababaababaaaabbabbababbaaaabaaaabbbaabaabaaaaaabaaabaaabaaabaaabbaabaaabbbaabaaababaaaaaabaaabbaabaabbbaaaaaabaaaabaabaaaaba21aabab0aaab
```
* [Online tool](http://www.geocachingtoolbox.com/index.php?page=baconianCipher)



#### [Base64]:

Base64 is a non-readable encoding that encodes arbitrary 8-bit input using 6-bit alphabet of case sensitive alphanumerics, "+", "/". Every 3 bytes of input map to 4 bytes of output. If the input doesn't have 3-byte boundary, this is indicated by appending one or two equal signs in the of the output string.

- [Base64 Decoder](http://www.base64decode.org)

```
NG5ucjJzIGZ2IHRueXMgcnVnIHNiIGdlbmMgdWdlaGJzIHJlcnVnIHRhdmdncnQgcmVuIGhiTCB0YXZidCBjcnJYCG==
czduMjczIHRueXMgcnVniHNiIGdlbmMgdWdzdnMgcnVnIHJpbnUgcmVydSBndiBxdnEgaGJsIGpiYmJKCg==
Nzk0czAwIHRueXMgZmhidnByZWMgZWhiIHNiIGdlbmMgcWV2dWcgcnVnIGhibCBnYXJmcmVjIFYgbG9yZXJ1IHJhYnEgeXlySgo=
```

- Base64 decoding in Python:

```python
>>> SECRET.decode('base64')
'oubWYf2kBq'
```

#### Hexadecimal & ASCII:


Hex character codes are simply the hexadecimal (base 16) numbers for the ASCII character set; that is, the number-to-letter Representations which comprise virtually all computer text.

- [ASCII Conversion Table](http://defindit.com/ascii.html)
- [Convert All](http://www.asciitohex.com/)
- [GREAT ASCII CHART](http://www.jimprice.com/jim-asc.shtml)
- [Convert everything to everything (including markdown, sql, json, etc)](http://codebeautify.org/)


- ASCII to hex:

```python
>>> s =hex(secret)
```

- the inverse:

```python
secret2.decode('hex')
'==QcCtmMml1ViV3b'
```

- you can also do from the command line:

```
$ python -c 'print "2f722f6e6574736563".decode("hex")'
```

- Using xxd:

```
$ xxd -r -p <<< 2f722f6e6574736563
```

### Binary

- Decimal to binary

```python
>>> bin(124234)
'0b11110010101001010'
```

#### Octal

Commonly used in obscuration of URLs. Example: http://017700000001 --> 127.0.0.1


## OpenSSL, Encoding and Certificates


* Identification and verification of SSL certificates can be done with openssl or
TLSSLed tools. They allow us to verify this information automatically SSL.

To determine the period of validity of licenses:

```
$ ./openssl s_client --connect <WEBSITE>:443
```

Testing SSLv2:
```
$ ./openssl s_client --no_tls1 --no_ssl3 --connect <WEBSITE>:443
```

* For Identification and verification of encoding supported by the Website we can use  **EcoScan34**.





---

## Block Cipher Encryption

* Electronic code book (ECB) mode.
* Simplest and default block cipher mode.
* Message is split into blocks and each is encrypted separately.
* Disadvantage: identical plaintext block encrypts to identical cipher text block (for example, figures).

### Attacking Randomness

* Good Randomness is vital for cryptographic operations.

* Two common attack against a PRNG :
	- PRGN state is reconstructed from its output.
	- Same PRNG is used more than once.

* Statistically random is not secure random!
	- if a PRNG is seeded with a value the attacker can influence, the state of the PRNG is likely compromised.

* Seed race condition attacks:
	- System clock often used to seed PRNG
	- Submit 10's or 100's of requests at a time. Seed a PRNG with the same system clock and the output will be the same.




----



[SHA]:http://en.wikipedia.org/wiki/Secure_Hash_Algorithm
[MD5]: http://en.wikipedia.org/wiki/MD5
[Base64]: http://en.wikipedia.org/wiki/Base64
[Bacon's cipher]:http://en.wikipedia.org/wiki/Bacon's_ciphe
[Carpenter's Formula]:http://security.cs.pub.ro/hexcellents/wiki/writeups/asis_rsang
[pngcheck]: http://www.libpng.org/pub/png/apps/pngcheck.html
[karmadecay]: http://karmadecay.com/
[tineye]:  https://www.tineye.com/
[images.google.com]: https://images.google.com/?gws_rd=ssl
[base64 decoding]: http://www.motobit.com/util/base64-decoder-encoder.asp
[pnginfo]: http://www.stillhq.com/pngtools/
[namechk]: http://namechk.com
[QR Code]: http://en.wikipedia.org/wiki/QR_code



##  Cryptography Glossary

* **Symmetric encryption (shared key encryption)**: all authorized parties have the same key. It has no means for verifying the sender of a message among any group of shared key users.

* **Block Chaining (CBC)**: operates on blocks of symbols. It's the only appropriate fixed-block cipher in use. If performs an XOR operation with the previous block of data. Most encryption is done by using block ciphers.

* **Modes of Operation of a Block Cipher**: there are four modes of operation:
	1.  **electronic code book** (ECB): The standard mode. It has the disadvantage that for a given key, two identical plaintexts will correspond to identical ciphertexts.
	2. ** cipherblock chaining ** (CBC): The most commonly used. Agreement on a non-secret **initialization vector** (of same length as the plaintext).
	3. **cipher feedback** (CFB): if the plaintext is coming in slowly, the ciphertext can be sent as soon as the plaintext comes in.
	4. **output feedback** (OFB): a way to create a keystream for a stream cipher.

* **The Data Encryption Standard (DES)**: introduced in 1975. It uses a 56 bit key with 8 additional bits for parity check. It operates on blocks of 64 bit plaintexts and gives 64 bit ciphertext. It alternates 16 substitutions with 15 transpositions. In 1997 DES was brute-forced in 24 hours.

* **The Advanced Encryption Standard (AES)**: introduced in 2002. It operates on 128 bit strings. AES has 128 bit key and 128 bit ciphertext and plain  text blocks. So when AES is used to encrypt a text message, it encrypts blocks of 128/8 = 16 symbols. It alternates 10 substitutions with 10 transpositions.


* **Stream Ciphers**: operates symbol-by-symbol. Block ciphers can run in modes that allow them to operate arbitrary size chunks of data. The counter CTR mode cipher is the best choice for a stream cipher. Modern stream ciphers are symmetric key cryptosystems.

* **Synchronous stream cipher**: when you simply XOR the plaintext with the keystream to get the ciphertext.

* **RC4**: the most widely used stream cipher, invented in 1987:
		1. Chose n, a positive integer, say n=8.
		2. Let l = (length in bits)/n
		3. There is a key array K_0...K_{2^n -1} whose entries are n-bit strings (integers from 0 to 2^n -1). You enter the key into that array and then repeat the key as necessary.
		4. The algorithm consists of permuting the integers from 0 2^n -1.

* **Initialization Vector**: is a dummy block used to start a block cipher. It's necessary to force the cipher to produce a unique stream of output. It doesn't need to be kept private but it must be different for every new cipher initialization with the same key.

* **One-time pads**: the keystream is never used again. If each bit of the keystream is truly randomly generated, this implies that each bit is independent of the previous bits. So you don't start with a seed/key that is short and generate a keystream from it (ex: flipping a coin).


-----

* **Asymmetric encryption (public key encryption)**: each party has a different set of keys for accessing the same encrypted data. Main uses:
	1. Agree on a key for a symmetric cryptosystem.
	2. Digital signatures.
	3. Rarely used for message exchange since it is slower than symmetric key cryptosystems.

* **Standard key exchange protocol**: RSA, Diffie-Hellman, El Gamal.

* **Cryptographic signature**: associating a message digest with a specific public key by encrypting the message digest with the sender's public and private key.

* **RSA**: Recall that if gcd(m,n)=1 and a = 1(mod f(n)), then m^a = m (mod n).
	1. Bob picks p, q primes around 1e150.
	2. He computes n = pq ~ 1e300 and f(n)=(p-1)(q-1).
	3. He finds some number e with gcd(e, f(n)) = 1 and computes 1/e mod f(n) = d.
	4. He publishes (n,e) and keep d, p, q hidden.
	5. Alice wants to send Bob the plaintext M (maybe an AES key) enconded as a number 0<=M<n. If the message is longer than n, she breaks into blocks..
	6. Alice looks up Bob's n,e and reduces M^e mod n = C, sending C to Bob.
	7. Bob reduces C^d mod n to get M because C^d = (M^e)^d = M
	8 If Eve intercepts C, it's useless without Bob's d.

You want :

	* gcd(p-1, q-1) to be small.
	* p-1 and q-1 should each have a large prime factor.
	* p and q shouldn't be too closer (ration ~ 4).
	* e can be small: 3, 17=2^4 +1, or 65537=2^16 +1: repeated squares fast for e small, e not have many 1's in binary representation.


People use n of 1024 bits (n ~ 1e308).
Corporates use  2048 bits (n ~ 1e617).
In the early 1990’s, it was common to use 512 bits (n ~ 1e154). An RSA challenge number with n~
2^768 ≈ 1e232 was factored in 2009.

*  **ElGamal**:  used to exchange a key for a symmetric cryptosystem.
	1. Bob chooses a finite field and a generator and a private  key.
	2. Alice encrypts M to Bob. She chooses a random session  and send with the generator and the message.


* **Elliptic Curve Cryptography** (ECC): it has much shorter keys (1/6 bits) than RSA with the same security. It's useful in terms of key agreement and minimal storage computations (such as smart cards).
	- An elliptic curve is a curve described an equation y^2 + a_1 xy + a_3 y = x^3 + a_2 x^2 + a_4 x + a_6.
	- All cublic curves can be brought to this form by a change of variables. The curve closes off in the infinite or zero point.

* **Elliptic Curve Diffie Hellman** (ECDH): chose a finite field, fix some elliptic curve with coefficients in this field , and a pseudo generator point. Each user has a private number and a public key point.

* **Elliptic Curve ElGamal Message Exchange**: how to encode a message as a point? Go to infinite fields.

----

* **Hash functions**: accepts a variable-length input and generates a fixed-sized output. It must be non-reversible and should have no collisions. The simplest forms are the cyclic redundancy check (CRC) and the cryptographic hash functions (SHA-1, SHA-256, MD5).
	- Hashes have an **one-way** property: if given an output  y it is difficult to find any input such as H(x) = y For example, passwords saved as a hash: if you login, it computes the hash and compare (you never calculate back!).
	- **weakly collision free property**: if, given input x, it is difficult difficult to find any x' ̸= x such that H(x) = H(x'′').
	- **strongly collision free property**: if it is difficult to find any x and x' with x ̸= x' such that H(x) = H(x').
	- of all the popular hash functions (MD5, SHA-0, SHA-1, SHA-2): only SHA-2  have the strongly collision free property. In addition, SHA-2 is similar to SHA-1, so it might not either.

* **MAC**: If a hash algorithm depends on a secret key, it is called a MAC. To do this, we just
replace the known IV with a secret shared key.
	- Example: f is AES, so t = m = 128. Break the message into 128 bit blocks. If the message length is not a multiple of 128 bits then add 0’s to the end (padding) so that it is. The key for the first AES is the IV. The key for the second AES is the output of the first AES and so on. The final output is the hash of the message. This is not a secure hash function but it’s OK as a MAC.

* **Hash-based message authentication code (HMAC)**: It's an originator validation, it validates the source of a message by incorporating some form of private key into the hash operation. Same weakness of any shared key system.

* **Bait-and-switch attack**: weakness found in an aging hash function. The attacker takes advantage of a weak hash function's tendency to generate collisions over certain ranges of input. By doing this, an attacker can create two inputs that generate the same value.


* **MD5 hash algorithm**: The function f takes two inputs: a 128 bit string and a 512 bi  strings and its output is a 128 bit strings. Let X be the 512 bit string. For MD5 we will call a 32 bit string a word. So X consists of 16 words. Let X[0] be the first word, X[1] be the next,..., X[15] be the last word.

* **SHA3**: chosen by NIST in 2012, it has the strongly collision free property. SHA-3 takes inputs of arbitrary length and gives output of length 256.


-----------

* **Internet security**: there are two main  protocols for providing security in the internet  (encryption and authentication): TLS and IPSec.

* **Transport Layer Security**: the process is called Secure Sockets Layer (SSL) and now being replaced by TLS.  RSA to agree on AES key (which is used to encrypt password for example).

* **Internet Protocol Security** (IPSec): a competitor of TLS, it is less efficient than TLS and it is used in VPN.

* **Timestamping**: If Alice signs a message, and later decides that she does not want that message to be signed then she can anonymously publish her private key and say that anyone could have done the signing. This is called repudiation. So if someone receives a signature from Alice, he or she can demand that Alice use a digital timestamping service.

* **Kerberos**: third part authentication protocol for insecure closed systems. It is used to prove someone's identity (authentication) in a secure manner without a public key crypto. An authentication server  authenticates the client identity with a ticket granting service for a service.

* **Salt**: random value added to a message so that two messages don't generate the same hash value. It must not be duplicated between messages. It must be stored in addition to the hash so that the digest can be reconstructed. It must be protected. A salt of 23 buts increase of the password pre-computation dictionary by 4 billions of time (2^32).

	- Salt is a string that is concatenated to a password. It should be different for each userid. It is public for non-SSL/TLS applications like KERBEROS and UNIX.

	-  If two people have the same password, they will not have the same hash. In Kerberos,  The authentication server keeps the hash secret, protected by a password known only to the authentication server.

	- Linux: in the password file, where there was once the salt and the hash of a salted password, there is now a *. A second hidden file called the shadow is the password file. It is encrypted using a password only known to the system admin. The shadow file contains userid, salt, hash(salt,password).

* **Rainbow tables**: example of how a lack of  salt value leaves password hashes vulnerable to pre-computation attacks.


---

* **Quantum Cryptography**: there are two ways of agreeing on a symmetric keys without presence: public key crypto or quantum crypto. It can work up to several kilometers. It can detect eavesdropping.
	- A photon has a polarization that can be measured on any basis in two-space. If you measure in the wrong basis, you get random results and disturbs future measurements.
	- Alice sends Bob a stream of photons. Each photon is randomly assigned a polarization in for direction (-1, 0, 1, 0).
	- Bob randomly picks a basis for each photon. Every time he chooses the right basis, he measure the polarization correctly, otherwise, he gets random.
	- Now Bob contact Alice in clear and tells the basis settings he made. Alice tells him which were correct. The others were thrown out.
	- When Bob correctly sets the basis, they both have the same polarization, which can be turned into 0 or 1.
	- On average, if Alice sends 2n bits, they end up with n bits. So to agree on 128 bit key, on average, Alice must send 256 bits.
	- To detect eavesdropping, Alice and Bob agree to check on some of the bits, which are randomly chosen by Alice.
	- Eve can perform a MITM attack and impersonate Alice and Bob for each other, so QC needs some authentication.


---
* **CryptoAnalysis**: there are three types:
	- **Ciphertext only attack**: enemy intercepted ciphertext but has no matching plaintext. The enemy is aware of the nature of the cryptosystem but does not have the key, or the enemy is not aware of the nature of the cryptosystem (not stable).
	- **Known plaintext attack**: enemy has some matched ciphertext/plaintext pairs.
	- **Chosen plaintext attack**: the enemy can choose the plaintext that she wants to put through the system.

---

## References

- [Crypto Intro](http://math.scu.edu/~eschaefe/book.pdf)
