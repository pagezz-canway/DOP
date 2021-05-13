<template>
    <div class="wrapper">
        <bk-container :col="12">
            <bk-row>
                <bk-col :span="7">
                    <div style="width: 600px;">
                        <bk-form :label-width="200" :model="formData" ref="validateForm1">
                            <bk-form-item label="集群" :required="true" :property="'cluster_name'">
                                <bk-select v-model="formData.cluster_name" searchable>
                                    <bk-option v-for="option in esClusterName"
                                        :key="option.cluster_name"
                                        :id="option.cluster_name"
                                        :name="option.cluster_name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item label="IP" :required="true" :property="'ips'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.ips" placeholder="待缩容的ip列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item>
                                <bk-button ext-cls="mr5" theme="primary" title="提交" @click="submitData" :loading="isChecking">提交</bk-button>
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
                        <p class="ex">3> 执行流程：变迁数据->关闭节点</p>
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
                rules: {}
            }
        },
        created () {
            this.getEsClusterName()
        },
        methods: {
            async checkName (val) {
                const resutl = await this.asyncCheck(val)
                return resutl
            },
            async asyncCheck (val) {
                // 模拟异步请求
                const p = new Promise((resolve, reject) => {
                    setTimeout(() => {
                        if (val === 'admin') {
                            Promise.reject(new Error('地址解析失败, 请刷新重试'))
                        } else {
                            resolve(true)
                        }
                    }, 2000)
                })
                const result = await p.then(res => {
                    return true
                }).catch(res => {
                    return false
                })
                return result
            },
            async getEsClusterName () {
                try {
                    const res = await this.$store.dispatch('es/getEsClusterName')
                    // console.log(res)
                    this.esClusterName = res.data
                } catch (e) {
                    console.error(e)
                }
            },
            validate1 () {
                this.isChecking = true
                this.$refs.validateForm1.validate().then(validator => {
                    if (validator) {
                        try {
                            const res = this.$store.dispatch('es/createEsCluster', this.formData)
                            // alert(JSON.stringify(res))
                            if (res.code === 0) {
                                alert('tijaochengogn')
                                console.log('success')
                            }
                        } catch (e) {
                            console.log(e)
                        }
                        alert('验证成功！')
                        this.isChecking = false
                    } else {
                        console.log('error submit!!')
                        return false
                    }
                })
            },
            clearError1 () {
                this.$refs.validateForm1.clearError()
            },
            async submitData () {
                try {
                    const res = await this.$store.dispatch('es/reduceNode', this.formData)
                    // alert(JSON.stringify(res))
                    console.log(res)
                    if (res.code === 0) {
                        // alert('tijaochengogn')
                        // console.log('success')
                        const config = { theme: 'success' }
                        config.message = '提交成功, 请到HDFS执行记录中查看部署详情！'
                        config.offsetY = 80
                        this.$bkMessage(config)
                    }
                } catch (e) {
                    console.log(e)
                }
            }
        }
    }
</script>
