#!/bin/bash

# If timeout is not set then use 3600 seconds (1 hour) by default
TS_TIMEOUT="${TS_TIMEOUT:-3600}"

# Run infinity loop
while true; do
  python /app/twitterSays.py
  sleep $TS_TIMEOUT
done
