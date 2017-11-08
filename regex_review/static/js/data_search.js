"use strict";

// search page searcher
document.getElementById("filter-text")
    .addEventListener("input", filterTextHandler); 

function filterTextHandler(event){
    var inputText = event.path[0].value;
    showReviewElement(inputText);
}

function showReviewElement(text) {
    var elements = getAllReviewsElement();
    for (var i = 0; i < elements.length; i++){
        var element = elements[i];
        setElementVisable(checkFilterReviewName(text, getReviewName(element)), element);
    }
}

function getReviewName(element) {
    return element.getElementsByTagName('a')[0].innerText;
}

function checkFilterReviewName(filterText, text) {
    if (text.length > 0){
        return (text.toLowerCase().indexOf(filterText.toLowerCase()) > -1);
    } else {
        return true;
    }
}

function getAllReviewsElement() {
    return document.getElementsByClassName('description');
}

//set @element visable if @isVisable is true
function setElementVisable(isVisable, element) {
    if (isVisable) {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}