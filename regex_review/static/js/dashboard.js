"use strict";

document.getElementById("filter-text")
    .addEventListener("input", filterTextHandler);

document.getElementById("filter-data-review-text")
    .addEventListener("input", filterReviewDataHandler);

//handler for id: filter-data-review-text
function filterReviewDataHandler(event) {
    var inputText = event.path[0].value;
    showReviewDataElement(inputText);
}

//show review data according text
function showReviewDataElement(text) {
    var elements = getAllReviewsElement();
    for (var i = 0; i < elements.length; i++){
        var element = elements[i];
        setElementVisable(checkFilterFileName(text, getFileName(element)), element);
    }
}

//get all reviews
function getAllReviewsElement() {
    return document.getElementById("review-data-files").getElementsByTagName("div");
}

function getAllFilesElement() {
    return document.getElementById("files").getElementsByTagName("div");
}

//get file name according to the element
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