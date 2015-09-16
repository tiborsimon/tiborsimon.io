// Bootstrap javascript triggers
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$(function () {
  $('[data-toggle="popover"]').popover()
})


 // ----------------------------------------------------------------------------
// Redirect external links to new tab
$('a').each(function() {
   var a = new RegExp('/' + window.location.host + '/');
   if(!a.test(this.href)) {
       $(this).click(function(event) {
           event.preventDefault();
           event.stopPropagation();
           window.open(this.href, '_blank');
       });
   }
});


 // ----------------------------------------------------------------------------
// Irrelevant fading
var cookie_expires = 365;
$(function () {
  if ($.cookie('irrelevant-off')) {
    $("#irrelevant-on-btn").prop('checked', false);
    $("#irrelevant-off-btn").prop('checked', true);
    $("#irrelevant-on-btn").parent().removeClass('active');
    $("#irrelevant-off-btn").parent().addClass('active');
    $(".irrelevant").css("opacity", "1");
    $(".irrelevant").removeClass("irrelevant-content");
  };
})

$(".irrelevant-content").mouseenter(function(){
    $(".irrelevant-content").css("opacity", "1");
});
$(".irrelevant-content").mouseleave(function(){
    $(".irrelevant-content").css("opacity", "0.1");
});

$("#irrelevant-on-btn").change(function () {
  $.removeCookie('irrelevant-off', { expires: cookie_expires, path: '/' });
  $(".irrelevant").css("opacity", "0.1");
  $(".irrelevant").addClass("irrelevant-content");
});

$("#irrelevant-off-btn").change(function () {
  $.cookie('irrelevant-off', '1', { expires: cookie_expires, path: '/' });
  $(".irrelevant-content").css("opacity", "1");
  $(".irrelevant").removeClass("irrelevant-content");
});

