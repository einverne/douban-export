豆瓣导出工具

工具包含 Python 版本和 JavaScript 版本。

## Python
Python 版本基于 Python 3.6.x ，其他版本暂未测试。

主要实现:

- 电影导出
- 书籍导出
- 音乐导出
- 日记导出

![result](screenshot/screenshot-output-result.png)

关于豆瓣相册导出可以参考我 [这个](https://github.com/einverne/douban-dl) 项目。

### 命令使用

设置

    douban-export setup
    
输入 uesr id，会将用户ID保存到 HOME 目录的 `~/.douban-export` 文件中，如果预先设置，一下的命令可以省略 `-u` 选项。

导出电影

    douban-export movie -u einverne -t wish -o wish_movie.csv

说明：

- `-t` 参数可以选择 `collect` 看过，`wish` 想看, `doing` 在看

导出书籍

    douban-export book -u einverne -t wish -o wish_book.csv
    
同理

    douban-export music -u einverne -t wish -o wish_music.csv
    

## JS

userscript 主要来自于

- douban-book-export.user.js
- douban-movie-export.user.js

分别来自于：

OpenUserJS

- <https://openuserjs.org/scripts/KiseXu/%E8%B1%86%E7%93%A3%E7%94%B5%E5%BD%B1%E5%AF%BC%E5%87%BA%E5%B7%A5%E5%85%B7/source>

DannyVim

- https://raw.githubusercontent.com/DannyVim/ToolsCollection/master/douban_book.js



## reference

- <https://github.com/chishui/douban-movie>






