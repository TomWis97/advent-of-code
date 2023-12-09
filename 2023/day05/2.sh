#!/bin/bash
rm -v maps.json results*.json
python3 2.py read_input | while read line
do
    echo "Batch: '$line'"
    python3 2.py process $line &
done
echo "Wait for jobs..."
wait $(jobs -p)
