# ArchiveGuardian

![Logo](https://github.com/karlh001/archiveguardian/blob/main/logos/archive_guardian_logo_web_low_res.jpg?raw=true)

## About 

Archive Guardian (AG) is a light-weight python command line utility designed to check file (object) integrity within a directory structure. The hash of the object is stored with the object to check next time the program is run. The meta data file keeps the name of the object plus the extension [.aghash0](https://github.com/karlh001/archiveguardian/wiki/aghash0-Extension).  

It is best used for static objects, such as pictures, archived documents and audio. An excellent use case is on hard drives infrequently accessed as a backup or archive disk. Another use is for checking cloud integrity: run the command, then upload objects with hash file to the cloud to ensure nothing has changed should you need to restore the objects.

After the hash has been produced, further execution of the program will result in the object being hashed and check against the existing hash. Best way to test is run the program, make a chance to the object and run again to see the failed output. 

Run [periodically](https://github.com/karlh001/archiveguardian/wiki/Schedule-Run) to check the integrity of your static archive or backup.  

## Requirements

Runs on Linux x64. [Click here](https://github.com/karlh001/archiveguardian/wiki/OS-Tested) for versions tested on.

5.1 MB disk space.

## How it works

Each object is checked against a known hash. If the object has not been seen by AG yet, a meta data hash object will be created next to it. Further running of the script will result in the object being checked against the hash. Some objects change, you know which are corrupted and need restoring for backup. Many integrity fails informs you that your media is damaged, such as faulted hard drive.  


#### Objects Before Running

![Before](https://github.com/karlh001/www-public/blob/main/Projects/ArchiveGuardian/pasted_image.png?raw=true)

#### Objects After Running

![After](https://github.com/karlh001/www-public/blob/main/Projects/ArchiveGuardian/pasted_image001.png?raw=true)

As you can see, a small text file will be created to store the object's metadata. This hash file is then used to check the object's integrity at a later date. It contains date process, hash, object path, size and program version.  


## What's a hash?  

The object (such as picture file, video file, document) is put through a mathematical formula to return a unique code for each object. It's unlikely two different objects will contain the same code. This is why it's a great method to check objects have not been changed. For example, if bit rot occurs, a single bit may change from a 1 to a 0 or vice versa which may not make much difference to a text file, but completely change a picture or damage a video.  

AG used SHA-256 algorithm to generate hashes. For example the word "ArchiveGuardian" run through SHA-256 will become: 5ed67e6e88e9641c9660f6398c66410e0c9042a6a7e20eb831cd55ab97779a8d. If I change the n to a m ("ArchiveGuardiam") the hash changes drastically to: fdc1c8b8ca1ff406180c2315f4c3c200e83fd0d1ac960ad5580ff46a65678679 

## Download

For quick set-up, simply download the file named "ag" (linux) or "ag.exe" for Windows.

## Operating Systems

### Windows

For Windows, download ag.exe and follow this [post](https://github.com/karlh001/archiveguardian/wiki/AG-on-Windows).

Using POWERSHELL or CMD (Win+R, type 'cmd' hit enter) type the full path to execute the program. If you double-click the icon the console closes straight away.

> C:\Users\Me\ag.exe -d C:\Users\Me\Pictures\

Your anti-malware or anti-virus scanner may block these execuable file. You will need to allow AG before running.

### Linux

For Linux, download "ag". Due to many different varients of Linux, if this does not work, try the ag.py in the /src directory using python but [read me](https://github.com/karlh001/archiveguardian/wiki/ag.py-File) first. 

Download and unpack the archive. Copy 'ag' to your usr bin for easy use on the command line. 

> sudo cp ag /usr/bin/ag

Make executable

> sudo chmod +x /usr/bin/ag

Alternatively, if you want to run directly from directory:

> ./ag

Open the terminal and type: 
 
> ag

If you see an output it works. Read the "Run" section. If not, make sure you are in the same directory. If you are unable to run ag on your system, and have python3 installed, try running [ag.py](https://github.com/karlh001/archiveguardian/wiki/ag.py-File) from source code.

### MAC OS

No complied binary for Mac OSX as I do not have access to the operating system. 

## Run Commands

To scan your first directory add the -d flag followed by your path.  

> ag -d /home/Pictures/ 

Type 'y' to confirm the input directory 

> Do you want to run on directory? /home/Pictures/ (y or n): 
 
## Failed Hashes 

When the program finds a hash mismatch, the following output will occur: 

> Hash Error: /path/to/the/file/picture001.jpg 

This means that the object has changed. If you did not make any changes, it's likely the object has become corrupted.

This tools does not negate the need for a backup. You should always at least follow 3-2-1 backup rule. If you find a corrupted object, simply replace the object(s) from backup and run the program again.  

## Process 

AG will check every object in the directory structure, if no hash file present, the object will undergo hashing and an output file produced in the JSON format. Please do not edit this file, or it may result in failed hash checking.  

The object is opened 64MB increments to preserve RAM should you try to hash a 5 GB file.  

AG will not attempt to hash zero byte objects. Minimum file object is 1 byte and no theoretical maximum size. AG has been tested on object sizes up to 5 GB. 

## Logging

AG does not yet have built-in logging. However you can add > with log location to achive this

> ag -d /path/to/files/ -s yes > /dir/to/log.log

## Run on schudule

From version 1.1 you can now run on schedule. use the -s flag followed by yes

> ag -d /path/to/files/ -s yes

Adding -s yes will skip the user prompt.

## What's next? 

AG is still actively developed. Now that the core function is stable, I am looking to add new features and possibility of GUI. Feedback is important to help direct the project.  

## Wiki

More details about AG found [here](https://github.com/karlh001/archiveguardian/wiki) on the GitHub Wiki.

## Contact 

ag@karlhunter.co.uk 

## Bugs 

Report using GitHub. [Click here](https://github.com/karlh001/archiveguardian/issues)

## License

[MIT](https://choosealicense.com/licenses/mit/)
