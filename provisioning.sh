#!/bin/bash

# Cause the script to exit on failure.
set -eo pipefail

# Activate the main virtual environment
. /venv/main/bin/activate

printf "\nGetting User Data\n"
vastai cloud copy --src /workspace/kohya_ss/ --dst /workspace/kohya_ss/ --transfer "Cloud To Instance" --connection $VAST_CONNECTION_ID --api-key $VAST_API_KEY --instance ${VAST_CONTAINERLABEL:2}
echo "vastai cloud copy --src /workspace/kohya_ss/ --dst /workspace/kohya_ss/ --transfer \"Instance to Cloud\" --connection $VAST_CONNECTION_ID --api-key $VAST_API_KEY --instance ${VAST_CONTAINERLABEL:2} --update" > /workspace/cronjob.sh
chmod +x /workspace/cronjob.sh
crontab -l > /tmp/current_cron 
echo "*/10 * * * * /workspace/cronjob.sh" >>  /tmp/current_cron
crontab /tmp/current_cron
printf "\nGot User Data\n"
