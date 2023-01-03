## The Playground Shell
The `psh` is an interactive GUI written in the Python Programming Language meant to simulate `zsh`. `touch` multiple files, `cd` into different directories, and `echo` funny messages are all things you can do in the `psh` without accidently ruining your own personal machine.


## Documentation
The `psh` supports the following Unix-like operating system commands:
```c
ls    [file ... | directory ...]
echo  [>>] [string ...]
touch [file ...]
mkdir [directory ...]
cd    [directory]
cat   [file]
rm    [-r] [file ... | directories ...]
rmdir [directories ...]
```
The listed commands follow a behavior similar to the `zsh`.

## Installation
To start playing around with the `psh` simply clone this repository into your working directory and run the following command:
```
> python3 shell.py
```
