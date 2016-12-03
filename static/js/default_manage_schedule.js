/**
 * Created by kayatomic on 12/2/16.
 */

var app = function() {
    var self = {};

    Vue.config.silent = false;

    self.vue = new Vue({

    });

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});