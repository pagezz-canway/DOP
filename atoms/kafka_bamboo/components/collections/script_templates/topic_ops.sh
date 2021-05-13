#!/bin/bash

create_topic(){
   /data/kafkaenv/confluent/bin/kafka-topics  --bootstrap-server "$1" --create   --topic "$2"
   if [[ $? -eq 0 ]];then
      exit 0
   else
      exit 1
   fi
}

create_topic "$@"
