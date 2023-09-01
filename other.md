# MySQL 和 RDP 安装和配置指南

本指南介绍如何安装配置 MySQL 与配置开机启动服务。这个过程包括下载和安装 MySQL，创建开机启动服务，以及更改 MySQL 密码并创建数据库表。

## 安装 MySQL

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

## 创建开机启动服务

1. 创建一个 systemd 服务配置文件：

   ```shell
   sudo vim /etc/systemd/system/rdp.service
   ```

2. 在文件中添加以下内容：

   ```shell
   [Unit]

   [Service]
   ExecStartPre=/bin/sleep 10
   ExecStart=/home/[user_name]/mysql/bin/mysqld
   ExecStart=/usr/bin/python3 /home/[user_name]/rdp/main.py
   ExecStart=/usr/bin/python3 /home/[user_name]/rdp/api.py
   User=[user_name]
   Group=[user_name]

   [Install]
   WantedBy=default.target
   ```

3. 重新加载 systemd 配置：

   ```shell
   sudo systemctl daemon-reload
   ```

4. 启用 RDP 服务，使其开机自动启动：

   ```shell
   sudo systemctl enable rdp.service
   ```

5. 立即启动此服务：

   ```shell
   sudo systemctl start rdp.service
   ```

## 检查服务是否启动

1. 使用以下命令检查 MySQL 服务是否启动：

   ```shell
   ps aux | grep mysqld
   ```

2. 如果启动失败（可能由于端口占用），可以使用以下命令找到并终止占用端口的进程（这里假设占用端口为 3307）：

   ```shell
   lsof -i:3307
   kill -9 [进程号]
   ```

## 更改 MySQL 密码和创建数据库表

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

5. （可选）如果需要，您可以使用以下命令删除数据库表中的所有内容，但保留表格结构：

   ```shell
   DELETE FROM rdp_result;
   ```