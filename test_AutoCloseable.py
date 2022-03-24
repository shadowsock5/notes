#coding=utf-8

import os
import sys
import zipfile

import javalang
from javalang.parse import parse
from javalang.tree import *


'''
代码参考：
https://github.com/Lonely-night/fastjson_gadgets_scanner


evil_set条件：
1、未实现黑名单接口：DataSource, RowSet
2、未继承黑名单类：Classloader

details_set条件：
1、存在无参的构造函数；
2、field和method配套


思路：
evil_set = set()   # 设置为集合，为了去重


对某目录下的所有java文件：
    解析每个文件的类/接口:
        if 该类继承/实现某敏感类/接口(evil_set):
            
            该类的方法名列表;
            该类的field名;

            if field名首字母非大写:（首字母大写应该是静态常量）
                if "get" + field名 in 该类的方法名列表:
                    将该类加入到evil_set中
'''

DECOMPILER_PATH = "D:\\repos\\fernflower\\build\\libs\\fernflower.jar"

SOURCE_DIR = "C:\\Users\\Administrator\\Downloads\\src"

OUT_RESULT_DETAILS = "./{0}.result_details.txt".format(SOURCE_DIR[-3:])

EVIL_SET_FILE = "./evil_set.txt"

time_tmp = 0


evil_set = set()    # 集合类型，为了去重
details_set = set()

evil_list = [line.rstrip('\n') for line in open(EVIL_SET_FILE)]
for i in evil_list:
    evil_set.add(i)


def scanner(filename):
    # 打开某个.java源文件
    file_stream = open(filename, 'r')
    _contents = file_stream.read()
    file_stream.close()


    try:
        root_tree = parse(_contents)

        # 先拿到继承/实现敏感类/接口的类
        class_declaration_list = get_class_declaration_in_condition(root_tree)
        
        # 查找有没有满足某些命名规则的方法

        for class_declaration in class_declaration_list:
            # evil_set因为是用于反复查找，所以条件松一些
            evil_set.add(class_declaration.name)    # 将得到的接口/类加入下一次待检查的集合中(不同于列表，用于去重)


            # details_set因为是想找最终可用的gadget，所以要满足多一些条件
            for method in class_declaration.methods:
                #print(method.name)        # 查看其方法名
                #if is_method_starts_with_get_or_set(method.name):
                    #print(method.name)
                    
                for field in class_declaration.fields:
                    for declarator in field.declarators:
                        if declarator.name[0].islower():
                            if is_method_field_match(declarator.name, method.name):
                                details = class_declaration.name + ":" + declarator.name + ":" + method.name
                                details_set.add(details)
                                #write_file(OUT_RESULT_DETAILS, details)
          

    except KeyboardInterrupt:
        # 碰到键盘中断，则将evil_set中的类写入到文件中
        dump_evil_set(evil_set)
        dump_details_set(details_set)

        sys.exit(1)

    except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError) as e:
        #dump_evil_set(evil_set)
        print(e)


# 碰到异常时，将evil_set中的类写入到文件中
def dump_evil_set(p_evil_set):
    for item in p_evil_set:
        EVIL_SET_FILE_TMP = "./evil_set_{0}.txt".format(time_tmp)
        write_file(EVIL_SET_FILE_TMP, item)



# 碰到异常时，将details_set中的详情写入到文件中
def dump_details_set(p_details_set):
    for item in p_details_set:
        OUT_RESULT_DETAILS_TMP = "./result_details_set{0}.txt".format(time_tmp)
        write_file(OUT_RESULT_DETAILS, item)



# 判断field和method是否配套
def is_method_field_match(p_field, p_method):
    field_to_match = "get{0}".format(p_field).upper()
    if field_to_match == p_method.upper():
        return True
    else:
        return False


def is_method_starts_with_get_or_set(p_method):
    if p_method.startswith("get") or p_method.startswith("set"):
        return True
    return False


# 筛选出符合条件的类
def get_class_declaration_in_condition(root):
    '''
    node.implements: 这个类实现的类
    node.extends： 这个类继承的类
    '''

    class_list = []
    
    for node in root.types:
        # 非类声明/接口声明都不分析
        isClassDeclaration = False

        if not isinstance(node, ClassDeclaration) and not isinstance(node, InterfaceDeclaration):
            continue
        elif isinstance(node, ClassDeclaration):
            isClassDeclaration = True

        # 实现了黑名单中的类、 继承黑名单中的接口是一定不能要的
        if isClassDeclaration:
            if is_subclass_of_blacklist(node):
                continue
        

        # 判断是否extends或者implements了`java.lang.AutoCloseable`

        if node.extends is not None:
            for extend in node.extends:
                #print(extend)
                for i in extend:
                    if get_attr_name(i):
                        class_list.append(node)


        # class才能实现接口
        if isClassDeclaration:
            if node.implements is not None:
                # 在其所有实现的接口中，如果有实现了AutoCloseable这个接口的
                for implement in node.implements:
                    if is_subclass_of_evil_set(implement.name, evil_set)
                        class_list.append(node)

    return class_list



# 筛选出符合条件的接口
def get_interface_declaration_in_condition(root):
    '''
    node.extends： 这个接口继承的类
    '''
    interface_list = []

    for node in root.types:
        isInterfaceDeclaration = False

        if isinstance(node, InterfaceDeclaration):
            isInterfaceDeclaration = True

        # 判断是否extends了`java.lang.AutoCloseable`

        if node.extends is not None:
            for extend in node.extends:
                #print(extend)
                for i in extend:
                    if get_attr_name(i, is_test_evil_set=True):
                        class_list.append(node)


# 判断是否实现了blacklist中的接口、blacklist中的类
def is_subclass_of_blacklist(p_node):

    black_interface = {"DataSource", "RowSet"}
    
    black_class = {"ClassLoader"}
    
    if p_node.implements is None:
        p_node.implements = []
    if p_node.extends is None:
        p_node.extends = []  

    for implement in p_node.implements:
        if implement.name in black_interface:    # 有一个实现了黑名单中的接口就break，不用继续找了
            return True
            

    for extend in p_node.extends:
        for i in extend:
            if get_attr_name(i, is_test_blacklist=True):
                return True

    return False


# 判断是否存在无参的构造函数
def is_exists_none_param_constructor(p_node):
    for constructor_declaration in p_node.constructors:
        if len(constructor_declaration.parameters) == 0:
            return True
    
    return False



def get_attr_name(p_node, is_test_evil_set=False, is_test_blacklist=False):
    # 非空tuple, 则遍历其元素，看是否有ReferenceType类型的元素。
    if p_node and isinstance(p_node, tuple):
        for n in p_node:

            if not isinstance(n, tuple) and not is_TypeArgument(n):
                if isinstance(n, list):
                    for i in n:
                        if not is_TypeArgument(i):
                            if i.name:
                                if is_test_evil_set:
                                    return is_subclass_of_evil_set(i.name, evil_set)
                                elif is_test_blacklist:
                                    return is_subclass_of_blacklist(i.name)

                elif isinstance(n.name, str):
                    if is_test_evil_set:
                        return is_subclass_of_evil_set(n.name, evil_set)


def is_subclass_of_evil_set(p_node_name, p_evil_set):
    for evil in p_evil_set:
        if p_node_name == evil:
            return True

            
def has_sub_type(p_node):
    if isinstance(p_node, ReferenceType):
        if p_node.sub_type:
            return True
    return False


def is_TypeArgument(p_node):
    if isinstance(p_node, TypeArgument):
        return True
    return False


def is_ReferenceType(p_node):
    if isinstance(p_node, ReferenceType):
        return True
    return False


# 拿到某目录下所有.java文件
def get_allfiles_fullpath(p_root_dir): 
    list_dirs = os.walk(p_root_dir)
    list_files = [] 
    
    for root, dirs, files in list_dirs:      
        for f in files:
            
            if f.endswith(".java"):   # 只要.java结尾的文件
                full_path_java_f = os.path.join(root, f)
                list_files.append(full_path_java_f) 
            
            elif f.endswith(".jar") and "javadoc" not in f:    # 若以.jar结尾(排除javadoc的jar包)，则进行反编译
                f_dir_name = f[0:-4] + "_jar"
                full_path_source_jar_f = os.path.join(root, f_dir_name)
                if not os.path.isdir(f_dir_name):    # 若不存在该目录则创建
                    # 传入反编译器的路径，jar文件的完整路径
                    
                    full_path_dest_dir = os.path.join(root, f)
                    decompile(DECOMPILER_PATH, full_path_source_jar_f, )
                    os.mkdir(os.path.join(root, f_dir_name))

    return list_files


# java -jar <fernflower_full_path.jar> <source.jar> <dest>
def decompile(p_compiler_path, p_jar_file, p_dest_dir):
    cmd = "java -jar {0} {1} {2}".format(p_compiler_path, p_jar_file, p_dest_dir)
    os.system(cmd)

    # 解压之后得到的是包含.java源文件的压缩包，需要进行解压
    #TODO


def write_file(filename, string):
    file_stream = open(filename, "a")
    file_stream.write(string + '\n')
    file_stream.close()



if __name__ == '__main__':
    
    # 拿到目标目录下的 .java文件列表
    file_list = get_allfiles_fullpath(SOURCE_DIR)

    # 通过键盘中断来结束
    while True:
        try:

            print("【*】 第{0}波".format(time_tmp))
            print("【*】 当前个数： {0}".format(len(evil_set)))
            print("【*】 当前evil_set: ", evil_set)
            

            for _file in file_list:
                scanner(_file)
            time_tmp = time_tmp + 1
            
            
        except KeyboardInterrupt:
            break
