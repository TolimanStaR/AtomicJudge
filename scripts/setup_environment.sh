#!/bin/bash

PASSWORD="password for user root in container"
export PASSWORD


echo "$PASSWORD" | sudo -S apt update

gcc -v

# shellcheck disable=SC2034
res=$?

if [ -$res -ne "0" ]; then
  echo "$PASSWORD" | sudo -S apt install gcc
fi

g++ -v

# shellcheck disable=SC2034
res=$?

if [ -$res -ne "0" ]; then
  echo "$PASSWORD" | sudo -S apt install g++
fi

python2 --version

# shellcheck disable=SC2034
res=$?

if [ -$res -ne "0" ]; then
  echo "$PASSWORD" | sudo -S apt install python2
fi

python3 --version

# shellcheck disable=SC2034
res=$?

if [ -$res -ne "0" ]; then
  echo "$PASSWORD" | sudo -S apt install python3
fi

javac -version

# shellcheck disable=SC2034
res=$?

if [ -$res -ne "0" ]; then
  echo "$PASSWORD" | sudo -S apt install default-jre;
  echo "$PASSWORD" | sudo -S apt install default-jdk
fi
