# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.db.models import F

from blueapps.utils.logger import logger
from common.utils.common import get_cc_info_by_ip


# Create your models here.


class KafkaCluster(models.Model):
    """
    Kafka集群信息
    """

    DELETE_STATUS = ((0, "未删除"), (1, "已删除"))
    ADD_TYPE = ((0, "平台录入"), (1, "平台新建"))

    CLUSTER_STATUS = (
        (0, "已下线"),
        (1, "部署中"),
        (2, "部署异常"),
        (3, "上线中"),
        (4, "集群变更中"),
        (5, "集群异常"),
        (6, "集群录入中"),
        (7, "集群录入异常"),
        (99, "未知状态"),
    )

    cluster_name = models.CharField('集群名称', max_length=100, default='', unique=True)
    cluster_status = models.IntegerField(choices=CLUSTER_STATUS, default=3, verbose_name="集群状态")
    app = models.CharField('业务', max_length=100, default='')
    app_id = models.IntegerField('业务id', default=0)
    zk_list = models.CharField('zookeeper列表', max_length=100, default='')
    zk_port = models.IntegerField('zookeeper集群访问端口', default=2181)
    broker_cnt = models.IntegerField('broker数量', default=0)
    version = models.CharField('版本号', max_length=100, default='')
    create_time = models.DateTimeField("创建时间", auto_now_add=True, blank=True)
    description = models.CharField('集群描述', max_length=100, default='')
    created_by = models.CharField("创建人", max_length=256, default="system")
    is_delete = models.IntegerField("删除标志", choices=DELETE_STATUS, default=0)
    add_type = models.IntegerField('集群创建方式', choices=ADD_TYPE, default=1)

    class Meta:
        db_table = "t_kafka_cluster_info"
        verbose_name = "kafka集群信息"
        verbose_name_plural = "kafka集群信息"
        index_together = ('app_id', 'create_time')

    def __unicode__(self):
        return '%d: %s' % (self.pk, self.cluster_name)


class Topic(models.Model):
    """
    Topic信息
    """

    cluster_name = models.CharField('所属集群', max_length=50, default='')
    topic = models.CharField('topic', max_length=50, default='')
    create_by = models.CharField('topic创建人', max_length=50, default='')
    create_time = models.DateTimeField("创建时间", auto_now_add=True, blank=True)

    class Meta:
        db_table = "t_kafka_topic_detail"
        verbose_name = "kafka集群topic信息"
        verbose_name_plural = "kafka集群topic信息"
        unique_together = ('cluster_name', 'topic')


class KafkaBroker(models.Model):
    """
    Kafka broker信息
    """

    app_id = models.IntegerField('业务id', default=0)
    cluster_name = models.CharField('所属集群', max_length=50, default='', db_index=True)
    ip = models.CharField('节点ip', max_length=50, default='', unique=True)
    version = models.CharField('es版本', max_length=50)
    device_class = models.CharField('设备类型', max_length=50)
    hard_memo = models.CharField('硬件说明', max_length=50)

    class Meta:
        db_table = "t_kafka_broker_detail"
        verbose_name = "kafka集群broker信息"
        verbose_name_plural = "kafka集群broker信息"


def insert_kafka_cluster(deploy_info):
    """
       部署kafka集群初始化数据库信息
       @param deploy_info: {
            "app_id": 业务id,
            "app": 业务名称,
            "add_type": 0/1,
            "cluster_name": 集群名称,
            "version": 集群版本,
            "target_ips": broker ip列表,
            "broker_str": zookeeper 集群信息,
            "description": 集群描述,
            "bk_username": 创建者,
            "task_type":
            }
    """
    try:
        # 绑定事务插入，保证事务的数据一致性
        with transaction.atomic():
            cluster = KafkaCluster.objects.create(
                cluster_name=deploy_info['cluster_name'],
                app=deploy_info['app'],
                app_id=deploy_info['app_id'],
                add_type=deploy_info['add_type'],
                zk_list=deploy_info['broker_str'],
                broker_cnt=len(deploy_info['target_ips']),
                version=deploy_info['version'],
                description=deploy_info['description'],
                created_by=deploy_info['bk_username'],
            )
            # 集群信息表插入后 插入broker信息
            for broker_ip in deploy_info['target_ips']:
                # 在配置平台获取IP的硬件信息
                res = get_cc_info_by_ip(deploy_info['bk_username'], deploy_info['app_id'], broker_ip)
                device_class = res['data']['info'][0].get('svr_device_class')
                hard_memo = res['data']['info'][0].get('hard_memo')

                KafkaBroker.objects.create(
                    app_id=deploy_info['app_id'],
                    cluster_name=deploy_info['cluster_name'],
                    ip=broker_ip,
                    version=deploy_info['version'],
                    device_class=device_class,
                    hard_memo=hard_memo,
                )
    except Exception as err:
        logger.error(f"集群数据插入发生异常：{str(err)}")
        return None

    return cluster.id


def update_kafka_cluster(cluster_id, update_data):
    """
       更新kafka cluster的数据
       @param cluster_id: 集群id
       @param update_data:更新数据
    """
    try:
        KafkaCluster.objects.filter(id=cluster_id).update(**update_data)
        return True

    except Exception as err:
        logger.error(f"集群数据更新发生异常{str(err)}")
        return False


def add_broker_node(add_info):
    """
       扩容后插入新的进程信息
       @param add_info:{
            "cluster_id": 集群id,
            "app_id": 业务id,
            "cluster_name": 集群名称,
            "version": 版本号,
            "target_ips": 扩容ip信list,
            "broker_str": zookeeper信息,
            "task_type":
            "bk_username": 操作者
       }
    """
    add_cnt = len(add_info['target_ips'])
    try:
        with transaction.atomic():
            KafkaCluster.objects.filter(id=add_info['cluster_id']).update(broker_cnt=F('broker_cnt') + add_cnt)
            for add_broker_ip in add_info['target_ips']:
                # 在配置平台获取IP的硬件信息
                res = get_cc_info_by_ip(add_info['bk_username'], add_info['app_id'], add_broker_ip)
                device_class = res['data']['info'][0].get('svr_device_class')
                hard_memo = res['data']['info'][0].get('hard_memo')

                KafkaBroker.objects.create(
                    app_id=add_info['app_id'],
                    cluster_name=add_info['cluster_name'],
                    ip=add_broker_ip,
                    version=add_info['version'],
                    device_class=device_class,
                    hard_memo=hard_memo,
                )
        return True

    except Exception as err:
        logger.error(f"新增节点插入发生异常: {str(err)}")
        return False
