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
                            <bk-form-item label="数据角色" :required="true" :property="'role'" :error-display-type="'normal'">
                                <bk-select v-model="formData.role" searchable>
                                    <bk-option v-for="option in roleList"
                                        :key="option.id"
                                        :id="option.id"
                                        :name="option.name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item label="扩容IP" :required="true" :property="'ips'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.ips" placeholder="待扩容的ip列表"></bk-input>
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
                        <h2>ES集群扩容说明</h2>
                        <p class="ex">1> 选择需要扩容的集群</p>
                        <p class="ex">2> 需要扩容的节点类型</p>
                        <p class="ex">3> 填入要扩容的机器IP，一行一个IP</p>
                        <p class="ex">4> 扩容的节点必须是新加节点，且不能存在es进程，节点的环境目录/data/esenv必须为空</p>
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
                    role: '',
                    ips: ''
                },
                roleList: [
                    {
                        id: 'master',
                        name: '主节点'
                    },
                    {
                        id: 'data',
                        name: '数据节点'
                    },
                    {
                        id: 'cold',
                        name: '冷节点'
                    },
                    {
                        id: 'client',
                        name: '协调节点'
                    }
                ],
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
                    role: [
                        {
                            required: true,
                            message: '选择对应的扩容节点角色',
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
                    // console.log(res)
                    this.esClusterName = res.data
                } catch (e) {
                    console.error(e)
                }
            },
            async submitData () {
                try {
                    const res = await this.$store.dispatch('es/addNode', this.formData)
                    // alert(JSON.stringify(res))
                    console.log(res)
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
