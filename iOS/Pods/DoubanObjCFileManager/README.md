DoubanObjCFileManager
====
**DoubanObjCFileManager**是一个Objective-C实现的iOS文件管理库。

##使用方法
####1.获取源码
git submodule add http://code.dapps.douban.com/DoubanObjCFileManager.git yourPath/

####2. 导入
把项目目录中的FileManager文件夹添加到工程中即可。

##功能
1.支持复杂路径的文件管理，自动新建路径中不存在的目录，可以对文件进行分类。

2.json文件cache。可以保存json形式的字符串或者字典到自定义的文件中。

3.可以保存NDData，NSString，NSDictionary到自定义的文件中。

4.支持异步的读写功能。

Note:

1.主要有三种文件路径

- Cache File：~/Library/Cache 主要用于保存Cache文件。程序重新启动时不会被清空，但当系统空间不足时可能会被清空。

- Tmp File：~/tmp 主要用于保存临时文件。当程序重新启动时会被清空。

- Offline File：~/Library/Offline 主要用于保存离线数据。程序重新启动时不会被清空，且当系统空间不足也不会被清空。

##iOS文件分类以及存放路径的建议
- 关键数据内容：用户创建的数据文件，无法在删除后自动重新创建，且会备份到iClound中
	- 路径：主目录/Documents
	- 属性：不要设置"不备份"
	- 管理：iOS系统即时遇到存储空间不足的情况下，也不会清除，同时会备份到iTunes或iCloud中  

- 缓存数据 
	- 内容：可用于离线环境，可被重复下载重复生成，即时在离线时缺失，应用本身也可以正常运行
	- 路径：主目录/Library/Caches
	- 属性：默认
	- 管理：在存储空间不足的情况下，会清空， 并且不会被自动备份到iTunes和iCloud中

- 临时数据
	- 内容：应用运行时，为完成某个内部操作临时生成的文件
	- 路径：主目录/tmp
	- 属性：默认
	- 管理：随时可能被iOS系统清除，且不会自动备份到iTunes和iCloud，尽量在文件不再使用时，应用自己情况，避免对用户设备空间的浪费 

- 离线数据内容：与缓存数据类似，可以被重新下载和重建，但是用户往往希望在离线时数据依然能够托托地存在着
	- 目录：主目录/Documents  或 主目录/Library/自定义的文件夹
	- 属性：放于Documents下不需设置，放在自定义文件夹中需设置"不备份" 
	- 管理：与关键数据类似，即时在存储空间不足的情况下也不会清楚，应用自己应该清除已经不再使用的文件，以免浪费用户设备空间