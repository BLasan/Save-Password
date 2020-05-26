#!/bin/bash

echo "User Name: $USER_NAME";

echo "Password: $USER_PASSWORD";

echo "=======================================================\n";

if [ ! -z "$USER_NAME" ] && [[ "$USER_NAME" =~ ^[a-zA-Z0-9]*@[a-zA-Z0-9]*\.[a-zA-Z0-9]*$ ]] && [ ! -z "$USER_PASSWORD" ]; then
    echo -e "Run Save Password Script!\n";
    python3 chrome-password.py "$USER_NAME" "$USER_PASSWORD"
else
    echo "Arguments Invalid!"
fi
