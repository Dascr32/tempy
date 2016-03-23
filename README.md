# TEMPy: a CLI for cleaning your Windows temp files

<br><p align="center">
  <img src="assets/tempy.png" alt="logo"/>
</p><br>


TEMPy is a **command line** utility intended for keeping your windows machine happy. Just run a command in your terminal every 10 seconds, week, year (please don't), or whenever you want and that's it your temp files are gone. Simple and fast.

TEMPy is written in python paired with the awesome [Click](http://click.pocoo.org/) and [PrettyTable](https://pypi.python.org/pypi/PrettyTable) libraries, so it's not windows only. You can run it on Linux or Mac, don't know why, but it's possible.

## Features
* Intuitive commands
* Temp directory content in tree view
* Temp directory content in ASCII tables (like MySQL or PostgreSQL shell)
* Temp directory size and total files
* Log file with detailed data of the performed deletions

## Installation
TEMPy can be installed with pip:
```
$ pip install tempy
```
Make sure pip and setuptools are up to date.

## Usage
The general command structure is:
```
$ tempy [COMMAND] [OPTION]
```
## Commands
| Command       | Option        | Description |
| ------------- |:-------------|:-------------|
| `delete`      | `--a`        | deletes all the files and directories |
| `delete`      | `--se`       | Shows all errors that were encountered in the last deletion |
| `analyze`     | `[none]`     | Shows the temp directory contents, number of files, and size.
| `tree`        | `[none]`     | Displays a tree view of the temp directory
| `log`         | `[none]`     | Opens the log file

## Examples

### Delete
```
$ tempy delete --a
```
```
Attempting deletion of: 5 elements..

Deleting dir: foo-dir
Deleting file: foo.log
Deleting file: code.log
Deleting file: app-log.log
Unable to delete
Deleting dir: data-temp
Unable to delete

Deletion complete!
* Deletions: 3
* Errors: 2
```
When this command is executed it automatically log the deletion report. Which can be accesed with `tempy log`.

The `Unable to delete` message means that the file/directory can't be deleted at the time, the reason can be that an other program is using it or something else. For error details use `tempy delete --se`

```
$ tempy delete --se
```
```
Errors encountered during the last deletion [03/22/16 12:10:22]:
Total: 2

* [WinError 32] The process cannot access the file because it is being used
by another process: 'C:\\Users\\User\\AppData\\Local\\Temp\\app-log.log'

* [WinError 5] Access denied: 'C:\\Users\\User\\AppData\\Local\\Temp\\data-temp
0\\additional.dll'
```

### Analyze
```
$ tempy analyze
```
```
$ tempy analyze
Analyzing directory: C:\Users\User\AppData\Local\Temp
+-----------------------------+-----------+
|             File            |    Size   |
+-----------------------------+-----------+
|         +~AF89898.tmp       | 193.0 KiB |
|         +~HJ89423.tmp       | 159.8 KiB |
|         +~KJ06734.tmp       | 192.4 KiB |
|         +~JF34535.tmp       | 159.2 KiB |
|    FOOAPIDebugLogFile.txt   |   0.0 B   |
|          PDFoo.log          |  3.8 KiB  |
|           FOORTS0           |  50.9 MiB |
|    fooapp_aoGNWKTfScJBMLT   |  16.0 KiB |
|    fooapp_lweTvWVQs433G8I   |  2.0 KiB  |
|         glufoo.log          |  138.0 B  |
|         glufoo1.log         |  1.0 MiB  |
|        foorpdata_user       |   0.0 B   |
|         fooelib.log         |  4.8 KiB  |
+-----------------------------+-----------+
* Files/Dirs: 13
* Size: 52.7 MiB
```
### Tree
```
$ tempy tree
```
```
Directory tree for: C:\Users\Daniel\AppData\Local\Temp
.
+-- foorpdata_user
|       +-- 7164
+-- FOORTS0
|       +-- foo.dll
|       +-- foo.dll.md5
|       +-- fooapp.exe
|       +-- fooapp.exe.md5
|       ....
+-- +~AF89898.tmp
+-- +~HJ89423.tmp
+-- +~HJ89423.tmp
+-- +~JF34535.tmp
+-- fooapp_aoGNWKTfScJBMLT
+-- fooapp_lweTvWVQs433G8I
+-- FOOAPIDebugLogFile.txt
+-- glufoo.log
+-- glufoo1.log
+-- fooelib.log
+-- PDFoo.log
```
### Log
```
$ tempy log
```
Opens your default editor with the log content:
```
##### Clean up performed at: 03/22/16 13:15:43#####


==== Directory contents on delete ====

+-----------------------------+-----------+
|             File            |    Size   |
+-----------------------------+-----------+
|         +~AF89898.tmp       | 193.0 KiB |
|         +~HJ89423.tmp       | 159.8 KiB |
|         +~KJ06734.tmp       | 192.4 KiB |
|         +~JF34535.tmp       | 159.2 KiB |
|    FOOAPIDebugLogFile.txt   |   0.0 B   |
|          PDFoo.log          |  3.8 KiB  |
|           FOORTS0           |  50.9 MiB |
|    fooapp_aoGNWKTfScJBMLT   |  16.0 KiB |
|    fooapp_lweTvWVQs433G8I   |  2.0 KiB  |
|         glufoo.log          |  138.0 B  |
|         glufoo1.log         |  1.0 MiB  |
|        foorpdata_user       |   0.0 B   |
|         fooelib.log         |  4.8 KiB  |
+-----------------------------+-----------+
=> Files/Dirs: 13
=> Size: 52.7 MiB

==== Deleted Files/Dirs ====

+-------------+---------+
|     File    |   Size  |
+-------------+---------+
|  glufoo.log | 318.0 B |
+-------------+---------+

=> Clean up size: 318.0 B
=> Deletions: 1
=> Errors: 12
```

## Authors
[Daniel Aguilar S](https://twitter.com/dasgaskl)

## License
See [LICENSE](https://github.com/Dascr32/tempy/blob/master/LICENSE)
