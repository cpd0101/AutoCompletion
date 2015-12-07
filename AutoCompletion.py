import sublime, sublime_plugin, os, re, codecs

workspace_dir = '/Users/baidu/workspace/fe'
namespace_dict = {}

# 插件加载 插件系统回调函数
def plugin_loaded():
    init_settings()

# 初始化配置
def init_settings():
    init_namespace()
  
# 初始化namespace
def init_namespace():
    for root, subFolders, files in os.walk(workspace_dir):
        # 需要忽略的文件夹
        ignores = ['page', 'plugin', 'static', 'test', 'widget']
        for folder in ignores:
            if folder in subFolders:
                subFolders.remove(folder)

        # 当前目录是否存在fis-conf.js文件
        if 'fis-conf.js' in files:
            # 以utf-8编码打开fis-conf.js文件
            fis_conf = codecs.open(os.path.join(root, 'fis-conf.js'), 'r', 'utf-8')
            # 查找文件内的namespace
            search = re.search('namespace[\s\:]*[\"\']([\w-]+)[\"\']', fis_conf.read())
            if search:
               namespace_dict[search.group(1)] = root 


# AutoCompletionCommand名字中Command为必须的
# AutoCompletionCommand将会转换成下划线风格auto_completion
class AutoCompletionCommand(sublime_plugin.EventListener):
    # completion list function
    def on_query_completions(self, view, prefix, locations):
        # print(prefix)
        snippets = []

        # fis namespace 自动映射
        regions = view.find_all('[\"\'][\w-]+:.*[\"\']', sublime.IGNORECASE)
        for r in regions:
            if r.contains(locations[0]):
                s = view.substr(r).split(':')
                path = namespace_dict.get(s[0][1:])
                s = s[1].split('/')
                s = s[:len(s) - 1]
                path = os.path.join(path, '/'.join(s))
                file_list = os.listdir(path)
                for f in file_list:
                    if f.startswith('.'):
                        continue
                    if '.' in f:
                        snippets += [(f, f)]
                    else:
                        snippets += [(f + '/', f + '/')]
                return snippets

        # 提示 fis namespace
        regions = view.find_all('[\"\'][\"\']', sublime.IGNORECASE)
        for r in regions:
            if r.contains(locations[0]):   
                for k in namespace_dict:
                    if re.match(prefix, k):
                        snippets += [(k + ':', k + ':')]
                return snippets

        if len(prefix) < 1:
            return snippets
        
        # 提示匹配单词 前缀匹配 并且不区分大小写
        regions = view.find_all('[^\w-]' + prefix + '[\w-]*', sublime.IGNORECASE)
        strs = []

        for r in regions:
            s = view.substr(r)[1:]
            if s not in strs and s != prefix:
                strs.append(s)

        for x in strs:
            snippets += [(x + ' <AutoCompletion>', x)]

        # print(snippets)

        return snippets
