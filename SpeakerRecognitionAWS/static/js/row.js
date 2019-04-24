

var addButton = document.getElementById("addrow");
addButton.addEventListener("click", addButtonFunction);


var submitButton = document.getElementById("submitButton");
submitButton.addEventListener("click", submitButtonFunction);

counter = 0;

function addButtonFunction() {

  var newRow = $("<tr>");
  var cols = "";
  cols +=  '<td> <p> Speaker ' + counter + '</p></td>';
  cols +=  '<td><input type="text" class="form-control" name="name' + counter + '"/></td>';
  newRow.append(cols);
  $("table.order-list").append(newRow);
  counter++;
}

function deleteButtonFunction() {
  $(this).closest("tr").remove();
  counter -= 1
}

function submitButtonFunction() {
  var table = document.getElementById('myTable');
  // var x = document.getElementsByTagName("input")[4].value;

  var names = [];
  var i;
  var total = counter;
  for (i = 4; i < (4 + total); i++) {
    names.push(document.getElementsByTagName("input")[i].value);
  }
  alert(names);

  var fd = new FormData();
  fd.append('names', names);
  $.ajax({
      type: 'POST',
      url: '/postNames',
      data: fd,
      processData: false,
      contentType: false
  });


}
