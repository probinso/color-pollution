#!/bin/bash

for i in 1 2 3 4;
do
    ./lamp-runner.py render input_$i.png .;
    mv output.png output_$i.png;
    convert input_$i.png output_$i.png +append $i.png;
    rm output_$i.png;
    exit;
done;
