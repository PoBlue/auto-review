function injectFile(fileName) {
    var s = document.createElement('script');
    s.src = chrome.extension.getURL(fileName);
    (document.head || document.documentElement).appendChild(s);
    s.onload = function () {
        s.parentNode.removeChild(s);
    };
}

injectFile('auto_review/result.js');