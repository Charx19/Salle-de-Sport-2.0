document.addEventListener("DOMContentLoaded", function () {
    // 🍔 Menu Burger
    const burger = document.getElementById("hamburgerBtn");
    const menu = document.getElementById("mobileMenu");
    const close = document.getElementById("closeMenu");
    const overlay = document.getElementById("menuOverlay");

    function closeMenu() {
        menu.classList.remove("active");
    }

    burger?.addEventListener("click", () => {
        menu.classList.add("active");
    });

    close?.addEventListener("click", closeMenu);
    overlay?.addEventListener("click", closeMenu);

    // ✅ Menu déroulant mobile (Nos services)
    const trigger = document.getElementById("servicesToggle");
    const dropdown = document.getElementById("dropdownServices");

    trigger?.addEventListener("click", function (e) {
        e.preventDefault();
        if (dropdown.style.display === "flex") {
            dropdown.style.display = "none";
        } else {
            dropdown.style.display = "flex";
        }
    });

    // Fermer si on clique ailleurs
    document.addEventListener("click", function (e) {
        if (!trigger.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = "none";
        }
    });

    // ❓ FAQ Toggle
    const faqQuestions = document.querySelectorAll(".faq-question");

    faqQuestions.forEach((question) => {
        question.addEventListener("click", () => {
            const answer = question.nextElementSibling;

            const isOpen = question.classList.contains("active");

            // Toggle active class
            question.classList.toggle("active", !isOpen);

            // Trigger animation
            if (!isOpen) {
                answer.style.maxHeight = answer.scrollHeight + "px";
            } else {
                answer.style.maxHeight = null;
            }
        });
    });

});
