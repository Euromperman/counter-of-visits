
#!/usr/bin/env bash


if [ -z "$1" ]; then
    echo "Error: There is no URL argument. Url argument should be written like this: ./healthcheck.sh http://localhost:8080"
    exit 1
fi

URL="$1/health"

for attempt in {1..5}; do

    status=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
    echo "[$(date)] Pokusaj $attempt/5 - HTTP $status"

    if [ "$status" = "200" ]; then
        exit 0
    fi

    if [ "$attempt" -lt 5 ]; then
        sleep 3
    fi
done

exit 1
