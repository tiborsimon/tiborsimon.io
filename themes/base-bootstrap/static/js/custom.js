// Bootstrap javascript triggers
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$(function () {
  $('[data-toggle="popover"]').popover()
})


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

