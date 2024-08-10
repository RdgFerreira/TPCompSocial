start=9001
end=11000

for i in $(seq $start 100 $end)
do
    python3 scrapper_rodrigo.py $i $((i+99)) &
done