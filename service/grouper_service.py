import os
import sys
import flask, json

# 添加环境变量
current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

from util.common_util import check_and_transform_field, check_excluded, get_exception_type
from util.config_util import  get_grouper_host, get_grouper_port
from grouper.grouper import drg_grouper
from grouper.model import Case

server = flask.Flask(__name__)  # __name__代表当前的python文件。把当前的python文件当做一个服务启动


@server.route('/test', methods=['post'])
# 第一个参数就是路径,第二个参数支持的请求方式，不写的话默认是get，
# 加了@server.route才是一个接口，不然就是一个普通函数
def test():
    res = {"msg": "连接成功"}
    print(res)
    # json.dumps 序列化时对中文默认使用的ascii编码，输出中文需要设置ensure_ascii=False
    return json.dumps(res, ensure_ascii=False)


@server.route('/grouper', methods=['post'])
# 第一个参数就是路径,第二个参数支持的请求方式，不写的话默认是get，
# 加了@server.route才是一个接口，不然就是一个普通函数
def grouper():
    input_dict = json.loads(flask.request.data)
    case = Case()
    case = check_and_transform_field(case, input_dict)
    case = check_excluded(case)
    case = drg_grouper(case)
    if 'error' in case.drg_code:
        case.drg_code = '0000'
    if case.drg_code == '0000':
        case = get_exception_type(case)
        case.mdc_code = '0000'
        case.adrg_code = '0000'
    return_field_list = ["unique_id", "excluded_flag", "excluded_reason", "mdc_code", "adrg_code", "drg_code", 'drg_name', 'exception_type', 'has_mcc', 'has_cc', 'grouper_version']
    result_dict = dict([])
    for return_field in return_field_list:
        result_dict[return_field] = getattr(case, return_field)
    # json.dumps 序列化时对中文默认使用的ascii编码，输出中文需要设置ensure_ascii=False
    return json.dumps(result_dict, ensure_ascii=False)


if __name__ == '__main__':
    # port可以指定端口，默认端口是5000
    # host默认是服务器，默认是127.0.0.1
    # debug=True 修改时不关闭服务
    server.run(host=get_grouper_host(), port=get_grouper_port())
