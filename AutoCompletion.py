import sublime, sublime_plugin, os, re, codecs

root_dir = '/Users/baidu/workspace/fe'
namespace_dict = {}

# 插件加载 插件系统回调函数
def plugin_loaded():
    init_settings()

# 初始化配置
def init_settings():
    init_namesapce()
    
# 初始化namespace
def init_namesapce():
    for root, subFolders, files in os.walk(root_dir):
        # 忽略page文件夹
        if 'page' in subFolders:
            subFolders.remove('page')

        # 忽略widget文件夹
        if 'widget' in subFolders:
            subFolders.remove('widget')

        # 忽略static文件夹
        if 'static' in subFolders:
            subFolders.remove('static')

        # 忽略test文件夹
        if 'test' in subFolders:
            subFolders.remove('test')

        # 忽略plugin文件夹
        if 'plugin' in subFolders:
            subFolders.remove('plugin')

        # 查找fis-conf.js文件
        for f in files:
            if 'fis-conf.js' == f:
                # 以utf-8编码打开文件
                fis_conf = codecs.open(os.path.join(root, f), 'r', 'utf-8')
                for line in fis_conf.readlines():
                    # 查找namespace
                    search = re.search('namespace[\s\:]*[\"\']([\w-]+)[\"\']', line)
                    if search:
                        namespace_dict[search.group(1)] = root
                        break


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
                for t in s:
                    path += '/' + t
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
        regions = view.find_all('[\"\'].*[\"\']', sublime.IGNORECASE)
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
