function updateQty(itemId, currentQty, delta) {
    const newQty = currentQty + delta;
    if (newQty < 1) {
        removeItem(itemId);
        return;
    }

    fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': CSRF,
        },
        body: `quantity=${newQty}`
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`qty-${itemId}`).value = newQty;
            document.getElementById(`subtotal-${itemId}`).textContent = `₹${data.item_subtotal}`;
            document.getElementById('summarySubtotal').textContent = `₹${data.cart_total}`;
            document.getElementById('summaryTotal').textContent = `₹${data.cart_total}`;
            const btns = document.querySelectorAll(`#item-${itemId} .qty-btn`);
            btns[0].setAttribute('onclick', `updateQty(${itemId}, ${newQty}, -1)`);
            btns[1].setAttribute('onclick', `updateQty(${itemId}, ${newQty}, 1)`);
        }
    });
}

function removeItem(itemId) {
    fetch(`/cart/remove/${itemId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF },
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const el = document.getElementById(`item-${itemId}`);
            el.style.opacity = '0';
            el.style.transform = 'translateX(20px)';
            el.style.transition = '0.3s ease';
            setTimeout(() => {
                el.remove();
                document.getElementById('summarySubtotal').textContent = `₹${data.cart_total}`;
                document.getElementById('summaryTotal').textContent = `₹${data.cart_total}`;
                if (data.cart_count === 0) location.reload();
            }, 300);
        }
    });
}
