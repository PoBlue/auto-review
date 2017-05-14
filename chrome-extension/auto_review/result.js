var DATA = [{"reviews": [{"lineNum": 0, "comment": "\u901a\u5e38\u5728\u7f16\u5199 html \u65f6\uff0c\u5728\u5f00\u5934\u7b2c\u4e00\u884c\u6dfb\u52a0 `Doctype` \u7684\u4ee3\u7801\u544a\u8bc9\u6d4f\u89c8\u5668\u6211\u4eec\u7528\u7684\u662f\u4ec0\u4e48\u7248\u672c\u7684 html \uff0c\u8ba9\u6d4f\u89c8\u5668\u66f4\u597d\u5730\u89e3\u6790\u5448\u73b0\u7f51\u9875\n```\n<!DOCTYPE html>```", "rate": "suggestion"}], "path": "notes.html"}];
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var Repeat = function(time, func) {
    this.time = time;
    this.func = func; 
    this.isEnd = false;
    this.index = 0;
};

Repeat.prototype.repeateInInterval = function (){
    var self = this;
    if (self.isEnd === true) {
        return;
    }
    sleep(self.time).then(() => {
        self.func();
        self.repeateInInterval();
    });
};

Repeat.prototype.repeateWithIndex = function (totalTime) {
    var self = this;
    if (self.index > totalTime || self.isEnd === true){
        return;
    }
    sleep(self.time).then(() => {
        self.func(self.index);
        self.index = self.index + 1;
        self.repeateWithIndex(totalTime);
    });
};

var ReviewData = function(data) {
    this.data = data;
};

ReviewData.prototype.getDatasLength = function() {
    return this.data.length;
};

ReviewData.prototype.getReviewsLength = function(pathIndex) {
    return this.data[pathIndex].reviews.length;
};

ReviewData.prototype.getPath = function (pathIndex) {
    return this.data[pathIndex].path;
};

ReviewData.prototype.getReview = function (pathIndex, reviewIndex) {
    return this.data[pathIndex].reviews[reviewIndex];
};

ReviewData.prototype.getLineNum = function (pathIndex, reviewIndex) {
    return this.getReview(pathIndex, reviewIndex).lineNum;
};

ReviewData.prototype.getLineComment = function (pathIndex, reviewIndex) {
    return this.getReview(pathIndex, reviewIndex).comment;
};

ReviewData.prototype.getRate = function (pathIndex, reviewIndex) {
    var returnRate = RATE.awesome;
    switch (this.getReview(pathIndex, reviewIndex).rate){
    case "awesome":
        returnRate = RATE.awesome;
        break;
    case "suggestion":
        returnRate = RATE.suggestion;
        break;
    case "require":
        returnRate = RATE.require;
        break;
    default:
        console.log('error in getRate funtion');
    }
    
    return returnRate;
};

var AutoReview = function(reviewData){
    this.tab = "Code Review";
    this.pathIndex = 0;
    this.reviewIndex = 0;
    this.data = reviewData;
};

AutoReview.prototype.start = function () {
    var self = this;
    var mainRepeat = new Repeat();
    mainRepeat.time = 1000;
    mainRepeat.func = function () {
        if (isLoadedPageContent() === true) {
            clickTab(self.tab);
            self.selectFile();
            this.isEnd = true;
        }
    };
    mainRepeat.repeateInInterval();
};

AutoReview.prototype.selectFile = function(){
    var self = this;
    clickFile(this.data.getPath(this.pathIndex));

    var reviewRepeat = new Repeat(1000, function(){
        if (isLoadedCode() === true) {
            this.isEnd = true;
            self.selectCode();
        }
    });
    reviewRepeat.repeateInInterval();
};

AutoReview.prototype.selectCode = function () {
    var self = this;
    mouseDownInCode(this.data.getLineNum(this.pathIndex,this.reviewIndex));

    var rateRepeat = new Repeat(1000, function () {
        if (isLoadedReviewRates() === true) {
            this.isEnd = true;
            self.comment();
        }
    });
    rateRepeat.repeateInInterval();
};

AutoReview.prototype.comment = function () {
    var self = this;
    var lineNum = this.data.getLineNum(this.pathIndex, this.reviewIndex);
    reviewRate(this.data.getRate(this.pathIndex, this.reviewIndex));
    reviewComment(this.data.getLineComment(this.pathIndex,this.reviewIndex));
    clickSaveButton();
    var saveRepeat = new Repeat(1000, function () {
        if (isSavedComment(lineNum) === true) {
            this.isEnd = true;
            self.saved();
        }
    });
    saveRepeat.repeateInInterval();
};

AutoReview.prototype.saved = function () {
    if (this.reviewIndex < this.data.getReviewsLength(this.pathIndex) - 1) {
        this.reviewIndex += 1;
        this.selectCode();
    } else if (this.pathIndex < this.data.getDatasLength() - 1) {
        this.pathIndex += 1;
        this.reviewIndex = 0;
        this.selectFile();
    }
    console.log("finished");
};
function clickTab(tabName) {
    $('.navbar-item').filter(function () {
        return $(this).text() == tabName;
    }).trigger("click");
}

function clickFile(fileName) {
    $('.code-section-item-title strong').filter(function () {
        return $(this).text() == fileName;
    }).trigger("click");
}

//创建鼠标事件
function mouseEvent(type, sx, sy, cx, cy) {
  var evt;
  var e = {
    bubbles: true,
    cancelable: (type != "mousemove"),
    view: window,
    detail: 0,
    screenX: sx, 
    screenY: sy,
    clientX: cx, 
    clientY: cy,
    ctrlKey: false,
    altKey: false,
    shiftKey: false,
    metaKey: false,
    button: 0,
    relatedTarget: undefined
  };
  if (typeof( document.createEvent ) == "function") {
    evt = document.createEvent("MouseEvents");
    evt.initMouseEvent(type, 
      e.bubbles, e.cancelable, e.view, e.detail,
      e.screenX, e.screenY, e.clientX, e.clientY,
      e.ctrlKey, e.altKey, e.shiftKey, e.metaKey,
      e.button, document.body.parentNode);
  } else if (document.createEventObject) {
    evt = document.createEventObject();
    for (prop in e) {
    evt[prop] = e[prop];
  }
    evt.button = { 0:1, 1:4, 2:2 }[evt.button] || evt.button;
  }
  console.log('create event');
  return evt;
}

//传递事件
function dispatchEvent (el, evt) {
  if (el.dispatchEvent) {
    el.dispatchEvent(evt);
  } else if (el.fireEvent) {
    el.fireEvent('on' + type, evt);
  }
  console.log('dispath event');
  return evt;
}

//点击第几行代码
function mouseDownInCode(lineNumber) {
    //test: console log 
    console.log("mouse down in code: " + lineNumber);

    var codeElement = $(".CodeMirror-code").children().eq(lineNumber - 1);
    var codeY = codeElement.offset().top - $(document).scrollTop();

    var event = mouseEvent("mousedown", 0, 0, 300, codeY);
    var elements = document.getElementsByClassName("CodeMirror-code");
    dispatchEvent(elements[0], event);
}

function isLoadedReviewRates () {
    var editor = $(".comment-editor:not(.ng-hide)");
    return editor.find("input").length !== 0;
}

//建议评价
function reviewRate(rate) {
    var editor = $(".comment-editor:not(.ng-hide)");
    editor.find("input").filter(function () {
        return $(this)[0].value == rate;
    }).click().click();
}

//review 的具体内容
function reviewComment(text) {
    var editor = $(".comment-editor:not(.ng-hide)");
    var textArea = editor.find("textarea");
    textArea[0].value = text;
    textArea.trigger('change');
}

function clickSaveButton() {
    $(".comment-container button").filter(function (){
        return $(this).attr("busy-click") == "submitComment()"; 
    }).click();
}

function isLoadedTab() {
    return $("#page-content .container-fluid").children().filter(function () {
        return $(this).attr("ng-show") == "loading";
    }).hasClass('ng-hide');
}

function isLoadedCode() {
    return $(".code-section-item-body .ng-isolate-scope").children().filter(function () {
        return $(this).attr("ng-show") == "isLoading";
    }).hasClass('ng-hide');
}

function isSavedComment(lineNumber) {
    return $(".CodeMirror-code").children().eq(lineNumber - 1)
            .find(".CodeMirror-linewidget").length !== 0;
}

function isLoadedPageContent() {
    return $('#page-content .container-fluid').children().filter(function () {
        return $(this).attr("ng-show") == "loading";
    }).hasClass('ng-hide');
}

var RATE = {
    'awesome': 'awesome',
    'suggestion': 'nitpick',
    'require': 'critical'
};

// //例如：点击 Code Review 标签
// clickTab('Code Review');

// //点击文件
// clickFile('js/resources.js');

// //点击第 10 行的代码
// mouseDownInCode(10);

// //reviewRate
// reviewRate(RATE.awesome);

// //review comment
// reviewComment("hello,world");

// //click save button
// clickSaveButton();
var reviewData = new ReviewData(DATA);
var autoReview = new AutoReview(reviewData);
autoReview.start();
console.log("start reviewing");
