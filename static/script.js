// ===============================
// DARK / LIGHT MODE
// ===============================

const themeToggle = document.getElementById("themeToggle");

const savedTheme = localStorage.getItem("theme");

if (savedTheme === "light") {
    document.body.classList.add("light");
    themeToggle.textContent = "☀️";
}

themeToggle.addEventListener("click", () => {

    document.body.classList.toggle("light");

    const isLight = document.body.classList.contains("light");

    themeToggle.textContent = isLight ? "☀️" : "🌙";

    localStorage.setItem(
        "theme",
        isLight ? "light" : "dark"
    );
});


// ===============================
// MOBILE MENU
// ===============================

const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

menuToggle.addEventListener("click", () => {

    navLinks.classList.toggle("open");

    menuToggle.textContent =
        navLinks.classList.contains("open")
            ? "✕"
            : "☰";
});


// Close menu after clicking a link

document.querySelectorAll(".nav-links a").forEach(link => {

    link.addEventListener("click", () => {

        navLinks.classList.remove("open");

        menuToggle.textContent = "☰";

    });

});


// ===============================
// SCROLL ANIMATIONS
// ===============================

const revealElements =
    document.querySelectorAll(".reveal");

const observer = new IntersectionObserver(
    (entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("active");

                observer.unobserve(entry.target);
            }

        });

    },
    {
        threshold: 0.15
    }
);

revealElements.forEach(element => {
    observer.observe(element);
});


// ===============================
// SKILL BAR ANIMATION
// ===============================

const skillBars =
    document.querySelectorAll(".progress-bar");

const skillObserver = new IntersectionObserver(
    (entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                const bar = entry.target;

                const width =
                    bar.getAttribute("data-width");

                bar.style.width = width + "%";

                skillObserver.unobserve(bar);
            }

        });

    },
    {
        threshold: 0.5
    }
);

skillBars.forEach(bar => {
    skillObserver.observe(bar);
});