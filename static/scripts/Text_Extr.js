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

var selDiv = "";
	
document.addEventListener("DOMContentLoaded", init, false);

function init() {
	document.querySelector('#file').addEventListener('change', handleFileSelect, false);
	selDiv = document.querySelector("#selectedfiles");
}
	
function handleFileSelect(e) {
	
	if(!e.target.files) return;
	
	selDiv.innerHTML = "";
	
	var files = e.target.files;
	for(var i=0; i<files.length; i++) {
		var f = files[i];
		
		selDiv.innerHTML += '<li class="list-group-item d-flex justify-content-between align-items-center">' + f.name + '<span class="close" onclick="removeItem($(this))">x</span><li/>';
	}
}

function removeItem(item) {
	item.parent().remove();

	selDiv.innerHTML = "";

	var files = e.target.files;
	for(var i=0; i<files.length; i++) {
		var f = files[i];
		console.log(f);
		console.log(item);
		if (f != item) {
			selDiv.innerHTML += '<li class="list-group-item d-flex justify-content-between align-items-center">' + f.name + '<span class="close" onclick="removeItem($(this))">x</span><li/>';
		}
	}
}

$( document ).ready(function(){
	if($("#alert").length){
		$('#alert').fadeIn('slow', function(){
			$('#alert').delay(5000).fadeOut(); 
		});
	}
});

function myFunction() {
	var copyText = document.getElementById("text");
	copyText.select();
	document.execCommand("copy");
  }