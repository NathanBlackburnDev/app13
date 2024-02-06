// Highlight the current page the user is on
addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.nav-link').forEach(
        link => {
            // If the user is on the current page
            if (link.href === window.location.href) {
                link.setAttribute('aria-current', 'page');
                link.classList.add('active');
            }
        }
    )
})