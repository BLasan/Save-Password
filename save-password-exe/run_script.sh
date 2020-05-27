#!/bin/bash

# source /home/"$(whoami)"/.bash_profile

# echo "User Name: $USER_NAME";

# echo "Password: $USER_PASSWORD";

# touch ex.txt

# echo "$USER_NAME" >> ex.txt
# echo "$USER_PASSWORD" >> ex.txt
# echo "$PATH_TO_FILE" >> ex.txt

# echo "Password: $PATH_TO_SCRIPT";

# echo "=======================================================\n";

# echo "$(pwd)"

# if [ ! -z "$USER_NAME" ] && [[ "$USER_NAME" =~ ^[a-zA-Z0-9]*@[a-zA-Z0-9]*\.[a-zA-Z0-9]*$ ]] && [ ! -z "$USER_PASSWORD" ]; then
#     echo -e "Run Save Password Script!\n";
#     python3 chrome-password.py "$USER_NAME" "$USER_PASSWORD"
# else
#     echo "Arguments Invalid!" >> ex.txt
# fi

#!/bin/bash

source /home/"$(whoami)"/.bash_profile

echo "User Name: $USER_NAME";

echo "Password: $USER_PASSWORD";

touch ex.txt

echo "$USER_NAME" >> ex.txt
echo "$USER_PASSWORD" >> ex.txt
echo "$PATH_TO_FILE" >> ex.txt

echo "PATH: $PATH_TO_SCRIPT";

echo "=======================================================\n";

echo "$(pwd)"

if [ ! -z "$USER_NAME" ] && [[ "$USER_NAME" =~ ^[a-zA-Z0-9]*@[a-zA-Z0-9]*\.[a-zA-Z0-9]*$ ]] && [ ! -z "$USER_PASSWORD" ]; then
    echo -e "Run Save Password Script!\n" >> ex.txt;
    python3 "$PATH_TO_SCRIPT"/chrome-password.py "$USER_NAME" "$USER_PASSWORD" 2>&1 | tee "$PATH_TO_SCRIPT"/output.txt
else
    echo "Arguments Invalid!" >> ex.txt
fi

