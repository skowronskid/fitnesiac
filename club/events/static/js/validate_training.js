// function enterText() {
//     // get the textarea element
//     var textarea = document.getElementById("textarea");
    
//     // get the display element
//     var display = document.getElementById("display");
    
//     // set the text in the display element to the text entered in the textarea
//     display.innerHTML = textarea.value;
//   }



  function validateForm() {
    var form = document.getElementById('myform');
    var name = form.elements.name;
    if (name.value.length < 3) {
      alert('Name must be at least 3 characters long.');
      event.preventDefault();
    }
  }
  
  var form = document.getElementById('myform');
  form.addEventListener('submit', validateForm);