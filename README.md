# Passman
A simple password manager written in python.

## Installation:

Clone the repository with:
```bash

git clone https://github.com/Hnobles12/passman.git

```
Enter the src/ directory and install:
```bash
cd passman
sudo pip3 install ./src
```
Copy the default config file:
```bash
cp ./doc/example.toml ~/.config/passman.toml
```

## Usage:

Run the command `passman --help` to see options. Passman will ask for a master password which will allow for the user to decrypt the passwords and data stored in the passman database. The password must be one that can be easily remembered as there is no recovery. To add new services to the database, use the flag `-n` and passman will prompt you to enter the information for the new service. The service name is what makes the service searchable so make sure it is clear and easily remembered.


