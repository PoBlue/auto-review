function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var Repeat = function(time, func) {
    this.time = time;
    this.func = func; 
};

Repeat.prototype.repeateInInterval = function (){
    var self = this;
    sleep(self.time).then(() => {
        self.func();
        self.repeateInInterval();
    });
};