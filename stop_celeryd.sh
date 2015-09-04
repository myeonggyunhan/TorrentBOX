#!/bin/bash
celeryd_pids=`ps -ef | grep "celeryd"  | awk -F" " '{ print $2 }'`
kill -9 $celeryd_pids
