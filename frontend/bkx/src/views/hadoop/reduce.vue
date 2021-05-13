<template>
    <div class="wrapper">
        <bk-container :col="12">
            <bk-row>
                <bk-col :span="7">
                    <div style="width: 600px;">
                        <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm1">
                            <bk-form-item label="集群名称" :required="true" :property="'cluster_id'" :error-display-type="'normal'">
                                <bk-select v-model="formData.cluster_id" searchable @change="changeHandle">
                                    <bk-option v-for="option in hadoopClusterInfo"
                                        :key="option.cluster_id"
                                        :id="option.cluster_id"
                                        :name="option.cluster_name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item label="缩容IP列表" :required="true" :property="'process_id_list'" :error-display-type="'normal'">
                                <bk-select v-model="formData.process_id_list" searchable multiple show-select-all display-tag>
                                    <bk-option v-for="option in dataNodeList"
                                        :key="option.process_id"
                                        :id="option.process_id"
                                        :name="option.process_ip">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item>
                                <bk-button ext-cls="mr5" theme="primary" title="提交" @click.stop.prevent="checkData" :loading="isChecking">提交</bk-button>
                                <bk-button ext-cls="mr5" theme="default" title="取消">取消</bk-button>
                            </bk-form-item>
                        </bk-form>
                    </div>
                </bk-col>
                <bk-col :span="5">
                    <div>
                        <h2>HDFS集群缩容说明</h2>
                        <p>1> 目前只支持DataNode节点缩容</p>
                        <p>2> 部署的机器IP需要先安装gse_agent,具有业务job执行权限</p>
                        <p>3> 部署任务耗时5分钟左右,后台异步部署,结果请到<a href="/hadoop/hadooprecord">HDFS执行记录中查看</a></p>
                        <p>4> 缩容流程：退役DataNode --> 停止退役节点进程</p>
                        <p>5> 缩容后默认不进行rebanlance操作</p>
                    </div>
                </bk-col>
            </bk-row>
        </bk-container>
    </div>
</template>
<script>
    import { bkForm, bkFormItem, bkButton, bkSelect, bkOption } from '@tencent/bk-magic-vue'

    export default {
        components: {
            bkForm,
            bkFormItem,
            bkButton,
            bkSelect,
            bkOption
            // bkInput
        },
        data () {
            return {
                formData: {
                    cluster_id: '',
                    rebanlance: '0',
                    op_type: 'recycle_datanode',
                    process_id_list: []
                },
                selectData: {
                    add_type: 1
                },
                dataNodeList: [],
                hadoopClusterInfo: [],
                isChecking: false,
                rules: {
                    cluster_id: [
                        {
                            required: true,
                            message: '选择对应的集群',
                            trigger: 'blur'
                        }
                    ],
                    process_id_list: [
                        {
                            required: true,
                            message: '选择对应下线IP',
                            trigger: 'blur'
                        }
                    ]
                }
            }
        },
        created () {
            this.getHadoopData()
        },
        methods: {
            closeDialog () {
                this.$router.push(
                    {
                        path: 'hadooprecord'
                    }
                )
            },
            async changeHandle (value) {
                try {
                    const param = { 'cluster_id': value, 'process_name': 'DataNode' }
                    const res = await this.$store.dispatch('hadoop/getHadoopDetail', param, { fromCache: true })
                    this.dataNodeList = res.data
                    this.formData.cluster_id = value
                } catch (e) {
                    console.error(e)
                }
                return true
            },
            
            async getHadoopData () {
                try {
                    const res = await this.$store.dispatch('hadoop/getHadoopData', this.selectData)
                    // this.tableData = res.data
                    this.hadoopClusterInfo = res.data
                } catch (e) {
                    console.error(e)
                }
            },
            async submitData () {
                try {
                    console.log(this.dataNodeList)
                    const res = await this.$store.dispatch('hadoop/removeDataNode', this.formData)
                    // alert(JSON.stringify(res))
                    console.log(res)
                    if (res.code === 0) {
                        this.isChecking = false
                        const config = { theme: 'success' }
                        config.message = '提交成功, HDFS执行记录中查看缩容详情！'
                        config.offsetY = 80
                        this.$bkMessage(config)
                        this.closeDialog()
                    } else {
                        this.isChecking = false
                        const config = { theme: 'error' }
                        config.message = res.message
                        config.offsetY = 80
                        this.$bkMessage(config)
                    }
                } catch (e) {
                    this.isChecking = false
                    console.log(e)
                }
            },
            checkData () {
                this.isChecking = true
                this.$refs.validateForm1.validate().then(validator => {
                    this.submitData()
                    this.isChecking = false
                }, validator => {
                    this.isChecking = false
                })
            }
        }
    }
</script>

<style>
p.er {color:red;font-size:12pt;}
p.ex {color:rgb(8, 8, 8);font-size:12pt;}
span.er {color:red;font-size:12pt;}
span.inf {color:#00ff00;font-size:12pt;}
</style>
