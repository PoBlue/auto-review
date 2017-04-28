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
  return evt;
}

//传递事件
function dispatchEvent (el, evt) {
  if (el.dispatchEvent) {
    el.dispatchEvent(evt);
  } else if (el.fireEvent) {
    el.fireEvent('on' + type, evt);
  }
  return evt;
}

//点击第几行代码
function mouseDownInCode(lineNumber) {
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

function isSavedComment() {
    return $(".comment-container button").filter(function (){
        return $(this).attr("busy-click") == "submitComment()"; 
    }).prop('disabled');
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