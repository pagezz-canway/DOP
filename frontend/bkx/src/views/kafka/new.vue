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
                            <bk-form-item label="broker节点信息" :required="true" :property="'broker_list'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.broker_list" placeholder="请输入broker的IP列表，一个行一个IP"></bk-input>
                            </bk-form-item>
                            <!-- <bk-form-item label="用户名" :required="true" :property="'user'" :error-display-type="'normal'">
                                <bk-input v-model="formData.user" placeholder="请输入访问Kafka的账号，集群创建之后建立"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="密码" :required="true" :property="'password'" :error-display-type="'normal'">
                                <bk-input v-model="formData.password" :type="'password'" placeholder="请输入访问Kafka的密码"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item> -->
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
                        <h2>Kafka集群部署说明</h2>
                        <p class="ex">1> 最小集群需要3台机器</p>
                        <p class="ex">2> 集群名称建议只包含小写字母，数字及-</p>
                        <!-- <p class="ex">3> 请记住账号及密码，出于安全考虑，密码不会被保存</p> -->
                        <p class="ex">3> 带*号的为必填项</p>
                        <p class="ex">4> IP请以换行符形式分隔</p>
                        <p class="ex">5> 部署的IP必须尚未部署kafka进程，且/data/kafkaenv部署目录为空</p>
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
                    cluster_name: '',
                    version: '',
                    broker_list: '',
                    description: '',
                    app: '',
                    app_id: ''
                    // user: '',
                    // password: ''
                },
                appList: [],
                isChecking: false,
                versionList: [
                    {
                        id: '6.0.1',
                        name: 'confluent 6.0.1(kafka 2.6)'
                    }
                ],
                rules: {
                    app: [
                        {
                            required: true,
                            message: '选择对应的业务名称',
                            trigger: 'change'
                        }
                    ],
                    cluster_name: [
                        {
                            required: true,
                            pattern: /^[a-z0-9]+[a-z0-9-]+[a-z0-9]+$/,
                            message: '请输入集群名称(只能包含小写字母，数字，-)',
                            trigger: 'change'
                        },
                        {
                            min: 2,
                            max: 32,
                            message: '长度在 2 到 32 个字符',
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
                    broker_list: [
                        {
                            required: true,
                            message: 'broker节点为空',
                            trigger: 'change'
                        }
                    ],
                    user: [
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
                    const res = await this.$store.dispatch('kafka/createKafkaCluster', this.formData)
                    this.submitLoading = false
                    if (res.code === 0) {
                        this.isChecking = false
                        const config = { theme: 'success' }
                        config.message = '提交成功, 跳转到Kafka执行记录中查看部署详情！'
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
                    this.isChecking = false
                }, validator => {
                    this.isChecking = false
                })
            }
        }
    }
</script>
