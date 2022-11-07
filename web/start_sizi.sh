cd $(dirname $0) || exit 199

nohup python sizi_server.py 18020  >> run.log 2>&1 &
echo $! > run.pid
