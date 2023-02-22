from bs4 import BeautifulSoup
import re
# {label|[AND|OR][.!text|.!html|([^%$])attr][^%$]}[=???][:]
# 情况:
# div:
#     class^=ab:
#         sp^=dd
#     AND.!class%=cc
# 同级match 视为或者匹配
# match ???

# 存储list下级匹配到的内容
# list ???:

# 将list转换成json
# json ??? use ???:

# 返回内容停止下面的操作
# ret ???
# json中用到的field,定义在json中field名字是什么,取得内容是哪些,返回给field的必须是ret返回
# field ???:

# json下的一级必须是json对应的field
# 情况:

# match div:
#     match class^=ab:
#         match sp^=dd
#     match .!class%=cc

# list abc:
#     match div:
#     match class^=ab:
#         match sp^=dd
#     match .!class%=cc

# json a use abc:
#     field name:
#         match a:
#             ret .!text    



html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div class="a">1234<a>666</a></div>
    <ul>
        <li>abc</li>
        <li>ddd</li>
        <li class="li">eeeeeeee111</li>
        <li>8882222eeee666</li>
        <li class="active">777777888</li>
    </ul>
    <ul open="789">
        <li>abc</li>
        <li>ddd</li>
        <li>eeeeeeee111</li>
        <li class="li">8882222eeee666</li>
        <li class="active">7777778881</li>
    </ul>
    <span>2333 yes i do</span>
    <div class="a">change you home</div>

</body>
</html>
"""
bs = BeautifulSoup(html,"html.parser")


list_save=dict()
json_save=dict()

# 创建json变量
def saveToJson(var):
    global json_save
    if var not in json_save:
        json_save[var]=dict()

# 赋值json字段
def field(var,field,val):
    global json_save
    if var not in json_save:
        json_save[var]=dict()
    if field is not None:
        json_save[var][field]=val

# 创建list变量
def saveToList(var,element_list):
    global list_save
    list_save[var]=element_list

def readFromList(var):
    global list_save
    return list_save[var]

# 返回一个内容
def ret(element_list):
    if len(element_list)>=1:
        return element_list[0]
    else:
        return None



# 匹配 标签
def match_findLabel(label,element_list):
    matchlist=[]
    for element in element_list:
        if element.name==label:
            matchlist.append(element)
    return matchlist

# 匹配 HTML内容
def match_findHtml(op,val,element_list):
    matchlist=[]
    for element in element_list:
        if op=="^":
            str1 =""
            for st in element.html.stripped_strings:
                str1+=re.sub(r'\n+','\n',st)
                if len(val)<len(str1):
                    break
            if str1.startswith(val):
                matchlist.append(element)
        elif op == "$":
            str1 =""
            for st in element.html.stripped_strings:
                str1+=re.sub(r'\n+','\n',st)
            if str1.endswith(val):
                matchlist.append(element)
        elif op == "%":
            str1 =""
            for st in element.html.strings:
                str1+=re.sub(r'\n+','\n',st)
            if str1.find(val)!=-1:
                matchlist.append(element)
    return matchlist

# 匹配 内容
def match_findText(op,val,element_list):
    matchlist = []
    for element in element_list:
        if op=="^":
            str1 =re.sub(r'\n+','\n',element.text)
            if str1.startswith(val):
                matchlist.append(element)
        elif op == "$":
            str1 =re.sub(r'\n+','\n',element.text)
            if str1.endswith(val):
                matchlist.append(element)
        elif op == "%":
            str1 =re.sub(r'\n+','\n',element.text)
            if str1.find(val)!=-1:
                matchlist.append(element)
        elif op =='/':
            str1 =re.sub(r'\n+','\n',element.text)
            if str1==val:
                matchlist.append(element)

    return matchlist

# 匹配 class
def match_findclass(_class,element_list):
    matchlist = []
    for element in element_list:
        if 'class' in element.attrs:
            if _class in element.attrs['class']:
                matchlist.append(element)
    return matchlist
                

# 匹配  属性
def match_findAttr(op,key,op1,val,element_list):
    matchlist = []
    for element in element_list:
        ok = False
        for _key in element.attrs:
            findkey=False
            if op =="^":
                findkey= _key.startswith(key)
            elif op=="$":
                findkey= _key.endswith(key)
            elif op=="%":
                findkey= _key.find(key)!=-1
            if findkey:
                attr_val = element.attrs[_key]
                if op1 =="^":
                    ok  = attr_val.startswith(val)
                elif op1=="$":
                    ok = attr_val.endswith(val)
                elif op1 == "%":
                    ok = attr_val.find(val)!=-1
                if ok:
                    break
        if ok:
            matchlist.append(element)
    return matchlist

savepoint_data=dict()
savepoint_id = 1
refer_point = [] # 无效id队列

# 保存数据进某内存
def add_savepoint(data):
    if len(refer_point)>0:
        pid = refer_point.pop()
        savepoint_data[pid]=data
        return pid
        
    savepoint_data[savepoint_id]=data
    savepoint_id+=1
    return savepoint_id-1

# 读取savepoint
def read_savepoint(id,delete):
    tmp = savepoint_data[id]
    if delete:
        del savepoint_data[id]
        refer_point.insert(0,id)
    return tmp

# 更新
def update_savepoint(id,data):
    if id in savepoint_data:
        savepoint_data[id]=data

def trimspace(str1):
    return re.sub(r'^\s+|\s+$','',str1)

def findOp(str1:str,start,end):
    loop = -1
    ov=[]
    while True:
        if len(ov)%2==0:
            loop = str1.find(start,loop+1)
            if str1[loop-1]=='/':
                print('out')
                continue
        else:
            loop = str1.find(end,loop+1)
            if str1[loop-1]=='/':
                print('out2')
                continue
        if loop!=-1:
            if len(ov)%2==0:
                ov.append(loop)
            else:
                ov.append(loop)
        else:
            break
        
    list2=[]
    for i in range(len(ov)):
        if i%2==0:
            list2.append(str1[ov[i]:ov[i+1]+1])
    return list2

class result(object):
    def __init__(self,type,data,level=0) -> None:
        self.type=type
        self.data=data
        self.level=level
    

def printtype(list1):
    str1="" 
    for i in list1:
        str1+=i.type+"="+str(i.data)+","
    return str1

def child_all(list1:list):
    matchlist =[]
    for it in list1:
        matchlist+=it.find_all()
    return matchlist

# -------------------------------------------------------------------
# label.*.* [^$%]attr[^$%]="" !html[^$%]="" !text[^$%]="":
def match_args(line:str,level:int,tree:list):
    label=''
    _class=[]
    _attr = dict()

    next = trimspace(line).endswith(':')
    if next:
        line=line[:-1]
    
    strv = findOp(line,'"','"')
    index=0
    for iv in strv:
        line=line.replace(iv,"{"+str(index)+"}")
        index+=1

    lines = line.split(' ')
    print('-----level=',level,'tree=',printtype(tree))
    # print(lines)
    # print('----')
    for mat in lines:
        if mat=='':
            continue

        if label=='' and mat[0] not in ['^','%','$','.','!','/']:
            label=mat
        
        if mat[0] == '.':
            for it in mat.split('.'):
                if it!='':
                    _class.append(it)
        
        if mat[0]=='!':
            if mat.startswith('!html'):
                mat2 = mat.replace('!html','').replace('=','').replace('{','').replace('}','')
                mat2 = trimspace(mat2)
                if mat2[0] not in ['%','^','$']:
                    _attr['html']=['/',strv[int(mat2)][1:-1].replace('/','')]
                else:
                    _attr['html']=[mat2[0],strv[int(mat2[1:])][1:-1].replace('/','')]
                pass
            elif mat.startswith('!text'):
                mat2 = mat.replace('!text','').replace('=','').replace('{','').replace('}','')
                mat2 = trimspace(mat2)
                if mat2[0] not in ['%','^','$']:
                    _attr['text']=['/',strv[int(mat2)][1:-1].replace('/','')]
                else:
                    _attr['text']=[mat2[0], strv[int(mat2[1:])][1:-1].replace('/','')]
                pass

        if mat[0] in ['^','$','%','/']:
            mat2 = mat.split('=')
            mat2_1 = trimspace(mat2[0])
            mat2_2 = trimspace(mat2[1])
            _attr[mat2_1]=[mat2_1[0],mat2_1[-1],strv[int(mat2_2[1:-1])][1:-1].replace('/','')]

    return [label,_class,_attr,tree,level,next]

# 匹配内容
def match(*args):
    if len(args)<=0:
        raise Exception('错误match')
    #label:str class:list attr:dict parentlist:list level # 之前的结果
    label = args[0]
    _class = args[1]
    _attr = args[2]
    _parent:list = args[3]
    _level =args[4]
    _next = args[5] # 是否有下一级
    list3=[]# 新解析出来的内容
    
    # last_list3=[]
    parent_list:list = None
    parent_list_level=0
    fined = False
    for parents in reversed(_parent):
        if parents.type=='match':
            # if parent_list is None and len(parents.data)>0 and parents.level < _level: # 上级match
            if parent_list is None and parents.level < _level: # 上级match
                fined=True
                parent_list=parents.data
                parent_list_level=parents.level
            # if parents.level == _level: #合并同级
            #     last_list3=last_list3+parents.data

    if len(_parent)<=0 or fined is False:
        global bs
        parent_list=bs.find_all() #全部

    if fined and len(_parent)>0 and parent_list_level < _level:
        parent_list = child_all(parent_list) #输出它下面所有child到parent_list


    # else:
    #     if  _parent[-1].type=='list':
    #         if len(_parent)>=2 and _parent[-2].type=='match': 
    #             parent_list = _parent[-2].data
    #     else:
    #         if  _parent[-1].type=='match':
    #             parent_list = _parent[-1].data # 上一级匹配的
    # if label=='a':
    #     pass

    if parent_list is not None:
        # label
        list3 = match_findLabel(label,parent_list)
        #class 
        for cls1 in  _class:
            list3 = match_findclass(cls1,list3)
        
        for k in _attr:
            v = _attr[k]
            if k =='text':
                if v[1]=='233':
                    pass
                list3 = match_findText(v[0],v[1],list3)
                continue
            if k =='html':
                list3 = match_findHtml(v[0],v[1],list3)
                continue
            # attr
            name = k[1:-1]
            # if name =="op":
            #     pass
            list3 =match_findAttr(v[0],name,v[1],v[2],list3)



    last_list_var = ''
    for index in reversed(range(len(args[3]))):
        res = args[3][index]
        if res.type=='list':
            last_list_var=res.data # var
            break
    output = list3
    if last_list_var!='' and _next is False:
        output = readFromList(last_list_var) + output
        saveToList(last_list_var,output)

    return result('match',output,_level)


# 读取文件
def file(*args):
    global bs
    f = open(args[0],"r",encoding="utf-8")

    html = ""
    for r in f.read():
        html=html+r
    bs = BeautifulSoup(html,"html.parser")
    return result('file',bs,args[1])

def file_args(line,level,tree):
    path = trimspace(line)
    return [path,level]


# 列表
def listfunc_args(line,level,tree):
    return [trimspace(line),level]

def listfunc(*args):
    saveToList(args[0],[])
    return result('list',args[0],args[1])

def printfunc_args(line,level,tree):
    return [line,readFromList(trimspace(line)),level]

def printfunc(*args):
    print(args[0],'print>',args[1])
    return result('print',None,args[1])


def json_args(line,level,tree):
    return []

def json(*args):
    pass




def field_args(line,level,tree):
    return []

def field(*args):
    pass




def ret_args(line,level,tree):
    return []

def ret(*args):
    pass

# -------------------------------------------------------------------


test = """
list hello
    match ul:
        match li .li

list abc
    match div .a !text^="change"
    match div !text^="233"

list cccc
    match div .a

list qqqq
    match span !text^="233"

list ddd
    match ul ^op^="7":
        match li .active

list dv
    match ul
        list qq
            match li .li
            match li .active

print abc
print cccc
print qqqq
print hello
print ddd
print dv
print qq
"""


def get_line_space(line):
    mat = re.match(r'^\s+',line)
    if mat != None:
        return mat.span()[1]
    else:
        return 0

# 解析代码
def analysis(strbody:str):
    syntax_table = {
        'match':match,
        'list':listfunc,
        'json':json,
        'field':field,
        'ret':ret,
        'file':file,
        'print':printfunc,
    }
    syntax_table_args={
        'match':match_args,
        'list':listfunc_args,
        'json':json_args,
        'field':field_args,
        'ret':ret_args,
        'file':file_args,
        'print':printfunc_args
    }
    # 缩进大小
    space = 0
    linelist = strbody.splitlines()
    for line in linelist:
        sp = get_line_space(line)
        if sp>0 and space ==0:
            space=sp
        if space>0 and sp % space >0:
            raise Exception('代码缩进错误')
    
    # 存储运行时每层的返回值，可供下一层使用
    lineIndex=dict()
    for _line in linelist:
        space1 = get_line_space(_line)
        line = re.sub(r'^\s+|\s+$','',_line)
        for syntax in syntax_table:
            if line.startswith(syntax):
                if space !=0:
                    level = int(space1/space)
                else:
                    level =0
                list2 = []

                # 开始一个新的list时清空tree上的所有节点
                if syntax=='list':
                    if level-1 in lineIndex:
                        if lineIndex[level-1].type=='match':
                            # 保留一个上级,如果上级是match
                            tmp = lineIndex[level-1]
                            lineIndex=dict()
                            lineIndex[level-1]=tmp
                        else:
                            lineIndex=dict()
                    else:
                        lineIndex=dict()
                    
                
                for iv in range(level+1):
                    if iv in lineIndex:
                        list2.append(lineIndex[iv])
                lineIndex[level]=syntax_table[syntax](*syntax_table_args[syntax](line[len(syntax):],level,list2))

        
    
analysis(test)