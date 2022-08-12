function openFilter(evt, Filter) {
  var i, x, filters;
  x = document.getElementsByClassName("fcontent");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  filters = document.getElementsByClassName("filter");
  for (i = 0; i < x.length; i++) {
    filters[i].className = filters[i].className.replace(" filter_blue", ""); 
  }
  document.getElementById(Filter).style.display = "block";
  evt.currentTarget.className += " filter_blue";
}

function filterText() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.querySelector("#textlist");
    filter = input.value.toUpperCase();
    ul = document.querySelector("#textitems");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].querySelectorAll("label")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
function filterAuthor() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.querySelector("#authorlist");
    filter = input.value.toUpperCase();
    ul = document.querySelector("#authoritems");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].querySelectorAll("label")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
function filterGenre() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.querySelector("#genrelist");
    filter = input.value.toUpperCase();
    ul = document.querySelector("#genreitems");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].querySelectorAll("label")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function filTextRes() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.querySelector("#textres");
    filter = input.value.toUpperCase();
    ul = document.querySelector("#textresitems");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].querySelectorAll("label")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function filAuthRes() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.querySelector("#authres");
    filter = input.value.toUpperCase();
    ul = document.querySelector("#authresitems");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].querySelectorAll("label")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
function uncheckAll() {
  document.querySelectorAll('input[type="checkbox"]')
    .forEach(el => el.checked = false);
}

document.querySelector('button').addEventListener('click', uncheckAll)

function toggleFilter() {
  var x = document.querySelector("#filter_container");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}

function disableEmptyInputs(form) {
  var controls = form.elements;
  for (var i=0, iLen=controls.length; i<iLen; i++) {
    controls[i].disabled = controls[i].value == '';
  }
}

function updateRequirements() {
  var search2 = document.querySelector('#search2').value;
  if (search2 != null) {
    document.querySelector('#oper1').required = true;
  } else {
    document.querySelector('#oper1').required = false;
  }
}

function updateRequirements2() {
  var search3 = document.querySelector('#search3').value;
  if (search3 != null) {
    document.querySelector('#oper2').required = true;
  } else {
    document.querySelector('#oper2').required = false;
  }
}