#!/bin/bash


#WAIT_COMMAND='[ $(curl --write-out %{http_code} --silent --output /dev/null http://elastic:9200/_cat/health?h=st) = 200 ]'
#WAIT_LOOPS=3
#WAIT_START_CMD="python -V"
#WAIT_SLEEP=2

echo $WAIT_COMMAND
echo $WAIT_START_CMD

is_ready() {
    eval "$WAIT_COMMAND"
}

# wait until is ready
i=0
while ! is_ready; do
    i=`expr $i + 1`
    if [ $i -ge $WAIT_LOOPS ]; then
        echo "$(date) - still not ready, giving up"
        exit 1
    fi
    echo "$(date) - waiting to be ready - $i"
    sleep $WAIT_SLEEP
done

#start the script
exec $WAIT_START_CMD
