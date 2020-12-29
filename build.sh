PID=""
PID=$(ps -ef | grep python | grep app.py | awk '{ print $2 }')

if [ -z "$PID" ]
then
    echo "running python server not found "
else
    #echo kill $PID
    kill -9  $PID
    echo "killed "+$PID+""
fi

PID=$(ps -ef | grep python  | grep app.py | awk '{ print $2 }')
if [ -z "$PID" ]
then
   python app.py >> log.log 2>&1 &
   echo "Started python server"
fi
