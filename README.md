# auto-review

用代码和电脑代替一些重复的步骤

## 例子

已完成 API 部分
```
//例如：点击 Code Review 标签
clickTab('Code Review');

//点击文件
clickFile('js/resources.js');

//点击第 10 行的代码
mouseDownInCode(10);

//评价为 awesome
reviewRate(RATE.awesome);

//评论
reviewComment("hello,world");

//保存
clickSaveButton();
```

## 将要做的功能
- 用正则表达式识别相关代码模板，将对应评论添加上 Review
- 识别网页读取的状态，避免冲突
- 利用智能加人工修改