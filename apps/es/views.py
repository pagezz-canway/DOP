# -*- coding: utf-8 -*-
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action

from apps.es.flow.es_flow import add_node_flow, deploy_cluster_flow, input_cluster_flow, reduce_node_flow
from apps.es.models import EsCluster, EsNodeInfo, EsRule
from apps.es.parameter import (
    retrieval_es_add_node_param,
    retrieval_es_deploy_param,
    retrieval_es_input_param,
    retrieval_es_reduce_node_param,
)
from apps.es.serializers import EsClusterSerializers, EsNodeSerializers, EsRuleSerializers
from blueapps.utils.logger import logger
from common.utils.common import get_cc_app_id_by_user
from common.utils.custom_auth import CsrfExemptSessionAuthentication
from common.utils.utils import ApiMixin


class EsClusterViewSet(ApiMixin, viewsets.ModelViewSet):
    """
       es集群表视图
    """
    serializer_class = EsClusterSerializers
    filter_fields = ('cluster_name', 'add_type',)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        """
           重写get_queryset方法，根据用户的业务权限来输出对应记录，用户隔离
        """
        app_id_list = get_cc_app_id_by_user()
        return EsCluster.objects.filter(app_id__in=app_id_list).order_by("-create_time")

    @action(methods=['post'], detail=False)
    def create_cluster(self, request, *args, **kwargs):
        """
           POST /es/create_cluster es集群创建
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_es_deploy_param(post_data=post_data, bk_username=bk_username)
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
    def add_node(self, request):
        """
           POST /api/es/add_node es节点扩容
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_es_add_node_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            add_node_parameter = info['data']
            # 部署任务，检测是否正常
            if add_node_flow(add_node_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "扩容任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "扩容任务启动失败"})

        except Exception as e:
            logger.error(f'create pipeline failed:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})

    @action(methods=['post'], detail=False)
    def reduce_node(self, request, *args, **kwargs):
        """
           POST /api/es/reduce_node es节点缩容
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_es_reduce_node_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            reduce_node_parameter = info['data']
            # 部署任务，检测是否正常
            if reduce_node_flow(reduce_node_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "缩容任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "缩容任务启动失败"})

        except Exception as e:
            logger.error(f'create pipeline failed:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})

    @action(methods=['post'], detail=False)
    def input_cluster(self, request, *args, **kwargs):
        """
           POST /es/input_cluster es集群录入
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_es_input_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            input_parameter = info['data']
            # 部署任务，检测是否正常
            if input_cluster_flow(input_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "集群录入任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "集群录入任务启动失败"})

        except Exception as e:
            logger.error(f'create pipeline failed:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})


class EsNodeViewSet(ApiMixin, viewsets.ModelViewSet):
    """
        es用户信息表视图S
    """
    queryset = EsNodeInfo.objects.all()
    serializer_class = EsNodeSerializers
    filter_fields = ('cluster_name',)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class EsRuleViewSet(ApiMixin, viewsets.ModelViewSet):
    """
        es用户信息表视图
    """

    queryset = EsRule.objects.all()
    serializer_class = EsRuleSerializers
    filter_fields = ('cluster_name',)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
