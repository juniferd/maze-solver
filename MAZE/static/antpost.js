

var newTurn = document.getElementById("newTurn");

if (newTurn){
    setTimeout(function(){
        newTurn.style.opacity = 1;
    },1000)
    newTurn.addEventListener("keypress", function(event) {


        var key = event.which || event.keyCode;
        if (key === 13) { // 13 is enter
            var selectedValue = document.getElementById('newTurn').value

            if (selectedValue <= maxCounterNum) {
                counter = selectedValue
                
                setTimeout(function(){
                    document.getElementById('newTurn').value = '';
                    document.activeElement.blur();
                },1000)
            } else {
                console.log('turn does not exist yet')
            }
        }
        
        
    });


}
