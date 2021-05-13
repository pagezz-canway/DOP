<template>
    <div class="wrapper">
        <bk-container :col="12">
            <bk-row>
                <bk-col :span="7">
                    <div style="width: 600px;">
                        <bk-form :label-width="200" :model="formData" :rules="rules" ref="validateForm1">
                            <bk-form-item label="业务名称" :required="true" :property="'app_id'" :error-display-type="'normal'">
                                <bk-select v-model="formData.app_id" searchable>
                                    <bk-option v-for="option in appinfo"
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
                            <bk-form-item label="版本选择" :required="true" :property="'cluster_version'" :error-display-type="'normal'">
                                <bk-select v-model="formData.cluster_version" searchable>
                                    <bk-option v-for="option in versionList"
                                        :key="option.id"
                                        :id="option.id"
                                        :name="option.name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            <bk-form-item label="集群启动账号" :required="true" :property="'cluster_user'" :error-display-type="'normal'">
                                <bk-input v-model="formData.cluster_user" :readonly="true" placeholder="请输入集群启动账号，默认是hadoop用户"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>

                            <bk-form-item label="集群安装目录" :required="true" :property="'base_dir'" :error-display-type="'normal'">
                                <bk-input v-model="formData.base_dir" :readonly="true" placeholder="请输入集群组件的安装目录，默认存放到/data/hadoop_env下"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="hdfs白名单路径" :required="true" :property="'hdfs_includes'" :error-display-type="'normal'">
                                <bk-input v-model="formData.hdfs_includes" :readonly="true" placeholder="请输入hdfs的白名单配置路径"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="hdfs黑名单路径" :required="true" :property="'hdfs_excludes'" :error-display-type="'normal'">
                                <bk-input v-model="formData.hdfs_excludes" :readonly="true" placeholder="请输入hdfs的黑名单配置路径"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="hdfs数据目录" :required="true" :property="'hdfs_dir'" :error-display-type="'normal'">
                                <bk-input v-model="formData.hdfs_dir" placeholder="请输入hdfs数据盘列表，多个目录可以用英文逗号隔开"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="hdfs副本数量" :required="true" :property="'repl_number'" :error-display-type="'normal'">
                                <bk-select v-model="formData.repl_number" placeholder="输入副本数量" searchable>
                                    <bk-option v-for="option in replnumberlist"
                                        :key="option.id"
                                        :id="option.id"
                                        :name="option.name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                            
                            <bk-form-item label="ssh远程端口" :required="true" :property="'ssh_port'" :error-display-type="'normal'">
                                <bk-input v-model="formData.ssh_port" placeholder="输入机器远程端口号,默认22"></bk-input>
                                <p class="mt5 mb0 f12" slot="tip"></p>
                            </bk-form-item>
                            <bk-form-item label="NameNode" :required="true" :property="'namenode'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.namenode" placeholder="请输入NameNode节点IP列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="StandbyNameNode" :required="true" :property="'standbynamenode'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.standbynamenode" placeholder="请输入StandNameNode节点IP列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="DataNode" :required="true" :property="'datanode'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.datanode" placeholder="请输入DataNode节点IP列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="JournalNode" :required="true" :property="'journalnode'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.journalnode" placeholder="请输入JournalNode节点IP列表, 至少需要三台机器"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="ZooKeeperNode" :required="true" :property="'zookeepernode'" :error-display-type="'normal'">
                                <bk-input type="textarea" v-model="formData.zookeepernode" placeholder="请输入ZooKeeperNode节点IP列表,至少需要三台机器"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="ResourceManagerNode">
                                <bk-input type="textarea" v-model="formData.resourcemanagernode" placeholder="请输入ResourceManagerNode节点IP列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="NodeManagerNode">
                                <bk-input type="textarea" v-model="formData.nodemanagernode" placeholder="请输入NodeManagerNode节点IP列表"></bk-input>
                            </bk-form-item>
                            <bk-form-item label="集群描述">
                                <bk-input type="textarea" v-model="formData.desc"></bk-input>
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
                        <h2>HDFS集群新建说明</h2>
                        <p>1> 最小集群需要3台机器</p>
                        <p>2> namenode节点和standbynamenode节点,需要部署到不同的IP上</p>
                        <p>3> 部署的机器IP需要先安装gse_agent,具有业务job执行权限</p>
                        <p>4> datanode节点必须大于或等于副本数量</p>
                        <p>4> 部署任务耗时3分钟左右,后台异步部署，结果请到<a href="/hadoop/hadooprecord">HDFS执行记录中查看</a></p>
                        <p>5> HDFS集群默认分块大小：128MB</p>
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
                    app_id: '',
                    app: '',
                    cluster_name: '',
                    cluster_version: '',
                    cluster_user: 'hadoop',
                    base_dir: '/data/hadoop_env',
                    hdfs_includes: '/data/hadoop_env/hadoop/etc/hadoop/includes',
                    hdfs_excludes: '/data/hadoop_env/hadoop/etc/hadoop/excludes',
                    hdfs_dir: '',
                    clean_data_force: '',
                    repl_number: '',
                    ssh_port: '',
                    namenode: '',
                    standbynamenode: '',
                    datanode: '',
                    journalnode: '',
                    zookeepernode: '',
                    resourcemanagernode: '',
                    nodemanagernode: '',
                    add_type: '1',
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
                    }
                ],
                appinfo: [],
                replnumberlist: [
                    {
                        id: '1',
                        name: '1'
                    },
                    {
                        id: '2',
                        name: '2'
                    },
                    {
                        id: '3',
                        name: '3'
                    }
                ],
                isChecking: false,
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
                            required: false,
                            message: '请输入zookeepernode',
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
                    const res = await this.$store.dispatch('hadoop/createHadoopCluster', this.formData)
                    if (res.code === 0) {
                        this.isChecking = false
                        const config = { theme: 'success' }
                        config.message = '提交成功, 跳转到HDFS执行记录中查看部署详情！'
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
