// modal toggle
const openModalBtns = [...document.getElementsByClassName('open-modal')];
const closeModalBtns = [...document.getElementsByClassName('close-modal')];
const modal = document.querySelector('.modal');

closeModalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    document.body.classList.remove("active-modal");
}))

openModalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    document.body.classList.add("active-modal")
}))
