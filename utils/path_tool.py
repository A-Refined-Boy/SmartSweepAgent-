"""
为整个工程提供统一的绝对路径
"""
import os

#获取当前文件所在的根目录
def get_project_root()->str:

    #获取当前文件的绝对路径
    current_file=os.path.abspath(__file__)
    #获取当前文件所在的文件夹的路径
    current_dir=os.path.dirname(current_file)
    #获取工程的根目录
    project_root=os.path.dirname(current_dir)

    #返回根目录
    return project_root


#通过当前文件的相对路径，获取其所在的绝对路径
def get_abs_path(relative_path:str) ->str:

    #获取当前文件所在的工程的根目录
    project_root=get_project_root()
    #通过根目录和相对路径计算绝对路径
    abs_path=os.path.join(project_root,relative_path)
    return abs_path



