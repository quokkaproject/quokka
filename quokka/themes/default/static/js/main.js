$('.root-menu-item').hover(
    function(){
        var menu_id = $(this).attr('id')
        $("." + menu_id).toggleClass('hidden-menu');
    },
    function(){
        var menu_id = $(this).attr('id')
        $("." + menu_id).toggleClass('hidden-menu');
    }
)