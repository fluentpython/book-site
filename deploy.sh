#!/bin/bash
hugo
rsync -avz --delete public/ dh_ggsv7h@fluentpython.com:~/fluentpython.com/public
