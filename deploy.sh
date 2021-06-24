#!/bin/bash
set -e  # exit when any command fails
hugo
rsync -avz --delete public/ dh_ggsv7h@fluentpython.com:~/fluentpython.com/public
