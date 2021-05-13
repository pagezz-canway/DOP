<template>
    <div class="wrapper">
        <bk-container :col="12">
            <bk-row>
                <bk-col :span="7">
                    <div style="width: 600px;">
                        <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm1">
                            <bk-form-item label="业务名称" :required="true" :property="'app'" :error-display-type="'normal'">
                                <bk-select v-model="formData.app_id" searchable>
                                    <bk-option v-for="option in appList"
                                        :key="option.bk_biz_id"
                                        :id="option.bk_biz_id"
                                        :name="option.bk_biz_name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item label="集群名称" :required="true" :property="'cluster_name'" :error-display-type="'normal'">
                                <bk-input v-model="formData.cluster_name" placeholder="请输入集群名称"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="版本选择" :required="true" :property="'version'" :error-display-type="'normal'">
                                <bk-select v-model="formData.version" searchable>
                                    <bk-option v-for="option in versionList"
                                        :key="option.id"
                                        :id="option.id"
                                        :name="option.name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item label="master node" :required="true" :property="'master_list'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.master_list" placeholder="请输入主节点IP列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="data node" :required="true" :property="'data_list'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.data_list" placeholder="请输入数据节点IP列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="cold node" :property="'cold_list'">
                                <bk-input type="textarea" v-model="formData.cold_list" placeholder="请输冷节点IP列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="client node" :property="'client_list'">
                                <bk-input type="textarea" v-model="formData.client_list" placeholder="请输入协调节点IP列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="用户名" :required="true" :property="'account'" :error-display-type="'normal'">
                                <bk-input v-model="formData.account" placeholder="请输入访问ES的账号，集群创建之后建立"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="密码" :required="true" :property="'password'" :error-display-type="'normal'">
                                <bk-input :type="'password'" v-model="formData.password" placeholder="请输入访问ES的密码"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="项目描述">
                                <bk-input type="textarea" v-model="formData.description"></bk-input>
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
                        <h2>ES集群新建说明</h2>
                        <p class="ex">1> 最小集群需要5台机器：3台master node，2台data node</p>
                        <p class="ex">2> 集群名称建议只包含小写字母，数字及-</p>
                        <p class="ex">3> 请记住账号及密码，出于安全考虑，密码不会被保存</p>
                        <p class="ex">4> 带*号的为必填项</p>
                        <p class="ex">5> IP请以换行符形式分隔</p>
                        <p class="ex">6> 默认的http端口是6300（暂无法指定）</p>
                        <p class="ex">7> 部署的节点必须是新加节点，且不存在es进程，节点的环境目录/data/esenv必须为空，否则部署会失败</p>
                    </div>
                </bk-col>
            </bk-row>
        </bk-container>
    </div>
</template>
<script>
    export default {
        components: {

        },
        data () {
            return {
                formData: {
                    cluster_name: '',
                    version: '',
                    master_list: '',
                    data_list: '',
                    cold_list: '',
                    client_list: '',
                    http_port: '6300',
                    description: '',
                    app: '',
                    app_id: '',
                    account: '',
                    password: ''
                },
                appList: [],
                versionList: [
                    // {
                    //     id: '5.4.0',
                    //     name: '5.4.0'
                    // },
                    {
                        id: '7.10.0',
                        name: '7.10.0'
                    }
                    // {
                    //     id: '6.8.1',
                    //     name: '6.8.1(暂不支持)'
                    // }
                ],
                isChecking: false,
                rules: {
                
                    cluster_name: [
                        {
                            required: true,
                            message: '请输入集群名称',
                            trigger: 'blur'
                        },
                        {
                            regex: /^[a-z0-9]+[a-z0-9-]+[a-z0-9]+$/,
                            message: '只能包含小写字母，数字，-, 长度不少于3',
                            trigger: 'change'
                        }
                    ],
                    version: [
                        {
                            required: true,
                            message: '请选择版本',
                            trigger: 'change'
                        }
                    ],
                    master_list: [
                        {
                            required: true,
                            message: '请输入作为master的IP列表',
                            trigger: 'change'
                        }
                    ],
                    data_list: [
                        {
                            required: true,
                            message: '请输入作为数据节点的IP列表',
                            trigger: 'blur'
                        }
                    ],
                    account: [
                        {
                            required: true,
                            message: '请输入集群初始用户名称',
                            trigger: 'change'
                        }
                    ],
                    password: [
                        {
                            required: true,
                            message: '请输入集群初始用户密码',
                            trigger: 'change'
                        }
                    ],
                    app: [
                        {
                            required: true,
                            message: '请选择对应的业务名称',
                            trigger: 'change'
                        }
                    ]
                }
            }
        },
        watch: {
            'formData.app_id': function (val) {
                this.formData.app_id = val
                this.appList.forEach(item => {
                    if (this.formData.app_id === item.bk_biz_id) {
                        this.formData.app = item.bk_biz_name
                        return true
                    }
                }
                )
            }
        },
        created () {
            this.getCc()
        },
        methods: {
            closeDialog () {
                this.$router.push(
                    {
                        path: 'record'
                    }
                )
            },
            async submitnewclusterForm () {
                try {
                    const res = await this.$store.dispatch('es/createEsCluster', this.formData)
                    if (res.code === 0) {
                        this.isChecking = false
                        const config = { theme: 'success' }
                        config.message = '提交成功, 跳转到ES执行记录中查看部署详情！'
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
                } catch (err) {
                    this.isChecking = false
                    this.$bkMessage({
                        message: err.message ? err.message : err,
                        theme: 'error'
                    })
                }
            },
            async getCc () {
                try {
                    const res = await this.$store.dispatch('es/getAppList')
                    this.appList = res.data.info
                } catch (e) {
                    console.error(e)
                }
            },
            checkData () {
                this.isChecking = true
                this.$refs.validateForm1.validate().then(validator => {
                    this.submitnewclusterForm()
                }, validator => {
                    this.isChecking = false
                })
            }
        }
    }
</script>
