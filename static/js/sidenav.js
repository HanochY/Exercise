function openMySidenav(){
    document.querySelector(':root').style.setProperty('--sidenav-width', '250px');
}
function closeMySidenav(){
    document.querySelector(':root').style.setProperty('--sidenav-width', '0px');
    return false;
}