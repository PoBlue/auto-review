"use strict";

new Clipboard('.copy-paste', {
    text: function(trigger) {
        return trigger.getAttribute('value'); 
    }
});