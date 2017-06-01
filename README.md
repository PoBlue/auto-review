# auto-review

用程序代替一些低层次的审阅, 让我们能够更加高层次地思考并且审阅代码。提供更加**棒**的 Review 体验

## 功能
- 用正则表达式识别相关代码模板，将对应评论添加上 Review

## 环境

1. Flask , python 的一个库
2. Chrome 浏览器
3. Python 3.0 以上
4. Review 的语言需要是 `英文的`，如下图的, 评价，编辑等都是英文的
![en-version](http://i1.piimg.com/519918/1403ec45256c786f.png)

## 安装

1. 在 `Chrome` 打开链接： `chrome://extensions/`, 
2. 按下 `加载已解压的扩展程序`, 选择 `auto-review` 文件夹下的 `chrome-extension`
3. 加载完后会看到下图这个 *剑* 图标

![icon](http://i1.piimg.com/519918/9414bcf013c522d1.png)

## 使用

在 `terminal` 使用下面 `cd` 语句进入目录 `auto-review/regex_review`

```
cd /path/to/auto-review/regex_review
```

接着用以下语句开启本地服务器
```
python web_handler.py
```

如果成功，将会看到类似下面的信息
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 375-481-444
```

其中 Running on 后面的 http://127.0.0.1:5000/ 就是控制面板地址，在 Chrome 上打开。如下图：

![dashboord](http://i4.buimg.com/519918/569424ebf7aab847.png)

### 设置要解析项目的路径
随意创建一个文件夹用来存储要进行解析的项目，然后 `cd` 进去这个文件夹，譬如：文件夹 `projects`：
```
cd /path/to/projects
```

然后使用 `pwd` 命令获取路径，然后输入到下图里，按 `submit`

![dashboord](http://i4.buimg.com/519918/569424ebf7aab847.png)

成功了会看到下面这张图, 会列出这个文件下的所有文件夹，这些文件就是 Review 项目了:

![list projects](http://i1.piimg.com/519918/a84efbf243c613fa.png)

### 自动解析

挑选一个项目，然后按 `sumbit`

![select project](http://i1.piimg.com/519918/54d5eb1b5ae373a5.png)

进入下面这个界面

![review](http://i1.piimg.com/519918/a9382e531e697200.png)

挑选 `要进行解析的文件（可多选）` 和相对应项目的 `解析数据集` ，按 `提交`, 会看到页面返回 `sucessful` 代表解析成功了。

Tips：下一次的解析，可以在看到 `sucessful` 后, 按浏览器的后退，然后按 `挑选项目`，选择下一个项目进行解析

### 自动 Review

必须在上一步的 `自动解析` 看到 `sucessful` 信息后。才用 Chrome 打开相应的 `reivew`, 按下图标，再按 `start`，然后 Chrome console 和 Review 都会有相应的反馈，这时 **先不要动这个网页**, 喝杯茶。看到 Chrome 的 `console` 有 `finished` 字样时就完成了，可以进行操作了

![chrome](http://i4.buimg.com/519918/b1e801d6540b8119.png)


`finshed` 自动 Reivew ✅


![finshed](http://i4.buimg.com/519918/a4a5a5bbeac2fc31.png)

### 设置数据

按网页顶上的 `设置 Review 数据` 进行设置，会进入下面这个页面, 列出所有数据：

![data list](http://i4.buimg.com/519918/cbee5ef0e67ded95.png)

点击数据，譬如：ipnd_p0, 会进入到它里面每一条 Review 的简单描述


![review list](http://i1.piimg.com/519918/c5c9163279a4a7dc.png)

点击 Review 的描述，进入`编辑界面`。点击 Review 的 `复制`, 则可以将这个 Review 复制到其它的文件去。

按 `add new review data` 新建识别进行自动 Review 的数据，进入下面这个界面

![add new review data](http://i4.buimg.com/519918/25179fc7f9e3e802.png)

1. 【必填】为填写正则表达式的地方，用来识别代码符合的代码进行 Review
2. 【必填】描述这个数据的简介，会在列表中显示出来
3. 【必填】review，就是我们 review 代码评论的具体数据
4. 【可不勾】如果勾选了的，当 `1` 表达式没有匹配的代码。则使用 `6` 里的表达式，识别出相应代码位置进行 Review。
5. 【必填】评价
6. 【可不填】如 `4` 所描述，如果 `4` 没有勾选，那么就可以不填了

按 `submit` 创建数据

其中的数据 **需** 遵循下面的提到的 [守则](#守则)

## 推荐阅读
- [flask 文档](http://docs.jinkan.org/docs/flask/)
- [chrome 插件开发文档](https://developer.chrome.com/extensions/getstarted)
- [书：精通正则表达式](https://book.douban.com/subject/2154713/)
- [网页: python 正则表达式测试网站](http://pythex.org)

## 守则
迟点再写

## 建议
1. 正则表达式，在做不出十分精准的情况下，可以写个简单点的。因为我们这边还有人在看着。

## 将要做的功能
- 利用智能加人工修改

----------------

Rock it !!!!
