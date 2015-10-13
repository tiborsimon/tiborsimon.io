 // ----------------------------------------------------------------------------
// Bootstrap javascript triggers
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$(function () {
  $('[data-toggle="popover"]').popover()
})


 // ----------------------------------------------------------------------------
// Trigger modal by anchor - http://stackoverflow.com/questions/19874795/open-a-bootstrap-modal-automatically-from-an-external-link
$(document).ready(function () {
    var target = document.location.hash;
    function showModal(target){
        $(target).modal('show');
    }
    if (target.length) {
        showModal(target+'-modal');
    }
});


 // ----------------------------------------------------------------------------
// Helper function to find out state
function findBootstrapEnvironment() {
    var envs = ["xs", "sm", "md", "lg"],    
        doc = window.document,
        temp = doc.createElement("div");

    doc.body.appendChild(temp);

    for (var i = envs.length - 1; i >= 0; i--) {
        var env = envs[i];

        temp.className = "hidden-" + env;

        if (temp.offsetParent === null) {
            doc.body.removeChild(temp);
            return env;
        }
    }
    return "";
}

 // ----------------------------------------------------------------------------
// Auto resize for iframes http://stackoverflow.com/questions/819416/adjust-width-height-of-iframe-to-fit-with-content-in-it
// function autoResize(id){
//     var newheight;
//     var newwidth;

//     if(document.getElementById){
//         // newheight = document.getElementById(id).contentWindow.document .body.scrollHeight;
//         newwidth = document.getElementById(id).contentWindow.document .body.scrollWidth;
//     }

//     document.getElementById(id).height = (newheight) + "px";
//     document.getElementById(id).width = (newwidth) + "px";
// }


 // ----------------------------------------------------------------------------
// Redirect external links to new tab
// $('a').each(function() {
//    var a = new RegExp('/' + window.location.host + '/');
//    if(!a.test(this.href)) {
//        $(this).click(function(event) {
//            event.preventDefault();
//            event.stopPropagation();
//            window.open(this.href, '_blank');
//        });
//    }
// });


 // ----------------------------------------------------------------------------
// Adding background
// https://github.com/srobbin/jquery-backstretch
$.backstretch("http://tiborsimon.io/images/background2.jpg");


 // ----------------------------------------------------------------------------
// Irrelevant fading
var cookie_name = 'sidebar-fade'
var cookie_expires = 365;

function turn_on_fading() {
  $("#irrelevant-on-btn").prop('checked', true);
  $("#irrelevant-off-btn").prop('checked', false);
  $("#irrelevant-on-btn").parent().addClass('active');
  $("#irrelevant-off-btn").parent().removeClass('active');

  $(".irrelevant").addClass("irrelevant-fade");
}

function turn_off_fading() {
  $("#irrelevant-on-btn").prop('checked', false);
  $("#irrelevant-off-btn").prop('checked', true);
  $("#irrelevant-on-btn").parent().removeClass('active');
  $("#irrelevant-off-btn").parent().addClass('active');
  
  $(".irrelevant").removeClass("irrelevant-fade");
}

function process_fading() {
  var env = findBootstrapEnvironment()
  if (env == "xs" || env == "sm") {
    $("#irrelevant-toggle").css("display", "none");
    turn_off_fading();
  } else {
    $("#irrelevant-toggle").css("display", "block");
    if ($.cookie(cookie_name)) {
      turn_on_fading();
    } else {
      turn_off_fading();
    }
  }  
}

$(function () {
  process_fading();
});

window.addEventListener('resize', process_fading);

$("#irrelevant-on-btn").change(function () {
  if (confirm('By turning on this feature you allow tiborsimon.io to place a tiny cookie on your machine to remember this setting.')) { 
    $.cookie(cookie_name, 1, { expires: cookie_expires, path: '/' });
    process_fading();
  }
});

$("#irrelevant-off-btn").change(function () {
  $.removeCookie(cookie_name, { expires: cookie_expires, path: '/' });
  process_fading();
});


 // ----------------------------------------------------------------------------
// Mansory - http://codepen.io/SitePoint/pen/mywEMR/
$('.masonry-container').masonry({
  itemSelector: '.article-listing',
  columnWidth: '.article-listing'
});

$('.about-masonry').masonry({
  itemSelector: '.about-masonry-item',
  columnWidth: '.about-masonry-item'
});


 // ----------------------------------------------------------------------------
// Social Share kit - http://socialsharekit.com
SocialShareKit.init();

