#!/bin/bash
rm -v maps.json results*.json
jid=1
python3 2.py read_input | while read line
do
    echo "Batch: '$line'"
    python3 2.py process $line $jid &
    jid=$((jid+1))
done
echo "Wait for jobs..."
wait $(jobs -p)
