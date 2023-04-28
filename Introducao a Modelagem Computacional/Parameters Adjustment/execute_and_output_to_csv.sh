
echo "Executing $1.py ..."

python3 "$1".py --experimental-data data.csv \
    | grep -o --line-buffered "\([0-9]\+\):\|\([0-9]\+\.[0-9]\+$\)" \
    | paste -d '' - - \
    > "$1"_output.csv

sed -i "s/:/,/g" "$1"_output.csv

echo "Finished executing $1.py"
