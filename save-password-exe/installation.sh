#!/bin/bash

echo -e "Welcome to Save Password Application\n";

echo -e "----------------------------------------------\n";

echo -e "Adding Python repository\n";

sudo add-apt-repository ppa:deadsnakes/ppa

echo -e "Updating!";

sudo apt update

echo -e "Installing python 3.6\n"

sudo apt install python3.6

cd save-password

echo -e "Installing Requirements\n"

pip3 install -r requirements.txt

echo -e "Creating Crontab file\n";

user = $(whoami)

echo -e "User Name : $user"

read -p 'User Name: ' uservar

read -sp 'Password: ' password

export USER_NAME="$uservar"

export USER_PASSWORD="$password"

echo "$USER_NAME"

echo -e "---------------------------------------------";

echo -e "Create a crontab file\n";

export EDITOR=nano

crontab -e

echo -e "Create Link for run_script.sh file in home directory\n";

ln -s run_script.sh /home/run_script.sh

echo "Done"
