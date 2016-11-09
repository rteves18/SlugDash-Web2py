// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    self.add_load = function (){
        self.add_post();
        self.get_posts();

        self.get_posts();
    };

    // gets the post url
    function get_posts_url(start_idx, end_idx) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx
        };
        return posts_url + "?" + $.param(pp);
    };

    // displays the number of posts
    self.get_posts = function () {
        $.getJSON(get_posts_url(0, 4), function (data) {
            self.vue.posts = data.posts;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
        })
    };

     self.load_current_post = function () {
         var num_posts = self.vue.posts.length;
        $.getJSON(get_posts_url(0, num_posts), function (data) {
            self.vue.posts = data.posts;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
        })
    };

    // gets more post to display
    self.get_more = function () {
        var num_posts = self.vue.posts.length;
        $.getJSON(get_posts_url(num_posts, num_posts + 4), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.posts, data.posts);
        });
    };

    // add post button toggle
    self.add_post_button = function () {
        // The button to add a track has been pressed.
        //if(self.vue.logged_in)
        self.vue.is_adding_post = !self.vue.is_adding_post;
    };

    // adds posts to db
    self.add_post = function() {
        $.post(add_post_url, {
                post_content: self.vue.form_post
            },
            function (data) {
                //$.web2py.enableElement($("#add_post_submit"));
                self.vue.posts.unshift(data.post);
                self.vue.form_post = "";
                self.vue.add_post_button(); // toggle the form so it goes away after submitting
                //enumerate(self.vue.posts);
            });
    };

    // edit post button toggle
    self.edit_post_button = function(post_id) {
        self.vue.is_edit = !self.vue.is_edit;
        self.vue.edit_id = post_id;
    };

    self.edit_post = function (post_id, new_content) {
        if(self.vue.is_edit)
            self.vue.is_edit = !self.vue.is_edit;

        $.post(edit_post_url,
            {
                post_id: post_id,
                post_content: new_content
            });
        self.load_current_post();
        self.load_current_post();
    };

    self.edit_cancel_button = function(){
        if(self.vue.logged_in)
        self.vue.is_edit = !self.vue.is_edit;
        self.load_current_post();
    };

    // delete posts from db
    self.delete_post = function(post_id) {
        $.post(del_post_url,
            {
                post_id: post_id
            },
            function () {
                var idx = null;
                for (var i = 0; i < self.vue.posts.length; i++) {
                    if (self.vue.posts[i].id === post_id) {
                        // If I set this to i, it won't work, as the if below will
                        // return false for items in first position.
                        idx = i + 1;
                        break;
                    }
                }
                if (idx) {
                    self.vue.posts.splice(idx - 1, 1);
                }
            }
        )
    };

    // fields and methods declaration
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_adding_post: false,
            posts: [],
            logged_in: false,
            has_more: false,
            is_edit: false,
            form_post: null,
            edit_post_id: 0,
            updated_on: null,
            new_content: null,
            edit_time: null,
            is_updated: false
            //edit_content: null,
            //edit_old: null
        },
        methods: {
            get_more: self.get_more,
            add_post_button: self.add_post_button,
            add_post: self.add_post,
            edit_post: self.edit_post,
            delete_post: self.delete_post,
            edit_post_button: self.edit_post_button,
            add_load: self.add_load,
            edit_cancel_button: self.edit_cancel_button,
            load_current_post: self.load_current_post
        }
    });

    self.get_posts();
    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
