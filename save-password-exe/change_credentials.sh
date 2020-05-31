!#/bin/bash

echo -e "Open .bash-profile with gedit tool!\n"

echo -e "Change USER_NAME and USER_PASSWORD and FILE_PATH accurately\n"

sudo gedit /home/"$(whoami)"/.bash_profile

echo -e "Restarting Installation script\n"

source ./installation.sh