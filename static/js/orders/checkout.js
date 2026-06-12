// Payment option highlight on select
document.querySelectorAll('.payment-option').forEach(option => {
    const radio = option.querySelector('input[type="radio"]');
    if (radio.checked) option.classList.add('selected');
    option.addEventListener('click', () => {
        document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected'));
        option.classList.add('selected');
        radio.checked = true;
    });
});

// Place order button loading state
const form = document.getElementById('checkoutForm');
const placeBtn = document.getElementById('placeBtn');
if (form && placeBtn) {
    form.addEventListener('submit', () => {
        placeBtn.textContent = 'Placing Order...';
        placeBtn.disabled = true;
    });
}
