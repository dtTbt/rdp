# MySQL 和 RDP 安装和配置指南

本指南介绍如何安装配置 MySQL 与配置开机启动服务。这个过程包括下载和安装 MySQL，创建开机启动服务，以及更改 MySQL 密码并创建数据库表。

## 一、安装 MySQL

1. 确保 MySQL 和 RDP 都应在用户文件夹下。

2. 下载 MySQL：

   ```shell
   wget https://downloads.mysql.com/archives/get/p/23/file/mysql-8.0.33-linux-glibc2.28-aarch64.tar.gz
   ```

3. 解压 MySQL：

   ```shell
   tar xzf mysql-8.0.33-linux-glibc2.28-aarch64.tar.gz
   ```

4. 将解压后的文件夹重命名为 `mysql`：

   ```shell
   mv mysql-8.0.33-linux-glibc2.28-aarch64 mysql
   ```

5. 编辑 `.bashrc` 文件：

   ```shell
   vim ~/.bashrc
   ```

   在文件末尾添加以下内容：

   ```shell
   export PATH=$PATH:~/mysql/bin
   ```

   然后更新 `.bashrc`：

   ```shell
   source ~/.bashrc
   ```

6. 初始化 MySQL：

   ```shell
   mysqld --initialize --user=$USER
   ```

## 二、设置开机启动

### 创建 rdp 开机启动服务

1. 创建一个脚本文件:
   ```shell
   sudo vim /home/forlinx/rdp/rdp.sh
   ```
2. 在文件中添加以下内容:

   ```shell
   #!/bin/bash
   
   cd /home/forlinx/rdp
   
   PYTHON="/home/forlinx/miniconda3/bin/python"
   
   start_services() {
       echo "Starting main.py..."
       $PYTHON /home/forlinx/rdp/main.py &
       echo "main.py started."
   
       echo "Starting api.py..."
       $PYTHON /home/forlinx/rdp/api.py &
       echo "api.py started."
   
       wait
   }
   
   stop_services() {
       echo "Stopping main.py..."
       pkill -f "$PYTHON /home/forlinx/rdp/main.py"
       echo "main.py stopped."
   
       echo "Stopping api.py..."
       pkill -f "$PYTHON /home/forlinx/rdp/api.py"
       echo "api.py stopped."
   }
   
   if [ "$1" == "start" ]; then
       start_services
   elif [ "$1" == "stop" ]; then
       stop_services
   else
       echo "Usage: $0 {start|stop}"
       exit 1
   fi

   ```
   
   注意将`PYTHON`路径替换为安装了依赖包的环境对应的Python解释器路径。

3. 赋予`rdp.sh`脚本执行权限:

   ```shell
   sudo chmod +x /home/forlinx/rdp/rdp.sh
   ```

4. 创建一个 systemd 服务配置文件：

   ```shell
   sudo vim /etc/systemd/system/rdp.service
   ```

5. 在文件中添加以下内容：

   ```shell
   [Unit]
   
   [Service]
   ExecStartPre=/bin/sleep 3
   ExecStart=/home/forlinx/rdp/rdp.sh start
   ExecStop=/home/forlinx/rdp/rdp.sh stop
   User=forlinx
   Group=forlinx
   
   [Install]
   WantedBy=default.target
   ```
   
   `forlinx`为示例用户名，注意将`forlinx`替换为您的用户名。

6. 重新加载 systemd 配置：

   ```shell
   sudo systemctl daemon-reload
   ```

7. 启用 RDP 服务，使其开机自动启动：

   ```shell
   sudo systemctl enable rdp.service
   ```

8. 立即启动此服务：

   ```shell
   sudo systemctl start rdp.service
   ```

9. 停止此服务：

   ```shell
   sudo systemctl stop rdp.service
   ```

### 创建 MySQL 开机启动服务

1. 创建一个 systemd 服务配置文件：

   ```shell
   sudo vim /etc/systemd/system/mysql_st.service
   ```

2. 在文件中添加以下内容：

   ```shell
   [Unit]

   [Service]
   ExecStartPre=/bin/sleep 10
   ExecStart=/home/forlinx/mysql/bin/mysqld
   ExecStop=/home/forlinx/mysql/bin/mysqladmin shutdown
   User=forlinx
   Group=forlinx

   [Install]
   WantedBy=default.target
   ```
   
   `forlinx`为示例用户名，注意将`forlinx`替换为您的用户名。

3. 重新加载 systemd 配置：

   ```shell
   sudo systemctl daemon-reload
   ```

4. 启用此服务，使其开机自动启动：

   ```shell
   sudo systemctl enable mysql_st.service
   ```

5. 立即启动此服务：

   ```shell
   sudo systemctl start mysql_st.service
   ```

6. 停止此服务：

   ```shell
   sudo systemctl stop mysql_st.service
   ```

### 检查MySQL服务是否启动

1. 使用以下命令检查 MySQL 服务是否启动：

   ```shell
   ps aux | grep mysqld
   ```

2. 如果启动失败（可能由于端口占用），可以使用以下命令找到并终止占用端口的进程（这里假设占用端口为 3307）：

   ```shell
   lsof -i:3307
   kill -9 [进程号]
   ```

## 三、更改 MySQL 密码和创建数据库表

1. 登录到 MySQL：

   ```shell
   mysql -u root -p
   ```

2. 更改 MySQL root 用户密码：

   ```shell
   alter user 'root'@'localhost' identified by '123456';
   FLUSH PRIVILEGES;
   ```

3. 创建一个名为 `test_rdp` 的数据库并切换到它：

   ```shell
   CREATE DATABASE test_rdp;
   USE test_rdp;
   ```

4. 创建名为 `rdp_result` 的数据库表：

   ```shell
   CREATE TABLE rdp_result (
       id INT AUTO_INCREMENT PRIMARY KEY,
       camera INT,
       type VARCHAR(255),
       date_time TIMESTAMP(3),
       image_data LONGBLOB
   );
   ```
   
5. 禁用 `test_rdp` 数据库记录binlog：

   打开一个新的终端窗口。打开MySQL服务器的配置文件 `my.cnf`。该文件通常位于`/etc/mysql/my.cnf`。

   ```shell
   sudo vim /etc/mysql/my.cnf
   ```
   
    在文件中添加以下内容：

   ```shell
   [mysqld]
   binlog-ignore-db=test_rdp
   ```
   
   保存并退出，然后重启MySQL服务。

6. （可选）查询当前有多少条数据：

   ```shell
   USE test_rdp;
   SELECT COUNT(*) FROM rdp_result;
   ```

7. （可选）如果需要，您可以使用以下命令删除数据库表中的所有内容：

   ```shell
   TRUNCATE TABLE rdp_result;
   ```