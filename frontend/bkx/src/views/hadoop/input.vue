<template>
    <div class="wrapper">
        <bk-container :col="12">
            <bk-row>
                <div>
                    <bk-process
                        :list="dataList"
                        :cur-process.sync="curProcess"
                        :display-key="'content'"
                        :show-steps="ture"
                        :controllable="false"
                        @process-changed="changeProcess"
                    ></bk-process>
            
                </div>
            </bk-row>
            <bk-row>
                <bk-col :span="7" style="margin-top: 50px;">
                    <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm1" v-show="curProcess === 1">
                        <bk-form-item label="业务名称" :required="true" :property="'app_id'" :error-display-type="'normal'">
                            <bk-select v-model="formData.app_id" searchable placeholder="请选择集群对应的业务名称">
                                <bk-option v-for="option in appinfo"
                                    :key="option.bk_biz_id"
                                    :id="option.bk_biz_id"
                                    :name="option.bk_biz_name">
                                </bk-option>
                            </bk-select>
                        </bk-form-item>
                        <bk-form-item label="集群名称" :required="true" :property="'cluster_name'" :error-display-type="'normal'">
                            <bk-input v-model="formData.cluster_name" placeholder="请录入集群在平台的名称，禁止存在特殊符号"></bk-input>
                            <p class="mt5 mb0 f12" slot="tip"></p>
                        </bk-form-item>
                        <bk-form-item label="版本选择" :required="true" :property="'cluster_version'" :error-display-type="'normal'">
                            <bk-select v-model="formData.cluster_version" searchable placeholder="选择对应的hadoop版本">
                                <bk-option v-for="option in versionList"
                                    :key="option.id"
                                    :id="option.id"
                                    :name="option.name">
                                </bk-option>
                            </bk-select>
                        </bk-form-item>
                        <bk-form-item label="集群启动账号" :required="true" :property="'cluster_user'" :error-display-type="'normal'">
                            <bk-input v-model="formData.cluster_user" placeholder="请输入集群启动进程账号"></bk-input>
                            <p class="mt5 mb0 f12" slot="tip"></p>
                        </bk-form-item>

                        <bk-form-item label="集群安装目录" :required="true" :property="'base_dir'" :error-display-type="'normal'">
                            <bk-input v-model="formData.base_dir" placeholder="请输入集群组件的安装目录，所有组件必须存放在启动账号有权限的同一目录下"></bk-input>
                            <p class="mt5 mb0 f12" slot="tip"></p>
                        </bk-form-item>
                        <bk-form-item label="ssh远处端口" :required="true" :property="'ssh_port'" :error-display-type="'normal'">
                            <bk-input v-model="formData.ssh_port" placeholder="请输入集群机器远程端口号"></bk-input>
                            <p class="mt5 mb0 f12" slot="tip"></p>
                        </bk-form-item>
                        <bk-form-item label="域名映射信息" :required="true" :property="'hostname_list'" :error-display-type="'normal'">
                            <bk-input type="textarea" v-model="formData.hostname_list" placeholder="请输入每个节点的域名信息，输入格式:ip/dnsname，如果多个信息可以用空格隔开"></bk-input>
                        </bk-form-item>
                        <bk-form-item>
                            <bk-button ext-cls="mr5" theme="default" @click="reset" style="margin-top: 20px; margin-bottom: 20px;">重置</bk-button>
                            <bk-button ext-cls="mr5" theme="success" @click="last" style="margin-top: 20px; margin-bottom: 20px;">上一步</bk-button>
                            <bk-button ext-cls="mr5" theme="primary" @click.stop.prevent="checkData1" :loading="isChecking" style="margin-top: 20px; margin-bottom: 20px;">下一步</bk-button>
        
                        </bk-form-item>
                    </bk-form>
                    <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm2" v-show="curProcess === 2">
                        <bk-form-item label="hdfs白名单路径" :required="true" :property="'hdfs_includes'" :error-display-type="'normal'">
                            <bk-input v-model="formData.hdfs_includes" placeholder="请输入已配置好的hdfs的白名单配置绝对路径"></bk-input>
                            <p class="mt5 mb0 f12" slot="tip"></p>
                        </bk-form-item>
                        <bk-form-item label="hdfs黑名单路径" :required="true" :property="'hdfs_excludes'" :error-display-type="'normal'">
                            <bk-input v-model="formData.hdfs_excludes" placeholder="请输入已配置好的hdfs的白名单配置绝对路径"></bk-input>
                            <p class="mt5 mb0 f12" slot="tip"></p>
                        </bk-form-item>
                        <bk-form-item label="hdfs数据目录" :required="true" :property="'hdfs_dir'" :error-display-type="'normal'">
                            <bk-input v-model="formData.hdfs_dir" placeholder="请输入已配置好的hdfs数据盘列表，多个目录可以用英文逗号或者空格隔开"></bk-input>
                            <p class="mt5 mb0 f12" slot="tip"></p>
                        </bk-form-item>
                        <bk-form-item label="hdfs副本数量" :required="true" :property="'repl_number'" :error-display-type="'normal'">
                            <bk-input v-model="formData.repl_number" placeholder="请输入集群已配置好的副本数量">
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-input>
                        </bk-form-item>
                        <bk-form-item label="NameNode" :required="true" :property="'namenode'" :error-display-type="'normal'">
                            <bk-input type="textarea" v-model="formData.namenode" placeholder="请输入对应的NameNode节点IP信息"></bk-input>
                        </bk-form-item>
                        <bk-form-item label="StandbyNameNode" :required="true" :property="'standbynamenode'" :error-display-type="'normal'">
                            <bk-input type="textarea" v-model="formData.standbynamenode" placeholder="请输入对应的StandNameNode节点IP信息"></bk-input>
                        </bk-form-item>
                        <bk-form-item label="DataNode" :required="true" :property="'datanode'" :error-display-type="'normal'">
                            <bk-input type="textarea" v-model="formData.datanode" placeholder="请输入对应的DataNode节点IP列表,多个可以用英文逗号或者空格隔开"></bk-input>
                        </bk-form-item>
                        <bk-form-item label="JournalNode" :required="true" :property="'journalnode'" :error-display-type="'normal'">
                            <bk-input type="textarea" v-model="formData.journalnode" placeholder="请输入对应的JournalNode节点IP列表, 多个可以用英文逗号或者空格隔开"></bk-input>
                        </bk-form-item>
                        <bk-form-item label="ZooKeeperNode" :required="true" :property="'zookeepernode'" :error-display-type="'normal'">
                            <bk-input type="textarea" v-model="formData.zookeepernode" placeholder="请输入对应的ZooKeeperNode节点IP列表,多个可以用英文逗号或者空格隔开"></bk-input>
                        </bk-form-item>
                        <bk-form-item>
                            <bk-button ext-cls="mr5" theme="default" @click="reset" style="margin-top: 20px; margin-bottom: 20px;">重置</bk-button>
                            <bk-button ext-cls="mr5" theme="success" @click="last" style="margin-top: 20px; margin-bottom: 20px;">上一步</bk-button>
                            <bk-button ext-cls="mr5" theme="primary" @click.stop.prevent="checkData2" :loading="isChecking" style="margin-top: 20px; margin-bottom: 20px;">下一步</bk-button>
        
                        </bk-form-item>
                    </bk-form>
                    <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm3" v-show="curProcess === 3">
                        <bk-form-item label="ResourceManagerNode">
                            <bk-input type="textarea" v-model="formData.resourcemanagernode" placeholder="请输入ResourceManagerNode节点IP列表"></bk-input>
                        </bk-form-item>
                        <bk-form-item label="NodeManagerNode">
                            <bk-input type="textarea" v-model="formData.nodemanagernode" placeholder="请输入NodeManagerNode节点IP列表"></bk-input>
                        </bk-form-item>
                        <bk-form-item>
                            <bk-button ext-cls="mr5" theme="default" @click="reset" style="margin-top: 20px; margin-bottom: 20px;">重置</bk-button>
                            <bk-button ext-cls="mr5" theme="success" @click="last" style="margin-top: 20px; margin-bottom: 20px;">上一步</bk-button>
                            <bk-button ext-cls="mr5" theme="primary" @click.stop.prevent="checkData3" :loading="isChecking" style="margin-top: 20px; margin-bottom: 20px;">下一步</bk-button>
        
                        </bk-form-item>
                    </bk-form>
                    <bk-form :label-width="200" :model="formData" v-show="curProcess === 4">
                        <bk-form-item label="集群描述">
                            <bk-input type="textarea" v-model="formData.desc"></bk-input>
                        </bk-form-item>
                        <bk-form-item>
                            <bk-button ext-cls="mr5" theme="default" @click="reset" style="margin-top: 20px; margin-bottom: 20px;">重置</bk-button>
                            <bk-button ext-cls="mr5" theme="success" @click="last" style="margin-top: 20px; margin-bottom: 20px;">上一步</bk-button>
                            <bk-button ext-cls="mr5" theme="primary" @click="submitData" style="margin-top: 20px; margin-bottom: 20px;">提交</bk-button>
        
                        </bk-form-item>
                    </bk-form>
                </bk-col>
            </bk-row>
            <bk-row style="margin-top: 50px;">
                
            </bk-row>
        </bk-container>
    </div>
</template>
<script>
    import { bkProcess, bkButton } from '@tencent/bk-magic-vue'

    export default {
        components: {
            bkProcess,
            bkButton
        },
        data () {
            return {
                curProcess: 1,
                dataList: [
                    {
                        content: '基础配置',
                        isLoading: true
                    },
                    {
                        content: 'HDFS配置',
                        isLoading: true
                    },
                    {
                        content: 'YARN配置',
                        isLoading: true
                    },
                    {
                        content: '辅助信息'
                    }
                ],
                formData: {
                    app_id: '',
                    app: '',
                    cluster_name: '',
                    cluster_version: '',
                    cluster_user: '',
                    base_dir: '',
                    hdfs_includes: '',
                    hdfs_excludes: '',
                    hdfs_dir: '',
                    repl_number: '',
                    ssh_port: '',
                    namenode: '',
                    standbynamenode: '',
                    datanode: '',
                    journalnode: '',
                    zookeepernode: '',
                    resourcemanagernode: '',
                    nodemanagernode: '',
                    add_type: '0',
                    hostname_list: '',
                    desc: ''
                },
                versionList: [
                    {
                        id: '2.6.0',
                        name: '2.6.0'
                    },
                    {
                        id: '3.2.0',
                        name: '3.2.0'
                    },
                    {
                        id: 'other',
                        name: '其他'
                    }
                ],
                appinfo: [],
                isChecking: false,
                yesnolist: [
                    {
                        id: '0',
                        name: '否'
                    },
                    {
                        id: '1',
                        name: '是'
                    }
                ],
                rules: {
                    app_id: [
                        {
                            required: true,
                            message: '选择对应业务',
                            trigger: 'blur'
                        }
                    ],
                    cluster_name: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            min: 3,
                            message: function (val) {
                                return `${val}不能小于3个字符`
                            },
                            trigger: 'blur'
                        },
                        {
                            max: 128,
                            message: '不能多于128个字符',
                            trigger: 'blur'
                        },
                        {
                            regex: /^[A-Za-z0-9]+$/,
                            message: '不能存在特殊符号',
                            trigger: 'blur'
                        }
                        
                    ],
                    cluster_version: [
                        {
                            required: true,
                            message: '选择对应的安装版本',
                            trigger: 'blur'
                        }
                    ],
                    cluster_user: [
                        {
                            required: true,
                            message: '选择对应的部署用户',
                            trigger: 'blur'
                        },
                        {
                            regex: /^[A-Za-z0-9]+$/,
                            message: '不能存在特殊符号',
                            trigger: 'blur'
                        }
                    ],
                    base_dir: [
                        {
                            required: true,
                            message: '输入安装目录，只能输入一个目录',
                            trigger: 'blur'
                        },
                        {
                            regex: /^\/(\w+\/?)+$/,
                            message: '输入正确绝对路径表达方式，如: /xxxx/xxxx/，目录名称支持数字+字符+下划线组合',
                            trigger: 'blur'
                        }
                    ],
                    hdfs_includes: [
                        {
                            required: true,
                            message: '输入安装目录，只能输入一个目录',
                            trigger: 'blur'
                        },
                        {
                            regex: /^\/(\w+\/?)+$/,
                            message: '输入正确绝对路径表达方式，如: /xxxx/xxxx/，目录名称支持数字+字符+下划线组合',
                            trigger: 'blur'
                        }
                    ],
                    hdfs_excludes: [
                        {
                            required: true,
                            message: '输入安装目录，只能输入一个目录',
                            trigger: 'blur'
                        },
                        {
                            regex: /^\/(\w+\/?)+$/,
                            message: '输入正确绝对路径表达方式，如: /xxxx/xxxx/，目录名称支持数字+字符+下划线组合',
                            trigger: 'blur'
                        }
                    ],
                    hdfs_dir: [
                        {
                            required: true,
                            message: '输入hdfs数据存储目录',
                            trigger: 'blur'
                        }
                    ],
                    repl_number: [
                        {
                            required: true,
                            message: '输入hdfs文件副本数',
                            trigger: 'blur'
                        }
                    ],
                    ssh_port: [
                        {
                            required: true,
                            message: '输入远程端口号',
                            trigger: 'blur'
                        },
                        {
                            regex: /^([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$/,
                            message: '输入标准端口号访问：1-65535',
                            trigger: 'blur'
                        }
                    ],
                    namenode: [
                        {
                            required: true,
                            message: '请输入namenode',
                            trigger: 'blur'
                        }
                    ],
                    standbynamenode: [
                        {
                            required: true,
                            message: '请输入standbynamenode',
                            trigger: 'blur'
                        }
                    ],
                    datanode: [
                        {
                            required: true,
                            message: '请输入datanode',
                            trigger: 'blur'
                        }
                    ],
                    journalnode: [
                        {
                            required: true,
                            message: '请输入journalnode',
                            trigger: 'blur'
                        }
                    ],
                    zookeepernode: [
                        {
                            required: true,
                            message: '请输入zookeepernode',
                            trigger: 'blur'
                        }
                    ],
                    hostname_list: [
                        {
                            required: true,
                            message: '域名映射信息表不能为空',
                            trigger: 'blur'
                        }
                    ]

                }
            }
        },
        watch: {
            'formData.app_id': function (val) {
                this.formData.app_id = val
                this.appinfo.forEach(item => {
                    if (this.formData.app_id === item.bk_biz_id) {
                        this.formData.app = item.bk_biz_name
                        return true
                    }
                }
                )
            }
        },
        created () {
            this.getInfoData()
        },
        methods: {
            closeDialog () {
                this.$router.push(
                    {
                        path: 'hadooprecord'
                    }
                )
            },
            changeProcess (process, data) {
                console.log(process)
                console.log(data)
            },
            async getInfoData () {
                try {
                    const res = await this.$store.dispatch('hadoop/getAppInfoData', {}, { fromCache: true })
                    this.appinfo = res.data.info
                } catch (e) {
                    console.error(e)
                }
            },
            async submitData () {
                try {
                    const res = await this.$store.dispatch('hadoop/inputHadoopCluster', this.formData)
                    console.log(res)
                    if (res.code === 0) {
                        const config = { theme: 'success' }
                        config.message = '提交成功, 请到HDFS执行记录中查看录入详情！'
                        config.offsetY = 80
                        this.$bkMessage(config)
                        // this.closeDialog()
                    } else {
                        const config = { theme: 'error' }
                        config.message = res.message
                        config.offsetY = 80
                        this.$bkMessage(config)
                    }
                } catch (e) {
                    console.log(e)
                }
            },
            checkData1 () {
                this.isChecking = true
                this.$refs.validateForm1.validate().then(validator => {
                    this.next()
                    this.isChecking = false
                }, validator => {
                    this.isChecking = false
                })
            },
            checkData2 () {
                this.isChecking = true
                this.$refs.validateForm2.validate().then(validator => {
                    this.next()
                    this.isChecking = false
                }, validator => {
                    this.isChecking = false
                })
            },
            checkData3 () {
                this.isChecking = true
                this.$refs.validateForm3.validate().then(validator => {
                    this.next()
                    this.isChecking = false
                }, validator => {
                    this.isChecking = false
                })
            },
            last () {
                if (this.curProcess !== 1) {
                    this.curProcess--
                }
            },
            next () {
                if (this.curProcess < this.dataList.length) {
                    this.curProcess++
                }
            },
            reset () {
                this.curProcess = 1
            }
        }
    }
</script>
