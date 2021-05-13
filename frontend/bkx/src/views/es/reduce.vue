<template>
    <div class="wrapper">
        <bk-container :col="12">
            <bk-row>
                <bk-col :span="7">
                    <div style="width: 600px;">
                        <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm1">
                            <bk-form-item label="集群名称" :required="true" :property="'cluster_name'" :error-display-type="'normal'">
                                <bk-select v-model="formData.cluster_name" searchable>
                                    <bk-option v-for="option in esClusterName"
                                        :key="option.cluster_name"
                                        :id="option.cluster_name"
                                        :name="option.cluster_name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item label="缩容IP" :required="true" :property="'ips'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.ips" placeholder="待缩容的ip列表"></bk-input>
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
                        <h2>ES集群缩容说明</h2>
                        <p class="ex">1> 选择需要缩容的集群</p>
                        <p class="ex">2> 填入需要缩容的节点IP</p>
                        <p class="ex">3> 执行流程：变迁数据->关闭节点(为了安全考虑，目前版本缩容节点后暂不执行关闭节点)</p>
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
                    ips: ''
                },
                esClusterName: [],
                isChecking: false,
                rules: {
                    cluster_name: [
                        {
                            required: true,
                            message: '选择对应的集群',
                            trigger: 'blur'
                        }
                    ],
                    ips: [
                        {
                            required: true,
                            message: '填写ip列表',
                            trigger: 'blur'
                        }
                    ]
                }
            }
        },
        
        created () {
            this.getEsClusterName()
        },
        methods: {
            closeDialog () {
                this.$router.push(
                    {
                        path: 'record'
                    }
                )
            },
            async getEsClusterName () {
                try {
                    const param = { add_type: 1 }
                    const res = await this.$store.dispatch('es/getEsData', param)
                    this.esClusterName = res.data
                } catch (e) {
                    console.error(e)
                }
            },
            async submitData () {
                try {
                    const res = await this.$store.dispatch('es/reduceNode', this.formData)
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
