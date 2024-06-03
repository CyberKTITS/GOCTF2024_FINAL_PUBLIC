document.addEventListener('DOMContentLoaded', function() {
    const blogDropdown = document.getElementById('blog-dropdown');

    blogDropdown.addEventListener('mouseover', function() {
        const dropdownMenu = blogDropdown.querySelector('.dropdown-menu');
        dropdownMenu.style.display = 'block';
    });

    blogDropdown.addEventListener('mouseleave', function() {
        const dropdownMenu = blogDropdown.querySelector('.dropdown-menu');
        dropdownMenu.style.display = 'none';
    });
});

