var DATA = [{
    "path": "build.gradle",
    "reviews": [{
        "lineNum": 2,
        "comment": "awesome code",
        "rate": "awesome"
    }, {
        "lineNum": 5,
        "comment": "you are well done",
        "rate": "awesome"
    }]
}];

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
    reviewRate(RATE.awesome);
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

var reviewData = new ReviewData(DATA);
var autoReview = new AutoReview(reviewData);
autoReview.start();
