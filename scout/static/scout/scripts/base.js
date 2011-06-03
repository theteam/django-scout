$.scout = new Object();

$.scout.visibility = {
    init: function() {
        this.$projects = $('ul.project-list li');
        this.$projects.click($.proxy(this, 'toggleVisibility'));
    },
    toggleVisibility: function(e) {
        var $target = $(e.currentTarget);
        var $extra_details = $target.find('.extra-details');
        $extra_details.slideToggle();
    }
};

$(document).ready(function() {
    $.scout.visibility.init();
});
