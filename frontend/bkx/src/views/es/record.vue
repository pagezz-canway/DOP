<template>
    <div class="example1-wrapper">
        
        <bk-dialog v-model="revoketask.primary.visible"
            theme="primary"
            :mask-close="true"
            :header-position="revoketask.primary.headerPosition"
            @confirm="optask(revoketask.id, 'revoke')"
            title="撤销任务">
            <p><small>流程ID : {{ revoketask.id }}</small></p>
            <p><small>撤销任务后任务不再被调用，是否确认?</small></p>
        </bk-dialog>

        <bk-dialog v-model="pausetask.primary.visible"
            theme="primary"
            :mask-close="true"
            :header-position="pausetask.primary.headerPosition"
            @confirm="optask(pausetask.id, 'pause')"
            title="暂停任务">
            <p><small>流程ID : {{ pausetask.id }}</small></p>
            <p><small>暂停任务后任务流程则中断，是否确认?</small></p>
        </bk-dialog>

        <bk-dialog v-model="resumetask.primary.visible"
            theme="primary"
            :mask-close="true"
            :header-position="resumetask.primary.headerPosition"
            @confirm="optask(resumetask.id, 'resume')"
            title="重新执行任务">
            <p><small>流程ID : {{ resumetask.id }}</small></p>
            <p><small>即将重新执行已暂停任务，是否确认?</small></p>
        </bk-dialog>

        <div class="fr clearfix mb15">
            <bk-form form-type="inline">
                <bk-form-item label="集群名称">
                    <bk-input placeholder="搜索任务对应集群名称" v-model="formData.cluster_name"></bk-input>
                </bk-form-item>
                <bk-form-item label="创建日期">
                    <bk-date-picker placeholder="搜索任务的创建日期" v-model="timeRange" :type="'datetimerange'"></bk-date-picker>
                </bk-form-item>
                <bk-form-item>
                    <bk-button @click="search()" theme="primary" title="提交">搜索</bk-button>
                </bk-form-item>
            </bk-form>
        </div>
        <bk-table style="margin-top: 15px;"
            :data="tableData"
            :size="size"
            :pagination="pagination"
            @highlight-current-row="true"
            @row-mouse-enter="handleRowMouseEnter"
            @row-mouse-leave="handleRowMouseLeave"
            @page-change="handlePageChange"
            @page-limit-change="handlePageLimitChange">
            <bk-table-column label="流程ID" width="250" prop="pipeline_id"></bk-table-column>
            <bk-table-column label="集群名" prop="cluster_name"></bk-table-column>
            <bk-table-column label="组件名称" prop="db_type"></bk-table-column>
            <bk-table-column label="任务模式" prop="task_mode"
                :filters="typeFilters"
                :filter-method="typeFiltersMethod"
                :filter-multiple="false">
            </bk-table-column>
            <bk-table-column label="任务类型" prop="task_type"></bk-table-column>
            <bk-table-column label="操作人" prop="op_user"></bk-table-column>
            <bk-table-column label="执行状态" prop="task_status"
                :filters="statusFilters"
                :filter-method="statusFilterMethod"
                :filter-multiple="true">
            </bk-table-column>
            <bk-table-column label="创建时间" prop="create_time"></bk-table-column>
            <bk-table-column label="任务耗时" prop="stop_time"></bk-table-column>
            <bk-table-column label="任务操作" width="200">
                <template slot-scope="props">
                    <bk-button theme="primary" text @click="pause(props.row)">暂停</bk-button>
                    <bk-button theme="primary" text @click="revoke(props.row)">撤销</bk-button>
                    <bk-button theme="primary" text @click="resume(props.row)">执行</bk-button>
                    <!-- <bk-button theme="primary" text @click="resume(props.row)">重试</bk-button> -->
                    <bk-button theme="primary" text @click="getKafkaTaskRecordDetail(props.row)">详情</bk-button>
                </template>
            </bk-table-column>
        </bk-table>
        <bk-sideslider :is-show.sync="customSettings.isShow" :quick-close="true" :width="customSettings.width">
            <div slot="header">{{ customSettings.title }}</div>
            <div class="p30" slot="content">
                <bk-container>
                    <bk-row>
                        <bk-timeline :list="TaskDtateDetails"></bk-timeline>

                    </bk-row>

                </bk-container>
            </div>
        </bk-sideslider>
    </div>
</template>

<script>
    // import { formatDate } from '../../common/dateformat'
    export default {
        components: {
        },
        data () {
            return {
                timeRange: [],
                statusFilters: [
                    { text: '未执行', value: '未执行' },
                    { text: '正在执行', value: '正在执行' },
                    { text: '执行完成', value: '执行完成' },
                    { text: '执行失败', value: '执行失败' },
                    { text: '任务暂停', value: '任务暂停' },
                    { text: '任务撤销', value: '任务撤销' }
                ],
                typeFilters: [
                    { text: '异步触发', value: '异步触发' },
                    { text: '同步触发', value: '同步触发' }
                ],
                revoketask: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    },
                    id: ''
                },
                pausetask: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    },
                    id: ''
                },
                resumetask: {
                    primary: {
                        visible: false,
                        headerPosition: 'left'
                    },
                    id: ''
                },
                formData: {
                    db_type: 1,
                    cluster_name: '',
                    start_time: '',
                    stop_time: ''
                },
                // tableData: [],
                temptableData: [],
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10
                },
                customSettings: {
                    isShow: false,
                    title: '任务详情',
                    width: 600
                },
                TaskDtateDetails: [],
                task_id: ''
            }
        },
        computed: {
            tableData: function () {
                const start = (this.pagination.current - 1) * this.pagination.limit
                const end = start + this.pagination.limit < this.pagination.count ? start + this.pagination.limit : this.pagination.count
                return this.temptableData.slice(start, end)
            }
        },
        watch: {
            
            'timeRange': function (val) {
                this.formData.start_time = val[0]
                this.formData.stop_time = val[1]
            }
        },
        created () {
            this.getTaskData(this.formData)
        },
        mounted () {
            if (this.timer) {
                clearInterval(this.timer)
            } else {
                this.timer = setInterval(() => {
                    this.search()
                }, 5000)
            }
        },
        destroyed () {
            clearInterval(this.timer)
        },
        methods: {
            handleInfo (config) {
                config.offsetY = 80
                this.$bkMessage(config)
            },
            async getTaskData (param) {
                try {
                    const res = await this.$store.dispatch('es/getEsTaskRecord', param, { fromCache: true })
                    this.temptableData = res.data
                    this.pagination.count = res.data.length
                } catch (e) {
                    console.error(e)
                }
            },
            async getKafkaTaskRecordDetail (row) {
                try {
                    this.customSettings.isShow = true
                    const param = { 'pipeline_id': row.pipeline_id }
                    const res = await this.$store.dispatch('es/getEsTaskRecordDetail', param, { fromCache: true })
                    this.TaskDtateDetails = res.data
                } catch (e) {
                    console.error(e)
                }
            },
            handlePageLimitChange (limit) {
                this.pagination.limit = limit
            },
            handlePageChange (page) {
                this.pagination.current = page
            },
            statusFilterMethod (value, row, column) {
                const property = column.property
                return row[property] === value
            },
            typeFiltersMethod (value, row, column) {
                const property = column.property
                return row[property] === value
            },
            search () {
                console.log(this.formData.stop_time)
                this.getTaskData(this.formData)
            },
            revoke (row) {
                if (row.task_status !== '执行完成' && row.task_status !== '任务撤销') {
                    this.revoketask.primary.visible = true
                    this.revoketask.id = row.pipeline_id
                } else {
                    this.handleInfo({ theme: 'error', limit: 1, delay: 2000, message: '任务已完成/任务已撤销，无法撤销' })
                }
            },
            pause (row) {
                if (row.task_status === '正在执行') {
                    this.pausetask.primary.visible = true
                    this.pausetask.id = row.pipeline_id
                } else {
                    this.handleInfo({ theme: 'error', limit: 1, delay: 2000, message: '任务未正在执行，无法暂停' })
                }
            },
            resume (row) {
                if (row.task_status === '任务暂停') {
                    this.resumetask.primary.visible = true
                    this.resumetask.id = row.pipeline_id
                } else {
                    this.handleInfo({ theme: 'error', limit: 1, delay: 2000, message: '任务未执行暂停，无法重新执行' })
                }
            },
            async optask (Id, opType) {
                try {
                    const res = await this.$store.dispatch('es/opTask', { 'id': Id, 'op_type': opType })
                    console.log(res)
                    if (res.code === 0) {
                        this.handleInfo({ theme: 'success', limit: 1, delay: 3000, message: '操作成功' })
                        this.getTaskData(this.formData)
                    } else {
                        this.handleInfo({ theme: 'error', limit: 1, delay: 3000, message: '操作失败' })
                    }
                } catch (e) {
                    console.log(e)
                }
            }

        }
    }
    
</script>
<style lang="postcss">
    .timeline-update-time {
        font-size: 12px;
        color: #979ba5;
    }
    .timeline-content {
        p {
            margin-top: 0;
            margin-bottom: 8px;
        }
    }
</style>
