//  SHOW NAVBAR 
const showMenu = (headerToggle, menubarId) =>{
    const toggleBtn = document.getElementById(headerToggle),
    menubar = document.getElementById(menubarId)
    
    // Validate that variables exist
    if(toggleBtn && menubar){
        toggleBtn.addEventListener('click', ()=>{
            // We add the show-menu class to the div tag with the nav__menu class
            toggleBtn.classList.toggle('active')
            // change icon
            menubar.classList.toggle('activeMenubar')
        })
    }
}
showMenu('menuBtn','activeMenubar')