<template>
    <div class="wrapper">
        <bk-container :col="12">
            <bk-row>
                <bk-col :span="7">
                    <div style="width: 600px;">
                        <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm1">
                            <bk-form-item label="业务名称" :required="true" :property="'app'" :error-display-type="'normal'">
                                <bk-select v-model="formData.app_id" searchable placeholder="请选择对应的业务名称">
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
                            <bk-form-item label="ES集群httpUrl" :required="true" :property="'input_http_url'" :error-display-type="'normal'">
                                <bk-input v-model="formData.input_http_url" placeholder="请输入集群的url，用户获取es的集群状态信息"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="集群版本" :required="true" :property="'version'" :error-display-type="'normal'">
                                <bk-input v-model="formData.version" placeholder="请输入对应的版本编号，输入格式：0.0.0"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="用户名" :property="'account'">
                                <bk-input v-model="formData.account" placeholder="若存在登录账号，则填写登录账号"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="密码" :property="'password'">
                                <bk-input v-model="formData.password" :type="'password'" placeholder="填写登录账号密码"></bk-input>
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
                        <h2>ES集群录入说明</h2>
                        <p class="ex">1> 输入正确的ES的url来获取集群信息，同步到平台</p>
                        <p class="ex">2> 集群名称建议只包含小写字母，数字及-</p>
                        <p class="ex">3> 若原本的集群需要账号密码，则输入对应的账号密码</p>
                        <p class="ex">4> 带*号的为必填项</p>
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
                    input_http_url: '',
                    version: '',
                    description: '',
                    app: '',
                    app_id: '',
                    account: '',
                    password: ''
                },
                submitLoading: false,
                appList: [],
                isChecking: false,
                rules: {
                    cluster_name: [
                        {
                            required: true,
                            pattern: /^[a-z0-9]+[a-z0-9-]+[a-z0-9]+$/,
                            message: '请输入集群名称(只能包含小写字母，数字，-)',
                            trigger: 'change'
                        },
                        { min: 2, max: 32, message: '长度在 2 到 32 个字符', trigger: 'change' }
                        
                    ],
                    input_http_url: [
                        {
                            required: true,
                            message: '请输入正确的url地址',
                            trigger: 'change'
                        }
                    ],
                    version: [
                        {
                            required: true,
                            message: '版本不能为空',
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
                    const res = await this.$store.dispatch('es/inputEsCluster', this.formData)
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
                    this.isChecking = false
                }, validator => {
                    this.isChecking = false
                })
            }
        }
    }
</script>
