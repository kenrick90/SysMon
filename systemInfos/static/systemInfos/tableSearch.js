function searchProcessTable() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("processInput");

  filter = input.value
  table = document.getElementById("processTable");

  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 1; i < tr.length; i++)
  {
    isthere=false;
    tds = tr[i].getElementsByTagName("td")
    for (j = 0; j < tds.length; j++)
    {
        td = tds[j];
        if (td)
        {
          txtValue = td.textContent || td.innerText;
          if (txtValue.indexOf(filter) > -1)
          {
            isthere=true;
            break;
          }
        }
    }
    if(isthere==true)
    {
        tr[i].style.display = "";
    }
    else
    {
        tr[i].style.display = "none";
    }
  }
}

function searchLogTable() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("logInput");

  filter = input.value
  table = document.getElementById("logTable");

  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 1; i < tr.length; i++)
  {
    isthere=false;
    tds = tr[i].getElementsByTagName("td")
    for (j = 0; j < tds.length; j++)
    {
        td = tds[j];
        if (td)
        {
          txtValue = td.textContent || td.innerText;
          if (txtValue.indexOf(filter) > -1)
          {
            isthere=true;
            break;
          }
        }
    }
    if(isthere==true)
    {
        tr[i].style.display = "";
    }
    else
    {
        tr[i].style.display = "none";
    }
  }
}

// Code goes here

$(document).ready(function(){

    $(".grid thead td").click(function(){
      showFilterOption(this);
    });

});

