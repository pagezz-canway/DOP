<template>
    <div class="wrapper">
        <div class="fr clearfix mb15">
            <bk-form form-type="inline">
                <bk-form-item label="集群名称">
                    <bk-input placeholder="集群名称" v-model="formData.cluster_name"></bk-input>
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
            <bk-table-column label="集群id" prop="cluster_id"></bk-table-column>
            <bk-table-column label="业务" prop="app"></bk-table-column>
            <bk-table-column label="集群名称" prop="cluster_name"></bk-table-column>
            <bk-table-column label="添加模式" prop="add_type"
                :filters="typeFilters"
                :filter-method="typeFiltersMethod"
                :filter-multiple="false"></bk-table-column>
            <bk-table-column label="集群状态" prop="cluster_status"></bk-table-column>
            <bk-table-column label="集群版本" prop="cluster_version"></bk-table-column>
            <bk-table-column label="创建人" prop="create_user"></bk-table-column>
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
        components: {
        },
        data () {
            return {
                typeFilters: [
                    { text: '平台新建', value: '平台新建' },
                    { text: '平台录入', value: '平台录入' }
                ],
                formData: {
                    cluster_name: ''
                },
                temptableData: [],
                size: 'small',
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10
                },
                hdfsInfo: ''
            }
        },
        computed: {
            tableData: function () {
                const start = (this.pagination.current - 1) * this.pagination.limit
                const end = start + this.pagination.limit < this.pagination.count ? start + this.pagination.limit : this.pagination.count
                return this.temptableData.slice(start, end)
            }
        },
        created () {
            this.getHadoopData(this.formData)
        },
        methods: {
            typeFiltersMethod (value, row, column) {
                const property = column.property
                return row[property] === value
            },
            getClusterDetail (row) {
                this.$router.push(
                    {
                        path: 'hadoopdetail', query: { 'row': row }
                    }
                )
            },
            async getHadoopData (param) {
                try {
                    const res = await this.$store.dispatch('hadoop/getHadoopData', param, { fromCache: true })
                    this.temptableData = res.data
                    this.pagination.count = res.data.length
                } catch (e) {
                    console.error(e)
                }
            },
            async getHDFSStorage (row) {
                try {
                    this.customSettings.isShow = true
                    this.hdfsInfo = '后台查询中, 请稍等……'
                    const param = { 'namenode': row.namenode, 'app_id': row.app_id }
                    const res = await this.$store.dispatch('hadoop/getHDFSStorage', param, { fromCache: true })
                    // console.log(res)
                    this.hdfsInfo = res.data
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
                this.getHadoopData(this.formData)
            }
            
        }
    }
</script>
