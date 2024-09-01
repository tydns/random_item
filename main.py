# 初始化
FormworkCopy = 1
print("由 天源互联(bilibili)改进，随机物品生成逻辑由 明灯owo(bilibili)编写")
print("此项目在https://github/tianyuan/randomitem/ 上开源")
print("禁止二次收费")
print("具体请看当前目录下的README.txt")
print("README.md为项目简介")

# 生成 uuid
import uuid

uuidA = str(uuid.uuid4())
uuidB = str(uuid.uuid4())
uuidC = str(uuid.uuid4())
#print(uuidA, uuidB)

# 复制模板
import shutil
import os

# 源目录路径
src_dir = './Formwork'

# 目标目录路径
dst_dir = './Formwork-copy'

# 复制目录
try:
    shutil.copytree(src_dir, dst_dir)
    #print(f"目录已成功从 {src_dir} 复制到 {dst_dir}")
except FileExistsError:
    print(f"目标目录 {dst_dir} 已经存在")
    ModelCopy = 1
except Exception as e:
    print(f"复制目录时发生错误: {e}")

# 将复制的模板中的特定字符串替换为 uuid
file_path = os.path.join(dst_dir, 'manifest.json')  # 文件路径

# 读取文件内容
with open(file_path, 'r') as file:
    file_data = file.read()

# 替换字符串
file_data = file_data.replace('uuidA', uuidA)
file_data = file_data.replace('uuidB', uuidB)
file_data = file_data.replace('uuidC', uuidC)                                                                                          
# 写回文件
with open(file_path, 'w') as file:
    file.write(file_data)

# 生成函数包
fp = open(os.path.join(dst_dir, 'functions', 'random_item.mcfunction'), 'w')
print("gamerule commandblockoutput false\nscoreboard objectives add rc dummy\nscoreboard objectives add quantity dummy", file=fp, end="\n")
fp.close()

fp = open(os.path.join(dst_dir, 'functions', 'random_item.mcfunction'), 'a')
stackable_item = list(map(str, input("输入可堆叠物品：").split(",")))
non_stackable_item = list(map(str, input("输入单个物品：").split(",")))
rare_item = list(map(str, input("输入稀有物品：").split(",")))

for blank in range(27):
    print("tag @e remove rc\nscoreboard players random @e[name=rc] rc 1 4\ntag @e[name=rc,scores={rc=4}] add rc\nscoreboard players reset @e[name=rc,tag=!rc]\nscoreboard players random @e[tag=rc] rc 1", len(stackable_item) + len(non_stackable_item) + len(rare_item), "\nscoreboard players random @e[tag=rc,scores={rc=1..", len(stackable_item), "}] quantity 0 5", file=fp, end="\n")
    rc = 1
    for item in stackable_item:
        for quantity in range(5):
            print(f"execute @e[scores={{rc={rc},quantity={quantity}}}] ~~~ replaceitem block ~~-0.1~ slot.container {blank} {item} {2**(quantity+1)}", file=fp, end="\n")
        rc = rc + 1
    for item in non_stackable_item:
        print(f"execute @e[scores={{rc={rc}}}] ~~~ replaceitem block ~~~ slot.container {blank} {item}", file=fp, end="\n")
        rc = rc + 1
    for item in rare_item:
        print(f"execute @e[scores={{rc={rc}}}] ~~~ scoreboard players random @s rc -20 -1\nexecute @e[scores={{rc=-1}}] ~~~ replaceitem block ~~~ slot.container {blank} {item}", file=fp, end="\n")
        rc = rc + 1

print("kill @e[type=armor_stand,name=rc]", file=fp, end="")
fp.close()

# 压缩
import zipfile

# 源目录路径
dir_path = './Formwork-copy'

# 目标 ZIP 文件路径（包括 .zip 扩展名）
dst_zip = './out.zip'

# 将目录压缩为 ZIP 文件
with zipfile.ZipFile(dst_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), dir_path))

print(f"目录已成功压缩为 {dst_zip}")

# 删除目录
shutil.rmtree(dst_dir)
print(f"目录 {dst_dir} 已成功删除")

# 源文件路径
src_file = './out.zip'

# 目标文件路径
dst_file = './out.mcpack'

# 重命名文件
os.rename(src_file, dst_file)

print(f"文件已成功从 {src_file} 重命名为 {dst_file}")
print("已制作完成！")