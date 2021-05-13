# -*- coding:utf-8 _*-
import os

from apps.kafka.models import KafkaBroker, KafkaCluster, Topic
from blueapps.utils.logger import logger
from common.utils.common import get_job_ip_list, get_script, get_script_param
from common.utils.job_sdk import JobExecutor
from config import BASE_DIR


ATOM_DIR = os.path.join(BASE_DIR, 'atoms')

'''
@summary: 定义操作kafka topic 的管理操作
@usage:
'''


def create_topic(bk_username, cluster_name, topic_name):
    """
       定义创建topic方法，属于同步任务
    """
    if not topic_name:
        logger.error("传入的topic名称为空，请检查")
        return False
    app_id = KafkaCluster.objects.get(cluster_name=cluster_name).app_id
    broker_ip = KafkaBroker.objects.filter(cluster_name=cluster_name).values('ip')[0]['ip']
    broker_url = broker_ip + ":9092"

    client = JobExecutor(bk_username, [broker_ip])
    result, message = client.fast_execute_script({
        "bk_biz_id": app_id,
        "script_content": get_script('kafka_bamboo/components/collections/script_templates/topic_ops.sh'),
        "script_param": get_script_param([broker_url, topic_name]),
        "target_server": {"ip_list": get_job_ip_list([broker_ip])},
        "task_name": f"{cluster_name}集群创建topic:{topic_name}",
    })

    if result and result["data"].get("job_instance").get("status") == 3:
        # 任务执行成功，则更新数据信息，正确返回
        Topic.objects.create(cluster_name=cluster_name, topic=topic_name, create_by=bk_username)
        return True

    # 任务执行失败，则打印错误信息，并异常返回
    logger.error(message)
    return False
