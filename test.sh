timeout 600 bash -c 'while true  # infinite loop
do
    curl -I https://great.dev.uktrade.digital/
    sleep 1  # short pause between requests
done'
