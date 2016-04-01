

var element = document.querySelector("form#ff");
element.addEventListener("submit", function(event) {
    event.preventDefault();

    var selectedValue = document.getElementById('newTurn').value

    if (selectedValue <= maxCounterNum) {
        counter = selectedValue
    } else {
        console.log('turn does not exist yet')
    }
    
});

