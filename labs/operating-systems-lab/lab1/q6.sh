#!/bin/bash
cd ~/Desktop
mkdir Folder1 Folder2                                   # mkdir -p if they may already exist
echo "INDIAN INSTITUTE OF INFORMATION TECHNOLOGY" > Folder1/file.txt
cd Folder2
grep "INDIAN" ../Folder1/file.txt                       # search from Folder2 (relative path)
cat ../Folder1/file.txt                                 # display complete contents
