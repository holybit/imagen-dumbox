#!/bin/bash
set -e

trap 'kill -TERM $$' TERM

while true; do
    echo "running"
    sleep 60
done
