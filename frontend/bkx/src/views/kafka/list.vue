<template>
    <div class="example1-wrapper">
        <div class="fr clearfix mb15">
            <bk-form form-type="inline">
                <bk-form-item label="名称">
                    <bk-input placeholder="名称" v-model="formData.cluster_name"></bk-input>
                </bk-form-item>
                <bk-form-item>
                    <bk-button @click="search" theme="primary" title="提交">搜索</bk-button>
                </bk-form-item>
                <bk-form-item>
                    <bk-button @click="output" theme="primary" title="导出">导出本页数据</bk-button>
                </bk-form-item>
            </bk-form>
        </div>
        <bk-table id="mytable" style="margin-top: 15px;"
            :data="tableData"
            :size="size"
            :pagination="pagination"
            @row-mouse-enter="handleRowMouseEnter"
            @row-mouse-leave="handleRowMouseLeave"
            @page-change="handlePageChange"
            @page-limit-change="handleLimitChange">
            <bk-table-column label="集群id" prop="id"></bk-table-column>
            <bk-table-column label="业务名称" prop="app"></bk-table-column>
            <bk-table-column label="集群名称" prop="cluster_name"></bk-table-column>
            <bk-table-column label="添加模式" prop="add_type"
                :filters="typeFilters"
                :filter-method="typeFiltersMethod"
                :filter-multiple="false"></bk-table-column>
            <bk-table-column label="集群状态" prop="cluster_status"></bk-table-column>
            <bk-table-column label="集群版本" prop="version"></bk-table-column>
            <bk-table-column label="创建人" prop="created_by"></bk-table-column>
            <bk-table-column label="创建时间" prop="create_time"></bk-table-column>
            <bk-table-column label="操作">
                <template slot-scope="props">
                    <bk-button theme="primary" text @click="getClusterDetail(props.row)">集群详情</bk-button>
                </template>
            </bk-table-column>
        </bk-table>
    </div>
</template>

<script>
    import FileSaver from 'file-saver'
    import XLSX from 'xlsx'
    export default {
        components: {},
        data () {
            return {
                typeFilters: [
                    { text: '平台新建', value: '平台新建' },
                    { text: '平台录入', value: '平台录入' }
                ],
                formData: {
                    cluster_name: ''
                },
                tableData: [],
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10
                },
                apps: []
            }
        },
        created () {
            this.init()
        },
        methods: {
            init () {
                this.getKafkaData(this.formData)
            },
            getClusterDetail (row) {
                this.$router.push(
                    {
                        path: 'broker', query: { 'row': row }
                    }
                )
            },
            async getKafkaData (param) {
                try {
                    const res = await this.$store.dispatch('kafka/getKafkaData', param)
                    this.tableData = res.data
                    this.pagination.count = res.data.length
                } catch (e) {
                    console.error(e)
                }
            },
            toggleTableSize () {
                const size = ['small', 'medium', 'large']
                const index = (size.indexOf(this.size) + 1) % 3
                this.size = size[index]
            },
            handlePageChange (page) {
                this.pagination.current = page
            },
            handleLimitChange (limit) {
                this.pagination.limit = limit
                this.handlePageChange(1)
            },
            output () {
                /* generate workbook object from table */
                const wb = XLSX.utils.table_to_book(document.querySelector('#mytable')) // mytable为表格的id名
                /* get binary string as output */
                const wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
                try {
                    FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), 'sheet.xlsx')
                } catch (e) {
                    if (typeof console !== 'undefined') console.log(e, wbout)
                }
                return wbout
            },
            search () {
                this.getKafkaData(this.formData)
            }
        }
    }
</script>
