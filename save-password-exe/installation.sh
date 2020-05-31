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

echo -e "User Name : $(whoami)"

echo -e "\n"

echo -e "Enter to Super User mode!\n"

echo "$USER_NAME"

echo "$USER_PASSWORD"

echo "$PATH_TO_SCRIPT"

if [[  -z "$PATH_TO_SCRIPT" ]]; then
    read -p 'Path To Run Script File: ' path
    export PATH_TO_SCRIPT="$path"
    sudo sh -c "echo export PATH_TO_SCRIPT=$PATH_TO_SCRIPT >> /home/$(whoami)/.bash_profile"
fi

if [[ -z "$USER_NAME" ]]; then
    read -p 'User Name: ' uservar
    export USER_NAME="$uservar"
    sudo sh -c "echo export USER_NAME=$USER_NAME >> /home/$(whoami)/.bash_profile"
fi

if [[ -z "$USER_PASSWORD" ]]; then
    read -sp 'Password: ' password
    export USER_PASSWORD="$password"
    sudo sh -c "echo export USER_PASSWORD=$USER_PASSWORD >> /home/$(whoami)/.bash_profile"
fi

sudo sh -c "echo export PATH_TO_SCRIPT=$PATH_TO_SCRIPT >> /home/$(whoami)/.bash_profile"

echo -e "---------------------------------------------";

echo -e "Create a crontab file\n";

export EDITOR=nano

crontab -e

echo -e "Create Link for run_script.sh file in home directory\n";

sudo unlink /home/"$(whoami)"/run_script.sh

sudo ln -s "$PATH_TO_SCRIPT"/run_script.sh /home/"$(whoami)"/run_script.sh

echo "Done"
