#!/bin/bash
# Rebecca Nishide, 9/21/2020
# contact: rnnishide@gmail.com

echo "    Current paths:"
echo $PATH

unzip chromedriver*.zip

sudo mv chromedriver /usr/local/bin

echo "chromedriver moved to /usr/local/bin"
echo "Restart shell to use chromedriver"
