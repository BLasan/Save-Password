#!/bin/bash

# echo -e "Welcome to Save Password Application\n";

# echo -e "----------------------------------------------\n";

# echo -e "Adding Python repository\n";

# sudo add-apt-repository ppa:deadsnakes/ppa

# echo -e "Updating!";

# sudo apt update

# echo -e "Installing python 3.6\n"

# sudo apt install python3.6

# cd save-password

# echo -e "Installing Requirements\n"

# pip3 install -r requirements.txt


echo -e "Creating Crontab file\n";

echo -e "User Name : $(whoami)"

read -p 'User Name: ' uservar

read -sp 'Password: ' password

echo -e "\n"

echo -e "Enter to Super User mode!\n"

if [[  -z "$PATH_TO_SCRIPT" ]]; then
    read -p 'Path To Run Script File: ' path
    export PATH_TO_SCRIPT="$path"
    sudo sh -c "echo export PATH_TO_SCRIPT=$PATH_TO_SCRIPT >> /home/$(whoami)/.bash_profile"
fi

export USER_NAME="$uservar"

export USER_PASSWORD="$password"

sudo sh -c "echo export USER_NAME=$USER_NAME >> /home/$(whoami)/.bash_profile"

sudo sh -c "echo export USER_PASSWORD=$USER_PASSWORD >> /home/$(whoami)/.bash_profile"

echo "$USER_NAME"

echo "$PATH_TO_SCRIPT"

sudo sh -c "echo export PATH_TO_SCRIPT=$PATH_TO_SCRIPT >> /home/$(whoami)/.bash_profile"

echo -e "---------------------------------------------";

echo -e "Create a crontab file\n";

export EDITOR=nano

crontab -e

echo -e "Create Link for run_script.sh file in home directory\n";

# sudo unlink /home/"$(whoami)"/run_script.sh

sudo ln -s "$PATH_TO_SCRIPT"/run_script.sh /home/"$(whoami)"/run_script.sh

echo "Done"
