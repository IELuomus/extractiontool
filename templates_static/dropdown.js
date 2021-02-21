function showHideTextField(question) {
  var div = document.getElementById(`add-field-${question}`);
  var select = document.getElementById(question)
  var selected_option = select.options[select.selectedIndex].value
  if (div.style.display == "flex") {
    div.style.display = "none"
  } else {
    div.style.display = "flex";
    div.getElementsByTagName("input")[0].value = selected_option
  }
}

function showHideAddNewFieldElement() {
  var div = document.getElementById('add-field');
  div.style.display = div.style.display == "none" ? "flex" : "none"
}

function addOption(question) {
  var div = document.getElementById(`add-field-${question}`);
  var select = document.getElementById(question);
  var answer = div.getElementsByTagName("input")[0].value
  select.options[select.options.length] = new Option((answer, answer));
  select.selectedIndex = select.options.length - 1;
  div.style.display = "none"
}
