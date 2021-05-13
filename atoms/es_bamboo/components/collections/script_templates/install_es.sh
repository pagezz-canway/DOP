#!/bin/bash


anynowtime="date +'%Y-%m-%d %H:%M:%S'"
NOW="echo [\`$anynowtime\`][PID:$$]"

##### 可在脚本开始运行时调用，打印当时的时间戳及PID。
function job_start
{
    echo "`eval $NOW` job_start"
}

##### 可在脚本执行成功的逻辑分支处调用，打印当时的时间戳及PID。
function job_success
{
    MSG="$*"
    echo "`eval $NOW` job_success:[$MSG]"
    exit 0
}

##### 可在脚本执行失败的逻辑分支处调用，打印当时的时间戳及PID。
function job_fail
{
    MSG="$*"
    echo "`eval $NOW` job_fail:[$MSG]"
    exit 1
}

job_start


## 初始化
ESENV="/data/esenv"
##  暂时不考虑多个路径的情况
#ESDATA="/data/esdata"
ESLOG="/data/eslog"
user=elastic

adduser $user

echo -e "elastic soft memlock unlimited\nelastic hard memlock unlimited" >> /etc/security/limits.conf
echo -e "vm.max_map_count=262144\nvm.swappiness=1" >> /etc/sysctl.conf ;sysctl -p

path=`cat /etc/mtab |grep /data |grep -v overlay |awk '{print $2}'`
if [[ "x$path" == "x/data" ||  "x$path" == "x" ]];then
    mkdir -p /data/esdata && chown -R elastic:elastic /data/esdata
    ESDATA="/data/esdata"
else
    for i in $path;do
        mkdir $i/esdata  && chown -R elastic:elastic $i/esdata
        datapath=$i/esdata,$datapath
    done
    ESDATA=`echo $datapath|sed 's/,$//'`
fi

[[ ! -e "$ESENV" ]] && mkdir -p $ESENV  && chown  -R $user:$user $ESENV
[[ ! -e "$ESLOG" ]] && mkdir -p $ESLOG  && chown -R $user:$user $ESLOG

cat << 'EOF' > /data/esenv/esprofile
export JAVA_HOME=/data/esenv/java
export JRE=$JAVA_HOME/jre
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
export CLASSPATH=".:$JAVA_HOME/lib:$JRE/lib:$CLASSPATH"
export ES_HOME=/data/esenv/es
export ES_CONF_DIR=$ES_HOME/config
export PATH=$PATH:$ES_HOME/bin
export PATH=$PATH:$ES_HOME/sbin
export PATH=$PATH:${JAVA_HOME}/bin:${ES_HOME}/bin:${ES_HOME}/sbin
EOF

echo "export ESDATA=$ESDATA" >> /data/esenv/esprofile

chown elastic  /data/esenv/esprofile

sed -i '/esprofile/d' /etc/profile
echo "source /data/esenv/esprofile" >>/etc/profile
env

clustername=$1
masterip=$2
role=$3
port=$4
version=$5

user="elastic"

nodeip=`ip a|grep eth1|grep inet |awk '{print $2}'| awk -F'/' '{print $1}'`
source /etc/profile
env
esconfig="/data/esenv/es/config/elasticsearch.yml.template"
#kibanaconfig="/data/esenv/kibana/config/kibana.yml"
#strongerconfig="/data/esenv/stronger/status_config.xml"
jvmconfig="/data/esenv/es/config/jvm.options.template"
nodename="dn-$nodeip"

if [[ "x$role" = "xmaster" ]];then
    master="true"
    data="false"
    nodename="master-$nodeip"
    tag="node.attr.tag: master"
elif [[ "x$role" = "xdata" ]]; then
    master="false"
    data="true"
    nodename="dn-$nodeip"
    tag="node.attr.tag: hot"
elif [[ "x$role" = "xcold" ]]; then
    master="false"
    data="true"
    nodename="cold-$nodeip"
    tag="node.attr.tag: cold"
elif [[ "x$role" = "xall" ]]; then
    master="true"
    data="true"
elif [[ "x$role" = "xclient" ]]; then
    master="false"
    data="false"
    nodename="client-$nodeip"
    tag="node.attr.tag: client"
fi

echo "cluster name is: $clustername"
echo "master  ip is:    $masterip"
echo "node  ip is:     $nodeip"
echo "nodename is:     $nodename"
echo "port is: $port"
echo "version: $version"

oldnodename=$nodename
oldport=$port
masternodename=`echo $masterip | sed  's/,/&master-/g;s/^/master-&/'`

mv /data/*.tar.gz /data/esenv
cd /data/esenv
# shellcheck disable=SC2015
tar zxf elasticsearch-"$version".tar.gz && ln -s elasticsearch-"$version" es  || job_fail "tar elasticsearch-$version.tar.gz failed"


if [[ $version == "5.4.0" ]];then
    tar zxf TencentKona-8.tar.gz && ln -s TencentKona-8 java || job_fail "tar java failed"
    if [ -L "/usr/bin/java" ];then
        rm -f /usr/bin/java
    fi
    ln -sf  /data/esenv/java/bin/java /usr/bin/java || job_fail "创建java软链接失败"
else
    tar zxf TencentKona-11.tar.gz && ln -s TencentKona-11 java || job_fail "tar java failed"
    if [ -L "/usr/bin/java" ];then
        rm -f /usr/bin/java
    fi
    ln -sf  /data/esenv/java/bin/java /usr/bin/java || job_fail "创建java软链接失败"
fi

# 获取系统内存，单位KB 65465872
#
sysmem=`cat /proc/meminfo |grep MemTotal|awk '{print $2}'`

if [ "$sysmem" -ge 64088224 ];then
    jvm="26g"
else
    jvm=`echo "$sysmem*.5/1024/1024"|bc`
    jvm="${jvm}g"
fi



echo "JVM setting to $jvm ..."
sed -i -e "s/__HEAPSIZE__/$jvm/g" $jvmconfig

if [[ $? -ne 0 ]];then
    echo "Config  jvm.options failed"
    exit $?
else
    echo "Config jvm.options success."
fi

cp $jvmconfig /data/esenv/es/config/jvm.options


echo "Now changing the $esconfig  ... "

sed -i  -e "/cluster.name/s/__CLUSTERNAME__/$clustername/"  -e \
    "/path.data/s#__ESDATA__#$ESDATA#" -e \
    "/node.name/s/__NODENAME__/$nodename/"  -e \
    "/discovery.zen.ping.unicast.hosts/s/__MASTERLIST__/$masterip/" -e \
    "/discovery.seed_hosts/s/__MASTERLIST__/$masterip/" -e \
    "/cluster.initial_master_nodes/s/__MASTERLIST__/$masternodename/" -e \
    "/node.master/s/true/$master/" -e \
    "/node.data/s/true/$data/" -e \
    "s/__HTTPPORT__/$port/" -e \
    "/node.master/a\\$tag" -e  \
    "s/__IP__/$nodeip/"  $esconfig

if [[ $? -ne 0 ]];then
    echo "Config  elasticsearch.yml failed"
    exit $?
else
    echo "Config elasticsearch.yml success."
fi

cp $esconfig /data/esenv/es/config/elasticsearch.yml

echo "Change grant for /data/esenv ..."
chown -R elastic:elastic /data/esenv


## supervisor
f1=supervisor.tar.gz
f2=pypy-5.9.0.tar.gz
d=$(date +%Y%m%d%H%M%S)

cd /data/esenv
if [ -e "supervisor" ];then
    mv supervisor supervisor."$d"
fi
tar zxf  $f1 && echo "解压$f1完成" || echo "解压$f1失败"
tar zxf $f2 && echo "解压$f2完成" || echo "解压$f2失败"

echo "建立软链接"

ln -s pypy-5.9.0 python
ln -s /data/esenv/supervisor/conf/supervisord.conf /etc/supervisord.conf
ln -s /data/esenv/supervisor/bin/supervisorctl /usr/local/bin/supervisorctl
ln -s /data/esenv/python/bin/supervisord  /usr/local/bin/supervisord


echo "更改权限"
chown -R $user:$user /data/esenv/pypy-5.9.0
chown -R $user:$user /data/esenv/supervisor

echo "安装crontab"
crontab  -l -u  $user >crontab.$user.bak
cp crontab.$user.bak crontab."$d"
sed -i '/check_supervisord.sh/d' crontab.$user.bak
echo '*/1 * * * *  /data/esenv/supervisor/check_supervisord.sh >> /data/esenv/supervisor/check_supervisord.err 2>&1' >>crontab.$user.bak
crontab -u $user crontab.$user.bak

echo "生成es supervisor.ini"
cat <<'EOF' > /data/esenv/supervisor/conf/elasticsearch.ini
[program:elasticsearch]
command=/data/esenv/es/bin/elasticsearch ; the program (relative uses PATH, can take args)
numprocs=1 ; number of processes copies to start (def 1)
autostart=true ; start at supervisord start (default: true)
startsecs=3 ; # of secs prog must stay up to be running (def. 1)
startretries=99 ; max # of serial start failures when starting (default 3)
autorestart=true ; when to restart if exited after running (def: unexpected)
exitcodes=0 ; 'expected' exit codes used with autorestart (default 0,2)
user=elastic ;
redirect_stderr=true ; redirect proc stderr to stdout (default false)
stdout_logfile=/data/eslog/es_startup.log ; stdout log path, NONE for none; default AUTO
stdout_logfile_maxbytes=50MB ; max # logfile bytes b4 rotation (default 50MB)
stdout_logfile_backups=10 ; # of stdout logfile backups (default 10)
EOF

su - elastic -c  "/usr/local/bin/supervisord -c /data/esenv/supervisor/conf/supervisord.conf" && job_success "部署supervisor成功" || job_fail "部署supervisor失败"


