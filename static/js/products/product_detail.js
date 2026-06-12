function changeImage(url, thumb) {
    const img = document.getElementById('mainImg');
    if (img) img.src = url;
    document.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
    if (thumb) thumb.classList.add('active');
}

function changeQty(delta) {
    const input = document.getElementById('qty');
    if (!input) return;
    const max = parseInt(input.max) || 99;
    let val = parseInt(input.value) + delta;
    input.value = Math.max(1, Math.min(max, val));
}

function addToCart(productId) {
    const btn = document.getElementById('addCartBtn');
    btn.disabled = true;
    btn.textContent = 'Adding...';

    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(r => {
        if (r.status === 401 || r.redirected) {
            window.location.href = '/accounts/login/?next=' + window.location.pathname;
            return null;
        }
        return r.json();
    })
    .then(data => {
        if (!data) return;
        if (data.success) {
            btn.innerHTML = '✓ Added to Cart!';
            btn.style.background = '#06943D';
            showToast(data.message);
            setTimeout(() => {
                btn.innerHTML = '🛒 Add to Cart';
                btn.style.background = '';
                btn.disabled = false;
            }, 1500);
        } else {
            showToast(data.message || 'Kuch error aa gaya');
            btn.innerHTML = '🛒 Add to Cart';
            btn.disabled = false;
        }
    })
    .catch(() => {
        showToast('Pehle login karo');
        btn.innerHTML = '🛒 Add to Cart';
        btn.disabled = false;
        setTimeout(() => {
            window.location.href = '/accounts/login/?next=' + window.location.pathname;
        }, 1000);
    });
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2800);
}
