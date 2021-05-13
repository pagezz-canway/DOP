# -*- coding: utf-8 -*-
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action

from apps.kafka.flow.kafka_flow import add_node_flow, deploy_cluster_flow
from apps.kafka.models import KafkaBroker, KafkaCluster, Topic
from apps.kafka.parameter import retrieval_kafka_add_node_param, retrieval_kafka_deploy_param
from apps.kafka.serializers import KafkaBrokerSerializers, KafkaClusterSerializers, TopicSerializers
from apps.kafka.topic_ops import create_topic
from blueapps.utils.logger import logger
from common.utils.common import get_cc_app_id_by_user
from common.utils.custom_auth import CsrfExemptSessionAuthentication
from common.utils.utils import ApiMixin


class KafkaClusterViewSet(ApiMixin, viewsets.ModelViewSet):
    """
        kafka集群表视图
    """
    serializer_class = KafkaClusterSerializers
    filter_fields = ('cluster_name',)
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)

    def get_queryset(self):
        """
          重写get_queryset方法，根据用户的业务权限来输出对应记录，用户隔离
        """
        app_id_list = get_cc_app_id_by_user()
        return KafkaCluster.objects.filter(app_id__in=app_id_list).order_by("-create_time")

    @action(methods=['post'], detail=False)
    def create_cluster(self, request, *args, **kwargs):
        """
           POST /kafka/create_cluster  kafka集群创建
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_kafka_deploy_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            deploy_parameter = info['data']
            # 部署任务，检测是否正常
            if deploy_cluster_flow(deploy_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "部署任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "部署任务失败"})

        except Exception as e:
            logger.error(f'create pipeline failed:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})

    @action(methods=['post'], detail=False)
    def add_broker(self, request):
        """
           POST /kafka/add_node  kafka broker节点创建
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_kafka_add_node_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            add_node_parameter = info['data']
            # 部署任务，检测是否正常
            if add_node_flow(add_node_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "扩容任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "扩容任务失败"})

        except Exception as e:
            logger.error(f'create pipeline failed:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})


class KafkaBrokerViewSet(ApiMixin, viewsets.ModelViewSet):
    """
        kafka broker信息表视图
    """
    queryset = KafkaBroker.objects.all()
    serializer_class = KafkaBrokerSerializers
    filter_fields = ('cluster_name',)
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)


class KafkaTopicViewSet(ApiMixin, viewsets.ModelViewSet):
    """
        kafka topic信息表视图
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializers
    filter_fields = ('cluster_name',)
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)

    @action(methods=['post'], detail=False)
    def create_topic(self, request, *args, **kwargs):
        """
           /kafka/create_topic 创建kafka topic信息
        """
        try:
            post_data = request.data
            cluster_name = post_data.get('cluster_name')
            topic = post_data.get('topic')
            bk_username = request.user.username
            if create_topic(bk_username, cluster_name, topic):
                return JsonResponse({'result': True, 'code': 0, 'data': [], 'message': 'topic创建成功'})
            else:
                return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': 'topic创建失败'})
        except Exception as e:
            logger.error(f'create failed:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})
