var s = document.createElement('script');
s.src = chrome.extension.getURL('auto_review/review_functions.js');
(document.head||document.documentElement).appendChild(s);
s.onload = function() {
    s.parentNode.removeChild(s);
};

console.log("test");