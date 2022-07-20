const toggles = document.querySelectorAll('.click');
toggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
        toggle.parentNode.classList.toggle('active');
        e.preventDefault();
    })
});

var a = document.getElementById('selected_lang');
a.addEventListener('change', function() {
    // alert(this.value);
    if (this.value == "java") {
        alert("Class name should be -> " + a[a.selectedIndex].id.split('@')[0])
    }
}, false);

function validate() {
    var selectedValue = selectLang.options[ddl.selectedIndex].value;
    if (selectedValue == "java") {
        alert("Class Name Should be");
    }
}