"use strict";

document.getElementById("filter-text")
    .addEventListener("input", filterTextHandler);

function getAllFilesElement() {
    return document.getElementById("files").getElementsByTagName("div");
}

function getFileName(element) {
    return element.getElementsByTagName("label")[0].innerHTML;
}

function showFileElement(text) {
    var elements = getAllFilesElement();
    for (var i = 0; i < elements.length; i++){
        var element = elements[i];
        setElementVisable(checkFilterFileName(text, getFileName(element)), element);
    }
}

function setElementVisable(isVisable, element) {
    if (isVisable) {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

function checkFilterFileName(filterText, text) {
    if (text.length > 0){
        return (text.toLowerCase().indexOf(filterText.toLowerCase()) > -1);
    } else {
        return true;
    }
}

function filterTextHandler(event){
    var inputText = event.path[0].value;
    showFileElement(inputText);
}