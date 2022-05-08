import json


def remove_dot(*args):
    big_list =[]
    for item in args:
        item = "".join(item.split(","))
        big_list.append(item)
    return big_list


a=["3,43","333"]
b=("3,43","333")


d= [{"a":1,"vlanid":100},{"a":1,"vlanid":101},{"a":1,"vlanid":102},{"a":1,"vlanid":103},{"a":1,"vlanid":104}]

print([x for x in d if x["vlanid"]!=100])
j = json.dumps(d)


jj = [json.dumps({"a":1,"vlanid":100}),json.dumps({"a":1,"vlanid":101}),json.dumps({"a":1,"vlanid":102}),json.dumps({"a":1,"vlanid":103}),json.dumps({"a":1,"vlanid":104})]
print(jj)
#


# 在json模块有2个方法，
#
# loads()：将json数据转化成dict数据
# dumps()：将dict数据转化成json数据
# load()：读取json文件数据，转成dict数据
# dump()：将dict数据转化成json数据后写入json文件
# 下面是具体的示例：
# print(type(d))
# print(type(j))
print(len([x for x in jj if json.loads(x)["vlanid"]!=100]))