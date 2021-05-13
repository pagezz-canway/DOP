# -*- coding:utf-8 _*-
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action

from apps.hadoop.hadoop_flow import (
    add_datanode_flow,
    add_dir_flow,
    deploy_cluster_flow,
    input_cluster_flow,
    remove_datanode_flow,
)
from apps.hadoop.models import ClusterInfo, ClusterDetail
from apps.hadoop.parameter import (
    retrieval_hadoop_add_dir_param,
    retrieval_hadoop_add_node_param,
    retrieval_hadoop_deploy_param,
    retrieval_hadoop_remove_node_param,
)
from apps.hadoop.serializers import HadoopClusterSerializers, HadoopDetailSerializers
from blueapps.utils.logger import logger
from common.utils.common import get_cc_app_id_by_user
from common.utils.custom_auth import CsrfExemptSessionAuthentication
from common.utils.utils import ApiMixin


class HadoopClusterViewSet(ApiMixin, viewsets.ModelViewSet):
    """
       hadoop集群表视图
    """
    serializer_class = HadoopClusterSerializers
    filter_fields = ('cluster_name', 'add_type',)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        """
            重写get_queryset方法，根据用户的业务权限来输出对应记录，用户隔离
        """
        app_id_list = get_cc_app_id_by_user()
        return ClusterInfo.objects.filter(app_id__in=app_id_list).order_by("-create_time")

    @action(methods=['post'], detail=False)
    def create_cluster(self, request, *args, **kwargs):
        """
           POST /hadoop/create_cluster hadoop集群创建
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_hadoop_deploy_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            deploy_parameter = info['data']
            if deploy_cluster_flow(deploy_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "部署任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "部署任务失败"})

            # 部署任务，检测是否正常
        except Exception as e:
            logger.error(f'发布任务出现异常:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})

    @action(methods=['post'], detail=False)
    def add_node(self, request, *args, **kwargs):
        """
           POST /hadoop/add_node  hadoop集群添加node节点(datanode)
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_hadoop_add_node_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            deploy_parameter = info['data']
            if add_datanode_flow(deploy_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "部署任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "部署任务失败"})

            # 部署任务，检测是否正常
        except Exception as e:
            logger.error(f'发布任务出现异常:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})

    @action(methods=['post'], detail=False)
    def add_dir(self, request, *args, **kwargs):
        """
           POST /hadoop/add_dir  hadoop集群添加数据目录
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_hadoop_add_dir_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            deploy_parameter = info['data']
            if add_dir_flow(deploy_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "部署任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "部署任务失败"})

            # 部署任务，检测是否正常
        except Exception as e:
            logger.error(f'发布任务出现异常:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})

    @action(methods=['post'], detail=False)
    def remove_node(self, request, *args, **kwargs):
        """
           POST /hadoop/remove_node   hadoop集群回收node节点(datanode)
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_hadoop_remove_node_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            deploy_parameter = info['data']
            if remove_datanode_flow(deploy_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "部署任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "部署任务失败"})

            # 部署任务，检测是否正常
        except Exception as e:
            logger.error(f'发布任务出现异常:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})

    @action(methods=['post'], detail=False)
    def input_cluster(self, request, *args, **kwargs):
        """
           POST /hadoop/input_cluster   hadoop集群录入
        """
        try:
            post_data = request.data
            bk_username = request.user.username
            info = retrieval_hadoop_deploy_param(post_data=post_data, bk_username=bk_username)
            if info['code'] == 0:
                # 参数存在异常返回失败
                return JsonResponse(info['data'])

            deploy_parameter = info['data']
            if input_cluster_flow(deploy_parameter):
                return JsonResponse({"result": True, "data": [], "code": 0, "message": "部署任务已启动"})

            return JsonResponse({"result": False, "data": [], "code": 1, "message": "部署任务失败"})

            # 部署任务，检测是否正常
        except Exception as e:
            logger.error(f'发布任务出现异常:{e}')
            return JsonResponse({'result': False, 'code': 1, 'data': [], 'message': f'{e}'})


class HadoopDetailViewSet(ApiMixin, viewsets.ModelViewSet):
    """
       hadoop集群节点视图
    """
    queryset = ClusterDetail.objects.all()
    serializer_class = HadoopDetailSerializers
    filter_fields = ('cluster_id', 'hadoop_group_name', 'process_name')
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
