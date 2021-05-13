# -*- coding: utf-8 -*-
from common.utils.bamboo_flow import BambooFlow


"""
内部定义的db组件id db_type:
    (1, "ES"),
    (2, "Hadoop"),
    (3, "Kafka")
内部定义的任务流程id task_type:
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
    (11, "集群缩容")
"""


def deploy_cluster_flow(deploy_info):
    """
       定义kafka集群部署流程(串行流程)
       @param deploy_info: 部署参数 参数类型:dict
    """
    kafka_deploy_bamboo_flow = BambooFlow(db_type=3, param_info=deploy_info)
    if not kafka_deploy_bamboo_flow.check_param() or not kafka_deploy_bamboo_flow.create_record_detail(task_type=3):
        # 存储任务记录失败，立即退出
        return False
    kafka_deploy_bamboo_flow.add_act(act_name="分发文件", act_component_code="kafka_push_pkg_action")
    kafka_deploy_bamboo_flow.add_act(act_name="部署Kafka集群", act_component_code="install_kafka_action")
    if not kafka_deploy_bamboo_flow.build_bamboo():
        # 返回false证明建立流程任务失败，异常退出
        return False

    return True


def add_node_flow(add_info):
    """
       定义kafka扩容流程(串行流程)
       @param add_info: 扩容流程 参数类型:dict
    """
    kafka_add_node_bamboo_flow = BambooFlow(db_type=3, param_info=add_info)
    if not kafka_add_node_bamboo_flow.create_record_detail(task_type=10):
        # 存储任务记录失败，立即退出
        return False
    kafka_add_node_bamboo_flow.add_act(act_name="分发文件", act_component_code="kafka_push_pkg_action")
    kafka_add_node_bamboo_flow.add_act(act_name="扩容broker节点", act_component_code="install_kafka_action")
    if not kafka_add_node_bamboo_flow.build_bamboo():
        # 返回false证明建立流程任务失败，异常退出
        return False

    return True
