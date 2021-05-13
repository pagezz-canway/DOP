<template>
    <div class="wrapper">
        <bk-container :col="12">
            <bk-row>
                <bk-col :span="7">
                    <div style="width: 600px;">
                        <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm1">
                            <bk-form-item label="集群名称" :required="true" :property="'cluster_id'" :error-display-type="'normal'">
                                <bk-select v-model="formData.cluster_id" searchable>
                                    <bk-option v-for="option in hadoopClusterInfo"
                                        :key="option.cluster_id"
                                        :id="option.cluster_id"
                                        :name="option.cluster_name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item label="扩容模式" :required="true" :property="'op_type'" :error-display-type="'normal'">
                                <bk-select v-model="formData.op_type" searchable>
                                    <bk-option v-for="option in roleList"
                                        :key="option.id"
                                        :id="option.id"
                                        :name="option.name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item label="扩容目录路径" :property="'data_dir'" :error-display-type="'normal'" v-show="formData.op_type === 'add_dir'">
                                <bk-input type="textarea" v-model="formData.data_dir" placeholder="合法已存在目录，多个用英文逗号隔开"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="扩容IP列表" :property="'ips'" :error-display-type="'normal'" v-show="formData.op_type === 'add_datanode'">
                                <bk-input type="textarea" v-model="formData.ips" placeholder="待扩容的ip列表，多个用英文逗号隔开"></bk-input>
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
                        <h2>HDFS集群扩容说明</h2>
                        <p>1> 支持DataNode节点扩容与目录扩容,目录扩容需要所有机器必须存在</p>
                        <p>2> 强制数据清理配置，只在目录扩容下生效</p>
                        <p>3> 部署的机器IP需要先安装gse_agent,具有业务job执行权限</p>
                        <p>4> 部署任务耗时3分钟左右,后台异步部署,结果请到<a href="/hadoop/hadooprecord">HDFS执行记录中查看</a></p>
                        <p>5> 扩容完成后默认不进行rebanlance操作</p>
                    </div>
                </bk-col>
            </bk-row>
        </bk-container>
    </div>
</template>
<script>
    import { bkForm, bkFormItem, bkButton, bkInput } from '@tencent/bk-magic-vue'

    export default {
        components: {
            bkForm,
            bkFormItem,
            bkButton,
            bkInput
        },
        data () {
            return {
                formData: {
                    cluster_id: '',
                    op_type: '',
                    ips: '',
                    data_dir: '',
                    clean_data_force: ''
                },
                selectData: {
                    add_type: 1
                },
                roleList: [
                    {
                        id: 'add_datanode',
                        name: 'datanode节点扩容'
                    },
                    {
                        id: 'add_dir',
                        name: 'datanode目录扩容'
                    }
                ],
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
                    op_type: [
                        {
                            required: true,
                            message: '选择对应的扩容模式',
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
                    let url = ''
                    if (this.formData.op_type === 'add_datanode') {
                        url = 'hadoop/addDataNode'
                    } else {
                        url = 'hadoop/addDir'
                    }
                    const res = await this.$store.dispatch(url, this.formData)
                    if (res.code === 0) {
                        this.isChecking = false
                        const config = { theme: 'success' }
                        config.message = '提交成功, 跳转到HDFS执行记录中查看扩容详情！'
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
                    this.isChecking = false
                    this.submitData()
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
