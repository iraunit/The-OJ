const toggles = document.querySelectorAll('#show_code')
toggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
        toggle.parentNode.parentNode.classList.toggle('active');
        e.preventDefault();
    })
})

console.log("check")