# Library-Management-System
A program written using python to store and retrieve data about school library.

# Installation
To install, first we need to install the libraries:
```sh
sudo apt update
sudo apt install python3-pip -y
pip3 install PyQt5
pip3 install openpyxl
```
Then clone this repo and run library:

```sh 
git clone https://github.com/ghss-vazhakkad/Library-Management-System
./library
```

If you want to install to system:
```sh
sudo desktop-file-install ~/Desktop/Library.desktop
```

# Build notes
## 2 Octobar 2023
* Fixed some bugs
* Added support for editing members
* Created a new menu to report books and members
* Started a new sub project for v2

## 16 August 2023
* Continuous addition also added to member list.
* Last incrimented id will be loaded on each id text view

## 13 August 2023
* Added supports for continous addition of books
* Made books list hidden after login

## 5 July 2023
* Added splash screen
* Changed the action of modify buttonb to login button in splash
* Changed main window to maximized by default

## 4 July 2023
* Added function to delete book
* Added function to edit book
* Now we can remove members
## 3 July 2023
* Added function to issue book by selecting both book and member.
* Made all windows fixed to maintain stability.
* Added a desktop file to open app remotely.
* Added a new icon.
* Added reserve option
* Added book and member search bars
* Disabled unused menu items
* It checks whether book is issued or not
## 2 July 2023
* Added window to add members.
* The add member window writes information to excel file.
* A new excel file for storing lis of members is added with columns id, name and status.
## 27 June 2023
* Added book entry form and made it fully working.
* Made book list view lists book names from xlsx file.
* Fixed color errors in login window.