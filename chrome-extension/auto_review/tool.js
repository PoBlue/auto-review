function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var Repeat = function(time, func) {
    this.time = time;
    this.func = func; 
    this.isEnd = false;
    this.index = 0;
};

Repeat.prototype.repeateInInterval = function (){
    var self = this;
    if (self.isEnd === true) {
        return;
    }
    sleep(self.time).then(() => {
        self.func();
        self.repeateInInterval();
    });
};

Repeat.prototype.repeateWithIndex = function (totalTime) {
    var self = this;
    if (self.index > totalTime || self.isEnd === true){
        return;
    }
    sleep(self.time).then(() => {
        self.func(self.index);
        self.index = self.index + 1;
        self.repeateWithIndex(totalTime);
    });
};