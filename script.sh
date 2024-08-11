start=9001
end=10000

for i in $(seq $start 200 $end)
do
    python3 scrapper_rodrigo.py $i $((i+199)) &
done