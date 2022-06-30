const toggles = document.querySelectorAll('.click')
toggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
        toggle.parentNode.classList.toggle('active');
        e.preventDefault();
    })
})