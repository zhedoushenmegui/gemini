cd $(dirname $0) || exit 199

if [ -f run.pid ] ; then
        pid=$(cat run.pid)
    echo "kill ${pid}"
    kill -9 "${pid}"
    rm run.pid
fi