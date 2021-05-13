# -*- coding:utf-8 _*-
from apps.kafka.models import KafkaBroker, KafkaCluster
from common.utils.common import build_fail_result, get_cc_info_by_ip, is_ip, str_trans_list


'''
@summary: 定义不同kafka任务参数处理模块：参数检测，参数提取
@usage:
TASK_TYPE = (
        (0, "其他"),
        (1, "hdfs集群部署"),
        (2, "yarn集群部署"),
        (3, "集群部署"),
        (4, "datanode节点扩容"),
        (5, "datanode节点缩容"),
        (6, "nodemanager节点扩容"),
        (7, "nodemanager节点缩容"),
        (8, "多磁盘扩容"),
        (9, "集群录入检测"),
        (10, "集群扩容"),
        (11, "集群缩容"),
    )
'''


def check_kafka_add_ip(bk_username, ip_list, app_id, app):
    """
       提取公共检测ip的代码来封装，减少重复代码
       @param bk_username: ip在配置平台检测需要的用户名称 参数类型： str
       @param ip_list: 任务中新加的带检测ip列表，参数类型: list
       @param app_id: ip在配置平台检测需要的业务ID 参数类型： int
       @param app: ip的配置平台检测需要的业务名称 参数类型： str
    """
    for node_ip in ip_list:
        if not is_ip(node_ip):
            # 存在非法ip
            return build_fail_result(f"存在非法IP:{node_ip}")
        if KafkaBroker.objects.filter(ip=node_ip).exists():
            # ip已录入平台
            return build_fail_result(f"平台检测到存在该IP:{node_ip}")

        if get_cc_info_by_ip(bk_username=bk_username, app_id=app_id, ip=node_ip)['data']['count'] == 0:
            # 节点不属于对应业务，异常退出
            return build_fail_result(f"节点不属于对应业务{app}，请自查:{node_ip}")

    return None


def retrieval_kafka_deploy_param(post_data, bk_username):
    """
        提取kafka部署参数方法
        @param post_data: 前端post传入的参数信息 参数类型：dict
        @param bk_username: 前端传入的用户名称 参数类型：str
    """

    cluster_name = post_data.get('cluster_name')
    app = post_data.get('app')
    app_id = post_data.get('app_id')
    version = post_data.get('version')
    broker_list = str_trans_list(post_data.get('broker_list'))
    broker_str = ",".join(broker_list)
    description = post_data.get('description')

    if KafkaCluster.objects.filter(cluster_name=cluster_name).exists():
        return build_fail_result(f"集群名称已存在：{cluster_name}")

    if len(broker_list) < 3:
        return build_fail_result(f"集群数量少于3，不满足最小集群标准。目前节点数量：{len(broker_list)}")

    check_result = check_kafka_add_ip(bk_username, broker_list, app_id, app)
    if check_result:
        # 检测结果不为空，证明检测不通过
        return check_result

    return {
        "code": 1,
        "data": {
            "app_id": int(app_id),
            "app": app,
            "add_type": 1,
            "cluster_name": cluster_name,
            "version": version,
            "target_ips": broker_list,
            "broker_str": broker_str,
            "description": description,
            "bk_username": bk_username,
            "task_type": 3
        },
    }


def retrieval_kafka_add_node_param(post_data, bk_username):
    """
       提取kafka broker节点扩容参数方法
       @param post_data: 前端post传入的参数信息 参数类型：dict
       @param bk_username: 前端传入的用户名称 参数类型：str
    """
    target_ips = str_trans_list(post_data.get('ips'))
    cluster_name = post_data.get('cluster_name')
    cluster = KafkaCluster.objects.get(cluster_name=cluster_name)
    cluster_id = cluster.id
    version = cluster.version
    zk_list = cluster.zk_list
    app_id = cluster.app_id
    app = cluster.app

    check_result = check_kafka_add_ip(bk_username, target_ips, app_id, app)
    if check_result:
        # 检测结果不为空，证明检测不通过
        return check_result

    return {
        "code": 1,
        "data": {
            "cluster_id": cluster_id,
            "app_id": int(app_id),
            "cluster_name": cluster_name,
            "version": version,
            "target_ips": target_ips,
            "broker_str": zk_list,
            "bk_username": bk_username,
            "task_type": 10
        },
    }
