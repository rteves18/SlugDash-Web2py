/**
 * Created by kayatomic on 12/2/16.
 */

var app = function() {
    var self = {};

    Vue.config.silent = false;

    self.start_shift = function (){
        self.vue.is_on_shift = true;
        console.log(self.vue.driver_location);
        if(self.vue.driver_location == 'safeway'){
            self.vue.is_at_safeway = true;
        } else if(self.vue.driver_location == 'seven'){
            self.vue.is_at_seveneleven = true;
        } else if(self.vue.driver_location == 'eight'){
            self.vue.is_at_ferrells = true;
        } else {

        }
        // Calls the server
        $.post(start_shift_url,
            {
                is_on_shift: self.vue.is_on_shift,
                driver_location: self.vue.driver_location,
                is_at_safeway: self.vue.is_at_safeway,
                is_at_seveneleven: self.vue.is_at_seveneleven,
                is_at_ferrells: self.vue.is_at_ferrells,
            },
            function (data) {
                self.vue.driver_location = 'Select a location';
            }
        );
        self.get_schedule();
        self.vue.goto('on_shift');
        self.vue.refreshPage();
    };

    self.end_shift = function (){
        self.vue.is_on_shift = false;
        if(self.vue.driver_location == 'safeway'){
            self.vue.is_at_safeway = false;
        } else if(self.vue.driver_location == 'seven'){
            self.vue.is_at_seveneleven = false;
        } else if(self.vue.driver_location == 'eight'){
            self.vue.is_at_ferrells = false;
        } else {

        }
        // Calls the server
        $.post(end_shift_url,
            {

            },
            function (data) {

            }
        );
        self.vue.goto('default');

    };

    /* GO TO PAGE */
    self.goto = function (page) {
        //self.get_orders();
        self.vue.page = page;
    };

    self.warn = function(message, event){
      if (event) event.preventDefault();
      alert(message);
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

    self.get_schedule = function () {
        $.getJSON(get_schedule_url, $.param({q: self.vue.page}), function(data) {

        });
    };

    self.refreshPage = function () {
        window.location.reload();
    };

    self.test = function () {
        console.log("HELLO");
    };

    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_on_shift: false,
            driver_location: 'Select a location',
            page: 'default',
            is_at_safeway: false,
            is_at_ferrells: false,
            is_at_seveneleven: false,
        },
        methods: {
            get_schedule: self.get_schedule,
            start_shift: self.start_shift,
            end_shift: self.end_shift,
            send_data_to_server: self.send_data_to_server,
            goto: self.goto,
            warn: self.warn,
            test: self.test,
        }
    });

    self.get_schedule();
    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});