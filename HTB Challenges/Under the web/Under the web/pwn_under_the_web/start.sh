#!/bin/bash

while true 
do 
    php -S 0.0.0.0:8000 -dextension=./metadata_reader.so
done


