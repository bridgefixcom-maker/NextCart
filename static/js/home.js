/* ============================================
   NEXTCART — HOME PAGE JS
   ============================================ */

// === NAVBAR SCROLL ===
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
});

// === HAMBURGER MENU ===
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

hamburger.addEventListener('click', () => {
    const isOpen = mobileMenu.classList.toggle('open');
    const spans = hamburger.querySelectorAll('span');
    spans[0].style.transform = isOpen ? 'rotate(45deg) translate(5px, 5px)' : '';
    spans[1].style.opacity  = isOpen ? '0' : '';
    spans[2].style.transform = isOpen ? 'rotate(-45deg) translate(5px, -5px)' : '';
});

document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !mobileMenu.contains(e.target)) {
        mobileMenu.classList.remove('open');
        hamburger.querySelectorAll('span').forEach(s => {
            s.style.transform = '';
            s.style.opacity = '';
        });
    }
});

// === REVIEWS SLIDER ===
let curReview = 0;
const track = document.getElementById('reviewsTrack');
const reviewCards = track ? track.querySelectorAll('.review-card') : [];
const dots = document.querySelectorAll('.dot');

function goToReview(idx) {
    if (!track || !reviewCards.length) return;
    curReview = idx;

    const w = window.innerWidth;
    const visible = w <= 768 ? 1 : w <= 1024 ? 2 : 3;
    const max = Math.max(0, reviewCards.length - visible);
    const safeIdx = Math.min(idx, max);

    const gap = 18;
    const cardW = reviewCards[0].offsetWidth + gap;
    track.style.transform = `translateX(-${safeIdx * cardW}px)`;

    dots.forEach((d, i) => d.classList.toggle('active', i === idx));
}

const reviewInterval = setInterval(() => {
    curReview = (curReview + 1) % reviewCards.length;
    goToReview(curReview);
}, 4500);

window.addEventListener('resize', () => goToReview(curReview));

// === ADD TO CART ===
let cartCount = 0;

function addToCart(event, productId) {
    event.preventDefault();
    event.stopPropagation();

    cartCount++;
    const counter = document.getElementById('cartCount');
    if (counter) counter.textContent = cartCount;

    const btn = event.currentTarget;
    btn.style.transform = 'scale(1.35)';
    btn.style.background = '#06943D';
    setTimeout(() => {
        btn.style.transform = '';
        btn.style.background = '';
    }, 220);

    // TODO: AJAX call when cart app is ready
    // fetch(`/cart/add/${productId}/`, {
    //     method: 'POST',
    //     headers: {
    //         'X-CSRFToken': document.cookie.match(/csrftoken=([^;]+)/)?.[1] || ''
    //     }
    // }).then(r => r.json()).then(data => {
    //     counter.textContent = data.cart_count;
    // });
}

// === SMOOTH SCROLL ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
