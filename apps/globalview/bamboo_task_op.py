# -*- coding:utf-8 _*-
import json

from apps.globalview.models import TaskRecord
from blueapps.utils.logger import logger
from common.utils.bamboo_api import PipelineTaskApi
from common.utils.common import build_fail_result, build_success_result


'''
@summary:
@usage:
'''


def get_task_state(kwargs):
    """
       根据pipeline_id来获取task的流程树信息
    """
    return_data = []
    pipeline_id = kwargs.get('pipeline_id')
    pipeline_states = PipelineTaskApi(kwargs).get_task_states()
    pipeline_tree_str = TaskRecord.objects.get(pipeline_id=pipeline_id).pipeline_tree
    try:

        pipeline_tree = json.loads(pipeline_tree_str)
        for node_id in pipeline_tree:

            node_info = {'tag': "<strong>{}</strong>".format(pipeline_tree[node_id])}
            pipeline_child = pipeline_states[pipeline_id]['children']
            child_log_content = PipelineTaskApi({'node_id': node_id}).get_node_output()

            if node_id not in pipeline_child.keys():
                # 节点尚未执行
                node_info['color'] = 'silver'
                return_data.append(node_info)
                continue

            if pipeline_child[node_id]['state'] == 'FINISHED':
                node_info['color'] = 'green'
                # 节点执行成功不查询日志，直接返回"success"
                node_info['content'] = child_log_content

            elif pipeline_child[node_id]['state'] == 'FAILED':

                # 如果活动节点执行中断，则以fail输出
                if child_log_content == 'fail':
                    node_info['content'] = child_log_content
                    node_info['color'] = 'red'
                    return_data.append(node_info)
                    continue

                # 若节点正常执行失败，查询每个IP的执行情况
                if isinstance(child_log_content, dict):
                    err_dict = child_log_content
                else:
                    err_dict = json.loads(child_log_content)

                err_message = ""
                node_info['color'] = 'red'
                for err_key in err_dict:
                    err_message = err_message + "<p><small>{}:{}</small></p>".format(err_key, err_dict[err_key])
                node_info['content'] = err_message

            else:
                # 其他情况代表节点正在执行中
                node_info['color'] = 'blue'
                node_info['size'] = 'large'
                node_info['content'] = PipelineTaskApi({'node_id': node_id}).get_node_output()

            return_data.append(node_info)

    except Exception as err:
        logger.warning(str(err))

    finally:
        return return_data


def op_pipeline_task(kwargs):
    """
       对任务做管理操作，目前支持 任务启动，任务撤销，任务暂停
    """
    try:
        pipeline_id = kwargs.get("id")
        op_type = kwargs.get('op_type')
        task = PipelineTaskApi({'pipeline_id': pipeline_id})
        if op_type == 'revoke':
            if task.task_revoke():
                return build_success_result("操作成功")
            else:
                return build_fail_result("操作失败")

        elif op_type == 'resume':
            if task.task_resume():
                return build_success_result("操作成功")
            else:
                return build_fail_result("操作失败")

        elif op_type == 'pause':
            if task.task_pause():
                return build_success_result("操作成功")
            else:
                return build_fail_result("操作失败")
        else:
            return build_fail_result("后端暂不执行该类型操作:{}".format(op_type))

    except Exception as err:
        logger.error(str(err))
