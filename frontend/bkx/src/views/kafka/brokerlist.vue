<template>
    
    <div class="example1-wrapper">
        <bk-container :col="2">
            <bk-row>
                <bk-col :span="1">
                    <bk-card title="集群信息" style="height: 300px">
                        <p>集群名称: {{ cluster_detail.cluster_name }}</p>
                        <p>集群版本: {{ cluster_detail.version }}</p>
                        <p>集群状态: {{ cluster_detail.cluster_status }}</p>
                        <p>添加模式: {{ cluster_detail.add_type }}</p>
                        <p>集群描述: {{ cluster_detail.description }}</p>
                    </bk-card>
                </bk-col>
                <bk-col :span="1">
                    <bk-card title="集群配置" style="height: 300px">
                        <p>zookeeper集群节点列表: {{ cluster_detail.zk_list }} </p>
                        <p>zookeeper集群访问端口: {{ cluster_detail.zk_port }} </p>
                        <p>broker节点数量: {{ cluster_detail.brokers}}</p>
                   
                    </bk-card>
                </bk-col>
            </bk-row>
            <bk-row style="margin-top: 20px;">
                <bk-tab :active.sync="active" type="unborder-card" :before-toggle="gettab">
                    <bk-tab-panel
                        v-for="(panel, index) in panels"
                        v-bind="panel"
                        :key="index">
                    </bk-tab-panel>
                </bk-tab>
            </bk-row>

            <bk-row style="margin-top: 15px;" v-show="tab === 'broker'">
                <bk-table :data="tableData">
                    <bk-table-column label="业务ID" prop="app_id"></bk-table-column>
                    <bk-table-column label="broker ip" prop="ip"></bk-table-column>
                    <bk-table-column label="版本信息" prop="version"></bk-table-column>
                    <bk-table-column label="设备类型" prop="device_class"></bk-table-column>
                    <bk-table-column label="硬件信息" prop="hard_memo"></bk-table-column>
                </bk-table>
            </bk-row>

            <bk-row style="margin-top: 15px;" v-show="tab === 'topic'">
                <div class="mb10">
                    <bk-button size="small" theme="primary" @click="newTopicdialog">创建Topic</bk-button>
                </div>
                <bk-table :data="tableData" v-bkloading="dataLoading">
                    <bk-table-column label="集群名称" prop="cluster_name"></bk-table-column>
                    <bk-table-column label="topic名称" prop="topic"></bk-table-column>
                    <bk-table-column label="创建人" prop="create_by"></bk-table-column>
                    <bk-table-column label="创建时间" prop="create_time"></bk-table-column>
                </bk-table>
            </bk-row>
        </bk-container>
        <bk-dialog
            v-model="newTopicvisible"
            theme="primary"
            title="创建topic"
            :header-position="'left'"
            :width="600"
            @confirm="submitNewTopic"
        >
            <bk-input :placeholder="'输入新的topic名称'" v-model="newTopicForm.topic" style="margin-bottom: 15px;"></bk-input>
        </bk-dialog>
        
    </div>
</template>

<script>
    export default {
        components: {},
        data () {
            return {
                cluster_detail: {},
                tableData: [],
                tab: 'broker',
                newTopicvisible: false,
                dataLoading: {
                    isLoading: false,
                    opacity: 1,
                    zIndex: 10,
                    theme: 'primary',
                    mode: 'spin'
                },
                newTopicForm: {
                    cluster_name: '',
                    topic: ''
                },
                panels: [
                    { name: 'broker', label: 'broker信息' },
                    { name: 'topic', label: 'topic信息' }
                ],
                active: 'mission'
                
            }
        },
        beforeRouteLeave (to, from, next) {
            localStorage.removeItem('condition')
            next()
        },
        mounted () {
            const condition = localStorage.getItem('condition')
            if (condition != null) {
                this.cluster_detail = JSON.parse(condition)
            } else {
                this.cluster_detail = this.$route.query.row
            }
            this.getKafkaBrokerInfo()
            localStorage.setItem('condition', JSON.stringify(this.cluster_detail))
        },
        methods: {
            gettab (panelName) {
                this.tab = panelName
                if (this.tab === 'broker') {
                    this.getKafkaBrokerInfo()
                } else if (this.tab === 'topic') {
                    this.getKafkaTopicInfo()
                }

                return panelName
            },
            newTopicdialog () {
                this.newTopicForm = {
                    cluster_name: '',
                    topic: ''
                }
                this.newTopicvisible = true
            },
            async getKafkaBrokerInfo () {
                try {
                    const param = { 'cluster_name': this.cluster_detail.cluster_name }
                    const res = await this.$store.dispatch('kafka/getKafkaBroker', param)
                    this.tableData = res.data
                } catch (e) {
                    console.error(e)
                }
            },
            async getKafkaTopicInfo () {
                try {
                    const param = { 'cluster_name': this.cluster_detail.cluster_name }
                    const res = await this.$store.dispatch('kafka/listTopics', param)
                    this.tableData = res.data
                } catch (e) {
                    console.error(e)
                }
            },
            async submitNewTopic () {
                this.dataLoading.isLoading = true
                this.newTopicForm.cluster_name = this.cluster_detail.cluster_name
                try {
                    const res = await this.$store.dispatch('kafka/createTopic', this.newTopicForm)
                    if (res.code === 0) {
                        this.$bkMessage({
                            message: 'topic创建成功',
                            theme: 'success'
                        })
                    } else {
                        this.$bkMessage({
                            message: 'topic创建失败',
                            theme: 'error'
                        })
                    }
                } catch (e) {
                    console.error('submit err: ', e)
                } finally {
                    this.getKafkaTopicInfo()
                    this.dataLoading.isLoading = false
                }
            }
            
        }
    }
</script>
<style lang="postcss">
    .bk-card-body {
        p {
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 8px;
            &:last-child {
                margin-bottom: 0;
            }
        }
    }
</style>
