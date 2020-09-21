#!/bin/bash
# Rebecca Nishide, 09/08/2020 
# contact: rnnishide@gmail.com for key

# check for python3
PYTHON=$(which -a python3)
echo $PYTHON
if [[ "$PYTHON" == "" ]]
then
    echo "make sure python3 is installed properly"
    exit
fi

echo "python3 requirement satisfied"

# get libraries 
sudo pip3 install selenium
sudo pip3 install numpy
sudo pip3 install PIL

# clone from github with https 
# need to request access from me to use. 

git clone https://github.com/rnnisi/SiglentSDS1204X-E.git

print("Install chromedriver and configure path to use program.")
