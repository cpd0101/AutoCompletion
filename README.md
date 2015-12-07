# AutoCompletion

#### 这是一个fis模块自动提示的Sublime Text插件
* 在sublime中输入''或""会自动提示所有的fis模块以及fis模块下的文件与目录，方便大家对文件进行。
* 非fis模块文件与目录的提示推荐用AutoFileName插件，这里就不重复造轮子了。
* 已经输入过的单词会自动前缀匹配提示（单词里可以有-连字符），这个主要是解决某些时候输入过的单词并不会自动提示，省去了重复输入的工作量。

#### 安装与配置
* 下载本项目，比如：git clone https://github.com/cpd0101/AutoCompletion
* 进入packages目录：Sublime Text -> Preferences -> Browse Packages...
* 复制下载的AutoCompletion目录到刚才的packges目录里。
* 打开AutoCompletion.py，将 workspace_dir = '/workspace/fe' 里的'/workspace/fe'修改成自己的工作目录然后保存即可。

#### 兼容性
* 只在Sublime Text 3上进行过测试，如遇兼容性问题请及时反馈。