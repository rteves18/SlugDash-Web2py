/**
 * Created by kayatomic on 12/2/16.
 */

var app = function() {
    var self = {};

    Vue.config.silent = false;

    self.start_shift = function (){
        self.vue.is_on_shift = true;
        // Calls the server
        $.post(start_shift_url,
            {
                is_on_shift: self.vue.is_on_shift,
                driver_location: self.vue.driver_location,
            },
            function (data) {
                self.vue.driver_location = 'Select a location';
            }
        );
    };

    self.end_shift = function (){
        // Calls the server
        $.post(end_shift_url,
            {

            },
            function (data) {

            }
        );
    };

    self.send_data_to_server = function () {
        // Calls the server
        $.post(post_schedule_url,
            {
                driver_location: self.vue.driver_location,
                is_on_shift: self.vue.is_on_shift,
            },
            function (data) {
                // The order was successful.
                self.vue.driver_location = 'Select a location';
            }
        );
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_on_shift: false,
            driver_location: 'Select a location',
        },
        methods: {
            start_shift: self.start_shift,
            end_shift: self.end_shift,
            send_data_to_server: self.send_data_to_server,
        }
    });

    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});