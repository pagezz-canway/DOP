<template>
    
    <div class="example1-wrapper">
        <bk-container :col="2">
            <bk-row>
                <bk-col :span="1">
                    <bk-card title="集群信息" style="height: 300px">
                        <p>集群名称: {{ cluster_detail.cluster_name }}</p>
                        <p>集群版本: {{ cluster_detail.version }}</p>
                        <p>集群状态: {{ cluster_detail.cluster_status }}</p>
                        <p>添加模式: {{ cluster_detail.add_type }}</p>
                        <p>集群描述: {{ cluster_detail.description }}</p>
                    </bk-card>
                </bk-col>
                <bk-col :span="1">
                    <bk-card title="集群配置" style="height: 300px">
                        <p>master节点数量: {{ cluster_detail.master_cnt }} </p>
                        <p>data节点数量: {{ cluster_detail.data_cnt }} </p>
                        <p>cold节点数量: {{ cluster_detail.cold_cnt }}</p>
                        <p>协调节点数量: {{ cluster_detail.client_cnt }}</p>
                        <p>http端口: {{ cluster_detail.http_port }}</p>

                    </bk-card>
                </bk-col>
            </bk-row>
            <bk-row style="margin-top: 20px;">
                <bk-table :data="tableData">
                    <bk-table-column label="业务ID" prop="app_id"></bk-table-column>
                    <bk-table-column label="集群名" prop="cluster_name"></bk-table-column>
                    <bk-table-column label="节点名称" prop="node_name"></bk-table-column>
                    <bk-table-column label="ip" prop="ip"></bk-table-column>
                    <bk-table-column label="节点角色" prop="role"></bk-table-column>
                    <bk-table-column label="版本" prop="version"></bk-table-column>
                    <bk-table-column label="设备类型" prop="device_class"></bk-table-column>
                    <bk-table-column label="硬件信息" prop="hard_memo"></bk-table-column>
                </bk-table>
            </bk-row>
        </bk-container>
        
    </div>
</template>

<script>
    export default {
        components: {},
        data () {
            return {
                cluster_detail: {},
                tableData: []
                
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
            this.getEsNodeInfo()
            localStorage.setItem('condition', JSON.stringify(this.cluster_detail))
        },
        methods: {
            async getEsNodeInfo () {
                try {
                    const param = { 'cluster_name': this.cluster_detail.cluster_name }
                    const res = await this.$store.dispatch('es/getEsNodeInfo', param)
                    this.tableData = res.data
                } catch (e) {
                    console.error(e)
                }
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
