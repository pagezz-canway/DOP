<template>
    <div class="wrapper">
        <bk-container :col="2">
            <bk-row>
                <bk-col :span="1">
                    <bk-card title="集群详情" style="height: 300px">
                        <p>集群名称: {{ cluster_detail.cluster_name }}</p>
                        <p>集群版本: {{ cluster_detail.cluster_version }}</p>
                        <p>集群状态: {{ cluster_detail.cluster_status }}</p>
                        <p>添加模式: {{ cluster_detail.add_type }}</p>
                        <p>容量详情: null </p>
                    </bk-card>
                </bk-col>
                <bk-col :span="1">
                    <bk-card title="集群配置" style="height: 300px">
                        <p>启动用户: {{ cluster_detail.cluster_user }} </p>
                        <p>安装目录: {{ cluster_detail.base_dir }} </p>
                        <p>数据目录: {{ cluster_detail.hdfs_data_dir }}</p>
                        <p>副本设置: {{ cluster_detail.hdfs_repl_num }}</p>
                        <p>远程端口: {{ cluster_detail.ssh_port }}</p>
                        <p>hdfs白名单路径: {{ cluster_detail.hdfs_includes }}</p>
                        <p>hdfs黑名单路径: {{ cluster_detail.hdfs_excludes }}</p>
                    </bk-card>
                </bk-col>
            </bk-row>
            <bk-row style="margin-top: 20px;">
                <bk-tab :active.sync="active" type="unborder-card" :before-toggle="getHadoopDetail">
                    <bk-tab-panel
                        v-for="(panel, index) in panels"
                        v-bind="panel"
                        :key="index">
                    </bk-tab-panel>
                </bk-tab>
            </bk-row>
            
            <bk-row style="margin-top: 20px;">
                <bk-table :data="data">
                    <bk-table-column type="selection" width="60"></bk-table-column>
                    <bk-table-column label="进程名称" prop="process_name" sortable></bk-table-column>
                    <bk-table-column label="进程ip" prop="process_ip"></bk-table-column>
                    <bk-table-column label="进程域名" prop="process_hostname"></bk-table-column>
                    <bk-table-column label="进程版本" prop="package_version"></bk-table-column>
                    <bk-table-column label="进程状态" prop="process_status"></bk-table-column>
                    <bk-table-column label="创建时间" prop="create_time"></bk-table-column>
                </bk-table>
            
            </bk-row>
        </bk-container>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                id: '',
                cluster_detail: {},
                data: [],
                panels: [
                    { name: 'hdfs', label: 'HDFS节点信息' },
                    { name: 'yarn', label: 'YARN节点信息' }
                ],
                active: 'mission'
                
            }
        },
        beforeRouteLeave (to, from, next) {
            localStorage.removeItem('condition')
            next()
        },
        mounted () {
            const condition = localStorage.getItem('condition')
            if (condition != null) {
                this.cluster_detail = JSON.parse(condition)
            } else {
                this.cluster_detail = this.$route.query.row
            }
            this.getHadoopDetail('hdfs')
            localStorage.setItem('condition', JSON.stringify(this.cluster_detail))
        },
        methods: {
            async getHadoopDetail (panelName) {
                try {
                    const param = { 'cluster_id': this.cluster_detail.cluster_id, 'hadoop_group_name': panelName }
                    const res = await this.$store.dispatch('hadoop/getHadoopDetail', param)
                    this.data = res.data
                } catch (e) {
                    console.error(e)
                }
                return panelName
            }
        }

    }
</script>
<style lang="postcss">
    .bk-card-body {
        p {
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 8px;
            &:last-child {
                margin-bottom: 0;
            }
        }
    }
</style>
