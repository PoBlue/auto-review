var mainRepeat = new Repeat();

mainRepeat.time = 1000;
mainRepeat.func = function(){
    var self = this;
    if (isLoadedPageContent() === true){
        clickTab("Code Review");
        console.log("success");
        review('README.md', 2, "you are well done");
        self.isEnd = true; 
    }
};

function review(path, lineNum, comment){
    clickFile(path);
    var reviewRepeat = new Repeat(1000, function(){
        var self = this;
        if (isLoadedCode() === true) {
            self.isEnd = true;
            mouseDownInCode(lineNum);
            var rateRepeat = new Repeat(1000, function(){
                if (isLoadedReviewRates() === true) {
                    console.log("review?");
                    reviewRate(RATE.awesome);
                    reviewComment(comment);
                    clickSaveButton();
                    this.isEnd = true;
                    var saveRepeat = new Repeat(1000, function () {
                        if (isSavedComment() === true) {
                            console.log("finished");
                            this.isEnd = true;
                        }
                    });
                    saveRepeat.repeateInInterval();
                }
            });
            rateRepeat.repeateInInterval();
        }
    });
    reviewRepeat.repeateInInterval();
}

mainRepeat.repeateInInterval();