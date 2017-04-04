
  var timesClicked = 0;

   function btnClick(no_of_cart_items){
      timesClicked = no_of_cart_items + 1;
       
      document.getElementById('timesClicked').innerHTML = timesClicked;
      return true 
  }
