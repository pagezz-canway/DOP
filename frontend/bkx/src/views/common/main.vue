<template>
    <div class="main-grid">
        <div class="wrapper flex">
            
            <bk-container flex :col="15">
                <bk-row>
                    <bk-col :span="6"><div class="home-card-layout">
                        <div class="card-title">平台公告</div>
                        <div>
                            <bk-swiper :list="list" ext-cls="swiper-boby" :width="500">
                                <template slot-scope="item">
                                    <div class="swiper-content">
                                        <p>{{item.data}}</p>
                                    </div>
                                </template>
                            </bk-swiper>
                        </div>
   
                    </div></bk-col>
                    <bk-col :span="9">
                        <bk-row>
                            <bk-col :span="3">
                                <div class="home-card-layout">
                                    <div class="card-title">各组件集群数量比例</div>
                                    <div id="clusternum" class="echart_style"></div>
                                </div>
                            </bk-col>
                            <bk-col :span="3">
                                <div class="home-card-layout">
                                    <div class="card-title">各组件投入机器数量比例</div>
                                    <div id="machinenum" class="echart_style"></div>
                                </div>
                            </bk-col>
                                
                            <bk-col :span="3">
                                <div class="home-card-layout">
                                    <div class="card-title">各组件执行任务数量比例</div>
                                    <div id="tasknum" class="echart_style"></div>
                                </div>
                            </bk-col>
                        </bk-row>
                        
                    </bk-col>
                </bk-row>
                <bk-row>
                    <bk-col :span="9">
                        <bk-row>
                            <bk-col :span="12">
                                <div class="home-card-layout">
                                    <div id="es_chart" class="card-title">ES各业务资源统计TOP5</div>
                                    <div id="es_bar_top_5" class="bar-style"></div>
                                </div>
                            </bk-col>
                        </bk-row>
                        <bk-row>
                            <bk-col :span="12">
                                <div class="home-card-layout">
                                    <div class="card-title">Hadoop各业务资源统计TOP5</div>
                                    <div id="hadoop_bar_top_5" class="bar-style"></div>
                                </div>
                            </bk-col>
                        </bk-row>
                        <bk-row>
                            <bk-col :span="12">
                                <div class="home-card-layout">
                                    <div class="card-title">Kafka各业务资源统计TOP5</div>
                                    <div id="kafka_bar_top_5" class="bar-style"></div>
                                </div>
                            </bk-col>
                        </bk-row>
                    </bk-col>
                    
                    <bk-col :span="6">
                        <bk-row>
                            <bk-col :span="12">
                                <div class="home-card-layout">
                                    <a href="/" class="work-statistics-box">
                                        <div class="work-flag">
                                            <bk-icon type="pc-shape" svg style="width: 1em; height: 1.7em; font-size: xxx-large; color:#5470c6">
                                            </bk-icon>
                                        </div>
                                        <div class="work-total"><span>{{ runTask }}</span></div>
                                        <div class="work-name"><span>正在执行任务数</span></div>
                                    </a>
                                    
                                </div>
                            </bk-col>
                        </bk-row>
                        <bk-row>
                            <bk-col :span="12">
                                <div class="home-card-layout">
                                    <div class="card-title">
                                        <p>异常任务信息列表</p>
                                    </div>
                  
                                    <div class="history-record-box">
                                        <bk-table
                                            :data="failTaskData"
                                            :size="size"
                                            :outer-border="false"
                                            :header-border="false"
                                            :header-cell-style="{ background: '#fff' }"
                                            :pagination="pagination"
                                            @page-change="handlePageChange">
                                            <bk-table-column label="业务名称" prop="app_name"></bk-table-column>
                                            <bk-table-column label="组件名称" prop="db_name"></bk-table-column>
                                            <bk-table-column label="任务类型" prop="task_type"></bk-table-column>
                                            <bk-table-column label="操作人" prop="op_user"></bk-table-column>
                                            <bk-table-column label="创建时间" prop="create_time" sortable></bk-table-column>
                                            <bk-table-column label="操作">
                                                <template slot-scope="props">
                                                    <bk-button theme="danger" size="small" @click="reset(props.row)">查看</bk-button>
                                                </template>
                                            </bk-table-column>
                                        </bk-table>
                                    </div>
                                    
                                </div>
                            </bk-col>
                        </bk-row>
                    </bk-col>
                </bk-row>
            </bk-container>
        </div>
    </div>
</template>

<script>
    import * as echarts from 'echarts'
    import elementResize from 'element-resize-detector'
    export default {
      
        data () {
            return {
                esTopChart: null,
                hadoopTopChart: null,
                kafkaTopChart: null,
                clsuterChart: null,
                taskChart: null,
                machineChart: null,
                runTask: 10,
                size: 'small',
                list: [
                    'DOP平台基于蓝鲸开发，集成了ES、Hadoop、Kafka等常用大数据组件，\n旨在提高大数据组件的运维效率和安全效率',
                    '平台不仅提供”集群新建“模式来管控属于你的业务的集群，\n还能通过”集群录入“模式来管理非平台本身创建的集群',
                    '待部署的机器必须所属于你选择的业务,\n并且需要安装JOB平台GSE权限',
                    '用户若在部署、录入、查询集群过程中无法选择到对应的业务名称，\n则需要查看配置平台和权限中心是否有该业务的权限',
                    '目前平台对通过录入的第三方集群尚未适配管控功能，未来版本会开放，敬请期待'
                    
                ],
                failTaskData: [
                    {
                        app_name: '业务1',
                        db_name: 'hadoop',
                        task_type: '创建中',
                        op_user: 'admin',
                        create_time: '2018-05-25 15:02:24'
                    },
                    {
                        app_name: '业务2',
                        db_name: 'hadoop',
                        task_type: '创建中',
                        op_user: 'admin',
                        create_time: '2018-05-26 15:02:24'
                    }
                ],
                es_data: [
                    { value: 1048, name: '业务1' },
                    { value: 735, name: '业务2' },
                    { value: 580, name: '业务3' },
                    { value: 735, name: '业务4' },
                    { value: 580, name: '业务5' }
                ],
                hadoop_data: [
                    { value: 108, name: '业务1' },
                    { value: 735, name: '业务2' },
                    { value: 580, name: '业务3' },
                    { value: 735, name: '业务4' },
                    { value: 580, name: '业务5' }
                ],
                kafka_data: [
                    { value: 18, name: '业务1' },
                    { value: 735, name: '业务2' },
                    { value: 580, name: '业务3' },
                    { value: 75, name: '业务4' },
                    { value: 580, name: '业务5' }],
                cluster_pie_data: {
                    text: '各组件集群数量比例',
                    data: [
                        { value: 1048, name: 'ES集群数量' },
                        { value: 735, name: 'Hadoop集群数量' },
                        { value: 580, name: 'Kafka集群数量' }
                    ]
                },
                machine_pie_data:
                    {
                        text: '各组件机器数量比例',
                        data: [
                            { value: 18, name: 'ES投入机器数量' },
                            { value: 50, name: 'Hadoop投入机器数量' },
                            { value: 77, name: 'Kafka投入机器数量' }
                        ]
                    },
                task_pie_data: {
                    text: '各组件执行任务数比例',
                    data: [
                        { value: 35, name: 'ES已执行任务数量' },
                        { value: 23, name: 'Hadoop已执行任务数量' },
                        { value: 76, name: 'Kafka已执行任务数量' }
                    ]
                },
                pie_sample: {
                    tooltip: {
                        trigger: 'item',
                        textStyle: {
                            fontSize: 10
                        }
                    },
                  
                    series: [
                        {
                            name: '',
                            type: 'pie',
                            radius: ['40%', '70%'],
                            avoidLabelOverlap: false,
                            itemStyle: {
                                borderRadius: 10,
                                borderColor: '#fff',
                                borderWidth: 2
                            },
                            label: {
                                show: false,
                                position: 'center'
                            },
                            emphasis: {
                                label: {
                                    show: true,
                                    fontSize: '15',
                                    fontWeight: 'normal'
                                    
                                }
                            },
                            labelLine: {
                                show: true
                            },
                            data: []
                        }
                    ]
                },
                bar_sample: {
                    title: {
                        padding: [25, 20, 20, 20],
                        text: '',
                        left: 'left',
                        top: 'top',
                        textStyle: {
                            fontSize: 14
                        }
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: { // 坐标轴指示器，坐标轴触发有效
                            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                        }
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    yAxis: [
                        {
                            type: 'category',
                            axisTick: {
                                alignWithLabel: true,
                                length: 0
                
                            },
                            axisLine: {
                                show: false
                            }
          
                        }
        
                    ],
                    xAxis: [
                        {
                            show: false
                        }
                    ],
                    itemStyle: { borderRadius: 50 },
                    series: [
                        {
                            label: {
                                show: true,
                                position: 'inside'
                            },
                            name: '机器数量',
                            type: 'bar',
                            barWidth: '30%',
                            color: '#182132',
                            data: []
                        }
                    ]
                },
                rose_sample: {
                
                    tooltip: {
                        trigger: 'item',
                        textStyle: {
                            fontSize: 10
                        },
                        formatter: '{a} <br/>{b} : {c} ({d}%)'
                    },
                    legend: {
                        top: 'middle',
                        left: 0,
                        orient: 'vertical'
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            mark: { show: true },
                            dataView: { show: true, readOnly: true },
                            restore: { show: true },
                            saveAsImage: { show: true }
                        }
                    },
                    series: [
                        {
                            name: '机器数量',
                            type: 'pie',
                            radius: [60, 120],
                            center: ['50%', '50%'],
                            roseType: 'area',
                            itemStyle: {
                                borderRadius: 10
                            },
                            data: []
                        }
                    ]
                }
            }
        },
        mounted () {
            this.RoseChart(this.esTopChart, 'es_bar_top_5', this.es_data)
            this.RoseChart(this.hadoopTopChart, 'hadoop_bar_top_5', this.hadoop_data)
            this.RoseChart(this.kafkaTopChart, 'kafka_bar_top_5', this.kafka_data)
            this.PieChart(this.taskChart, 'tasknum', this.task_pie_data)
            this.PieChart(this.machineChart, 'machinenum', this.machine_pie_data)
            this.PieChart(this.clsuterChart, 'clusternum', this.cluster_pie_data)
        },
        methods: {
            clusterPieChart () {
                const clusterData = this.pie_sample
                clusterData.series[0].name = this.cluster_pie_data.text
                clusterData.series[0].data = this.cluster_pie_data.data
                
                const clsuterChart = echarts.init(document.getElementById('clusternum'))
                clsuterChart.setOption(clusterData)
            },
            machinePieChart () {
                const machineData = this.pie_sample
                machineData.series[0].name = this.machine_pie_data.text
                machineData.series[0].data = this.machine_pie_data.data

                const clsuterChart = echarts.init(document.getElementById('machinenum'))
                clsuterChart.setOption(machineData)
            },
            PieChart (chart, divId, xdata) {
                const Data = this.pie_sample
                Data.series[0].name = xdata.text
                Data.series[0].data = xdata.data
                const object = document.getElementById(divId)

                chart = echarts.init(object)
                chart.setOption(Data)
                const Resize = elementResize({
                    strategy: 'scroll', // <- 推荐监听滚动，提升性能
                    callOnAdd: true // 添加侦听器时是否应调用,默认true
                })
                Resize.listenTo(object, function (element) {
                    echarts.init(object).resize() // 当元素尺寸发生改变是会触发此事件，刷新图表
                })
            },
            RoseChart (topChart, divId, xdata) {
                const Data = this.rose_sample
                const object = document.getElementById(divId)

                Data.series[0].data = xdata
                topChart = echarts.init(object)
                topChart.setOption(Data)
                const Resize = elementResize({
                    strategy: 'scroll', // <- 推荐监听滚动，提升性能
                    callOnAdd: true // 添加侦听器时是否应调用,默认true
                })
                Resize.listenTo(object, function (element) {
                    echarts.init(object).resize() // 当元素尺寸发生改变是会触发此事件，刷新图表
                })
            }

        }
    }
</script>
<style lang="postcss">
    .home-card-layout {
        
        height: 100%;
        width: 100%;
        padding: 18px 20px;
        background: #fff;
        color: #63656e;
        -webkit-box-shadow: 0 1px 2px 0 rgb(0 0 0 / 10%);
        box-shadow: 0 1px 2px 0 rgb(0 0 0 / 10%);
        border-radius: 2px;
        
        .history-record-box {
            position: relative;
            width: 100%;
            height: 742px;

        }
        .card-title {
                  margin-bottom: 20px;
                  font-size: 14px;
                  font-weight: 700;
                  line-height: 1;
                  color: #313238;
                 
                  }
        .swiper-boby {
             font-size: 12px;
             margin-top: 50px;
             height: 180px;
             margin-right: auto;
             margin-left: auto;

             .swiper-content{
                white-space: pre-wrap;
                text-align: left;
                line-height: 30px;
             }
        }
        .bar-style {
            width: 100%;
            height: 250px;
            margin-right: auto;
            margin-left: auto;
           }
        .echart_style {
            width:100%;
            height:220px;
            margin-right: auto;
            margin-left: auto;
    }
      
    }

    .main-grid {
        .wrapper {
            overflow: hidden;
            /* border: 1px solid #ddd; */
            border-radius: 2px;
            padding: 20px 0;
        }
        .bk-grid-row {
        }

        .bk-grid-row + .bk-grid-row {
            margin-top: 30px;
        }

        .flex {
            .bk-grid-row + .bk-grid-row {
                margin-top: 20px;
            }
        }
        
    }
    .work-statistics-box {
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        padding-top: 18px;
        text-align: center;
        cursor: pointer;
        .work-flag {
            position: relative;
            width: 100px;
            height: 60px;
            margin-bottom: 15px;
            margin-left: auto;
            margin-right: auto;
        }
        .work-total {
            font-size: 24px;
            color: #313238;
            font-weight: 700;
        }
        .work-name {
            margin-top: 2px;
            color: #979ba5;
        }
    
    }

</style>
