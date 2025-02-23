# Reverse Engineering



* Objective: turn a x86 binary executable back into C source code.
* Understand how the compiler turns C into assembly code.
* Low-level OS structures and executable file format.

---
## Assembly 101

### Arithmetic Instructions

```
mov eax,2   ; eax = 2
mov ebx,3   ; ebx = 3
add eax,ebx ; eax = eax + ebx
sub ebx, 2  ; ebx = ebx - 2
```

### Accessing Memory

```
mox eax, [1234]     ; eax = *(int*)1234
mov ebx, 1234       ; ebx = 1234
mov eax, [ebx]      ; eax = *ebx
mov [ebx], eax      ; *ebx = eax
```

### Conditional Branches

```
cmp eax, 2  ; compare eax with 2
je label1   ; if(eax==2) goto label1
ja label2   ; if(eax>2) goto label2
jb label3   ; if(eax<2) goto label3
jbe label4  ; if(eax<=2) goto label4
jne label5  ; if(eax!=2) goto label5
jmp label6  ; unconditional goto label6
```

### Function calls

First calling a function:

```
call func   ; store return address on the stack and jump to func
```
The first operations is to save the return pointer:
```
pop esi     ; save esi
```

Right before leaving the function:
```
pop esi     ; restore esi
ret         ; read return address from the stack and jump to it
```
---


## Modern Compiler Architecture

**C code** --> Parsing --> **Intermediate representation** --> optimization --> **Low-level intermediate representation** --> register allocation --> **x86 assembly**

### High-level Optimizations



#### Inlining

For example, the function c:
```
int foo(int a, int b){
    return a+b
}
c = foo(a, b+1)
```
translates to  c = a+b+1


#### Loop unrolling

The loop:
```
for(i=0; i<2; i++){
    a[i]=0;
}
```
becomes
```
a[0]=0;
a[1]=0;
```

#### Loop-invariant code motion

The loop:
```
for (i = 0; i < 2; i++) {
    a[i] = p + q;
}
```
becomes:
```
temp = p + q;
for (i = 0; i < 2; i++) {
    a[i] = temp;
}
```

#### Common subexpression elimination

The variable attributions:
```
a = b + (z + 1)
p = q + (z + 1)
```

becomes
```
temp = z + 1
a = b + z
p = q + z
```

#### Constant folding and propagation
The assignments:
```
a = 3 + 5
b = a + 1
func(b)
```

Becomes:
```
func(9)
```

#### Dead code elimination

Delete unnecessary code:
```
a = 1
if (a < 0) {
printf(“ERROR!”)
}
```
to
```
a = 1
```

### Low-Level Optimizations

####  Strength reduction

Codes such as:
```
y = x * 2
y = x * 15
```

Becomes:
```
y = x + x
y = (x << 4) - x
```

#### Code block reordering

Codes such as :

```
if (a < 10) goto l1
printf(“ERROR”)
goto label2
l1:
    printf(“OK”)
l2:
    return;
```

Becomes:
```
if (a > 10) goto l1
printf(“OK”)
l2:
return
l1:
printf(“ERROR”)
goto l2
```


#### Register allocation

* Memory access is slower than registers.
* Try to fit as many as local variables as possible in registers.
* The mapping of local variables to stack  location and registers is not constant.

#### Instruction scheduling

Assembly code like:

```
mov eax, [esi]
add eax, 1
mov ebx, [edi]
add ebx, 1
```
Becomes:

```
mov eax, [esi]
mov ebx, [edi]
add eax, 1
add ebx, 1
```


---
## Tools Folder

- X86 Win32 Cheat sheet
- Intro X86
- base conversion
- Command line tricks


----
## Other Tools

- gdb
- IDA Pro
- Immunity Debugger
- OllyDbg
- Radare2
- nm
- objdump
- strace
- ILSpy (.NET)
- JD-GUI (Java)
- FFDec (Flash)
- dex2jar (Android)
- uncompyle2 (Python)
- unpackers, hex editors, compilers

---
## Encondings/ Binaries

```
file f1

ltrace bin

strings f1

base64 -d

xxd -r

nm

objcopy

binutils
```




---
## Online References

[Reverse Engineering, the Book]: http://beginners.re/
[Intel x86 Assembler Instruction Set Opcode Table]: http://sparksandflames.com/files/x86InstructionChart.html


---
## IDA

- Cheat sheet
- [IDA PRO](https://www.hex-rays.com/products/ida/support/download_freeware.shtml)



---
## gdb

- Commands and cheat sheet


```sh
$ gcc -ggdb -o <filename> <filename>.c

```

Starting with some commands:
```sh
$ gdb <program name> -x <command file>
```

For example:
```sh
$ cat command.txt
set disassembly-flavor intel
disas main
```

---
## objdump

Display information from object files: Where object file can be an intermediate file
created during compilation but before linking, or a fully linked executable

```sh
$ objdump -d  <bin>
```

----
## hexdump & xxd

For canonical hex & ASCII view:
```
$hexdump -C
```
----
## xxd
Make a hexdump or do the reverse:
```
xxd hello > hello.dump
xxd -r hello.dump > hello
```

----

# Talks

* [Patrick Wardle: Writing OS X Malware](https://vimeo.com/129435995).
