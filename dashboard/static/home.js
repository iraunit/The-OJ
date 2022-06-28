const toggles = document.querySelectorAll('.home-link')
toggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
        toggle.parentNode.classList.toggle('active');
        e.preventDefault();
    })
})