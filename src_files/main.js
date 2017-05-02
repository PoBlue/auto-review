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

var reviewData = new ReviewData(DATA);
var autoReview = new AutoReview(reviewData);
autoReview.start();
