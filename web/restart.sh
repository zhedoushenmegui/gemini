cd $(dirname $0) || exit 199

sh ./stop_sizi.sh && sh ./start_sizi.sh
exit 0;