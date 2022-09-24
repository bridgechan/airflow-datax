# airflow-datax
此项目由airflow和datax组件构成。Airflow是一个由社区创建的平台，用于以编程方式创作、安排和监控工作流程，而datax是一个开源的数据离线同步工具。项目中通过airflow调度平台，通过开发DAGS作业，定期的调度执行一个个datax任务，将数据从数据源离线同步至目标端。airflow通过SSHOperator执行远端datax容器里面的shell任务。具体脚本请参考相关目录。

一、Dockerfile构建datax镜像  
准备工作：  
1、需要从开源社区下载datax的安装包，下载地址：https://github.com/alibaba/DataX  
2、定制datax，包含增加和替换插件的jdbc的驱动包，加入编译插件（例如elasticsearchwriter）等  
3、生成安装包datax.tar.gz  
实施过程:  
1、在当前目录build_datax编辑Dockerfile文件  
2、编译生成本地的datax镜像（这个命令必须在Dockerfile文件所在的目录下运行）  
docker build -t="dc/datax" .  
3、查看本地的镜像是否成功生成  
docker images  

二、部署开源的调度组件airflow2.x  
1、查看官网，选择docker安装部署：  
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html  
2、下载docker-compose.yaml，根据自己需要，作相应修改，增加datax服务  
3、启动容器：  
docker-compose up -d  
4、查看容器是否正常启动  
docker-compose ps  
5、启动容器然后验证  
docker exec -it datax python /datax/bin/datax.py /datax/job/test.json  
