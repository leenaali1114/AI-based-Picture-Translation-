var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("myHeader").style.top = "0";
  } else {
    document.getElementById("myHeader").style.top = "-90px";
  }
  prevScrollpos = currentScrollPos;
};

function openNav() {
	document.getElementById("mySidenav").style.width = "100%";
}
  
function closeNav() {
	document.getElementById("mySidenav").style.width = "0";
}

function myFunction() {
	var copyText = document.getElementById("translation-result");
	copyText.select();
	document.execCommand("copy");
}

function showInfo(s) {
  if (s) {
    var message = messages[s];
    $("#info").html(message.msg);
    $("#info").removeClass();
    $("#info").addClass('alert');
    $("#info").addClass(message.class);
  } else {
    $("#info").removeClass();
    $("#info").addClass('d-none');
  }
}