# xv6 Installation

## 1. Download xv6

Download `xv6-public.tgz` from:

https://www.cse.iitb.ac.in/~mythili/os/xv6.html

**First check your Ubuntu version** (`lsb_release -a`).
If it is the 2024 release (Ubuntu 24.04), add the following flags to the `CFLAGS =` line in the `Makefile`:

```make
-Wno-array-bounds -Wno-infinite-recursion
```

## 2. Untar the xv6 code tarball

```bash
tar -zxvf xv6-public.tgz
```

## 3. Compile xv6

Go to the uncompressed xv6 folder and compile:

```bash
cd xv6-public
make clean
make
```

## 4. Run xv6 inside QEMU

```bash
make qemu
```

(To quit QEMU: press `Ctrl-a`, then `x`.)

## Basic operations (utilities lab)

Follow this link for implementing basic operations:

https://pdos.csail.mit.edu/6.828/2024/labs/util.html
