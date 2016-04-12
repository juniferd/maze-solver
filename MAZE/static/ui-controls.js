var statsControl = document.getElementById('stats-control')

statsControl.addEventListener('click', function(e){
    controlClass = statsControl.className
    statsPanel = document.getElementById('stats-panel')

    if (controlClass == 'expand') {
        statsPanel.className = 'expanded'
        statsControl.className = 'collapse'
        document.getElementById('content').className = 'sidebar-expanded'
    } else if (controlClass == 'collapse') {
        statsPanel.className = 'collapsed'
        statsControl.className = 'expand'
        document.getElementById('content').className = 'sidebar-collapsed'
    }
})