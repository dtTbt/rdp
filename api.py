from flask import Flask, jsonify, request
import pymysql
from main import get_mysql_config, read_config_file
import base64
import datetime
from json import JSONEncoder
import logging
import copy
import os
from file_operations import clear_large_file


# 自定义JSONEncoder，用于处理datetime类型的数据，保留毫秒
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return super().default(obj)  # 使用父类的默认处理方式

mysql_ip, mysql_username, mysql_password, mysql_database, mysql_table = get_mysql_config("config.yaml")
config = read_config_file("config.yaml")
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
mysql_config = {
    'host': mysql_ip,
    'user': mysql_username,
    'password': mysql_password,
    'db': mysql_database,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


# 配置日志记录器
logging.basicConfig(filename=config['log_path'], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/query/recent-messages', methods=['POST'])
def query_recent_messages():
    try:
        # 在每个路由函数开始时记录信息
        logging.info('Received POST request to /query/recent-messages')

        connection = pymysql.connect(**mysql_config)
        cursor = connection.cursor()

        request_data = request.get_json()
        N = int(request_data.get('limit', 5))
        sql = f"SELECT id, camera, type, date_time, image_data FROM {mysql_table} ORDER BY date_time DESC LIMIT {N}"

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        for row in result:
            row['image_data'] = base64.b64encode(row['image_data']).decode('utf-8')

        # 复制result并删除image_data
        result_copy = copy.deepcopy(result)
        for row in result_copy:
            del row['image_data']

        # 记录返回结果
        logging.info(f'Response sent: {result_copy}')

        return jsonify({'data': result}), 200
    except Exception as e:
        # 记录错误信息
        logging.error(f'Error: {str(e)}')
        return jsonify({'api_error': str(e)}), 500


@app.route('/query/by-datetime', methods=['POST'])
def query_by_datetime():
    try:
        # 在每个路由函数开始时记录信息
        logging.info('Received POST request to /query/by-datetime')

        connection = pymysql.connect(**mysql_config)
        cursor = connection.cursor()

        request_data = request.get_json()
        start_datetime_str = request_data.get('start_datetime')
        start_datetime = datetime.datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
        sql = f"SELECT id, camera, type, date_time, image_data FROM {mysql_table} WHERE date_time >= '{start_datetime}' ORDER BY date_time DESC"

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        for row in result:
            row['image_data'] = base64.b64encode(row['image_data']).decode('utf-8')

        # 复制result并删除image_data
        result_copy = copy.deepcopy(result)
        for row in result_copy:
            del row['image_data']

        # 记录返回结果
        logging.info(f'Response sent: {result_copy}')

        return jsonify({'data': result}), 200
    except Exception as e:
        # 记录错误信息
        logging.error(f'Error: {str(e)}')
        return jsonify({'api_error': str(e)}), 500


@app.route('/delete/by-datetime', methods=['POST'])
def delete_by_datetime():
    try:
        # 在每个路由函数开始时记录信息
        logging.info('Received POST request to /delete/by-datetime')

        connection = pymysql.connect(**mysql_config)
        cursor = connection.cursor()

        request_data = request.get_json()
        start_datetime_str = request_data.get('start_datetime')
        start_datetime = datetime.datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
        sql = f"DELETE FROM {mysql_table} WHERE date_time < '{start_datetime}'"

        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()

        # 记录成功消息
        logging.info('Records deleted successfully')

        return jsonify({'message': 'Records deleted successfully'}), 200
    except Exception as e:
        # 记录错误信息
        logging.error(f'Error: {str(e)}')
        return jsonify({'api_error': str(e)}), 500


@app.route('/delete/all', methods=['POST'])
def delete_all_records():
    try:
        # 在每个路由函数开始时记录信息
        logging.info('Received POST request to /delete/all')

        connection = pymysql.connect(**mysql_config)
        cursor = connection.cursor()

        sql = f"TRUNCATE TABLE {mysql_table}"

        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()

        # 记录成功消息
        logging.info('All records deleted successfully')

        return jsonify({'message': 'All records deleted successfully'}), 200
    except Exception as e:
        # 记录错误信息
        logging.error(f'Error: {str(e)}')
        return jsonify({'api_error': str(e)}), 500


if __name__ == '__main__':
    clear_large_file(config['log_path'], config['log_threshold'])
    logging.info("================== new start ==================")
    api_ip, api_port = config['api_ip'], config['api_port']
    if config['mode'] == 'debug':
        app.run(host=api_ip, port=api_port, debug=False)
    else:
        from gunicorn.app.base import BaseApplication
        class GunicornApp(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        gunicorn_options = {
            'bind': f'{api_ip}:{api_port}',
            'workers': 4  # 适当调整 worker 数量
        }
        GunicornApp(app, gunicorn_options).run()
