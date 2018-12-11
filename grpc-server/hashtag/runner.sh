#!/bin/bash

spark-submit cron_job.py > /dev/null
current_date_time="`date "+%Y-%m-%d %H:%M:%S"`";
echo $current_date_time;
