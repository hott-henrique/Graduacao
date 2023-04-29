while IFS= read -r LINE || [[ -n "$LINE" ]]; do
    echo "$LINE" \
        | grep -o --line-buffered "\([0-9]\+\):\|\([0-9]\+\.[0-9]\+$\)" \
        | paste -d '' - - \
        | sed --expression "s/:/,/g"
done

