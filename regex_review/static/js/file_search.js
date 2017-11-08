"use strict";

//data list page searcher
document.getElementById("filter-file")
    .addEventListener("input", filterFileHandler);

// data list page searcher handler
function filterFileHandler(event) {
    var inputText = event.path[0].value;
    showFileElement(inputText)
}

//show file element
function showFileElement(text) {
    var elements = getAllFilesElement();
    for (var i = 0; i < elements.length; i++){
        var element = elements[i];
        setElementVisable(checkFilterReviewName(text, getFileNameFromElement(element)), element);
    }
}

// return true if @text is in @filterText
function checkFilterReviewName(filterText, text) {
    if (text.length > 0){
        return (text.toLowerCase().indexOf(filterText.toLowerCase()) > -1);
    } else {
        return true;
    }
}

// get elements that class is data-file
function getAllFilesElement() {
    return document.getElementsByClassName('data-file');
}

//get file name
function getFileNameFromElement(element) {
    return element.getElementsByTagName('a')[0].innerText;
}

//set @element visable if @isVisable is true
function setElementVisable(isVisable, element) {
    if (isVisable) {
        element.style.display = "list-item";
    } else {
        element.style.display = "none";
    }
}