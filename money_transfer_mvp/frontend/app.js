const API = "http://127.0.0.1:8000";
let token = "";
let currentUser = null;
let countries = [];
let recipients = [];
let quoteData = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadCountries();
});

// ============ AUTH ============

function showTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

    if (tab === 'login') {
        document.querySelectorAll('.tab')[0].classList.add('active');
        document.getElementById('loginForm').classList.add('active');
    } else {
        document.querySelectorAll('.tab')[1].classList.add('active');
        document.getElementById('registerForm').classList.add('active');
    }
}

async function register() {
    const data = {
        email: document.getElementById('regEmail').value,
        name: document.getElementById('regName').value,
        password: document.getElementById('regPassword').value,
        phone: document.getElementById('regPhone').value,
        address: document.getElementById('regAddress').value,
        city: document.getElementById('regCity').value,
        state: document.getElementById('regState').value,
        zip_code: document.getElementById('regZip').value,
        date_of_birth: document.getElementById('regDOB').value
    };

    try {
        const response = await fetch(`${API}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showNotification('Account created! Please login.', 'success');
            showTab('login');
        } else {
            showNotification(result.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

async function login() {
    const data = {
        email: document.getElementById('loginEmail').value,
        password: document.getElementById('loginPassword').value
    };

    try {
        const response = await fetch(`${API}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            token = result.token;
            currentUser = result.user;
            showApp();
            showNotification(`Welcome back, ${result.user.name}!`, 'success');
        } else {
            showNotification(result.detail || 'Login failed', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

function logout() {
    if (token) {
        fetch(`${API}/auth/logout`, {
            method: 'POST',
            headers: { 'Authorization': token }
        });
    }

    token = "";
    currentUser = null;
    document.getElementById('authSection').style.display = 'block';
    document.getElementById('appSection').style.display = 'none';
    showNotification('Logged out', 'success');
}

async function showApp() {
    document.getElementById('authSection').style.display = 'none';
    document.getElementById('appSection').style.display = 'block';

    // Load user profile
    await loadUserProfile();
    await loadRecipients();
    await loadTransferHistory();
    await loadImpactData();
    await loadKYCStatus();

    // Update UI
    document.getElementById('userName').textContent = currentUser.name;
    updateKYCBadge();

    // Show KYC notice if not verified
    if (currentUser.kyc_tier === 0) {
        document.getElementById('kycNotice').style.display = 'block';
        document.getElementById('transferForm').style.display = 'none';
    }
}

async function loadUserProfile() {
    const response = await fetch(`${API}/auth/me`, {
        headers: { 'Authorization': token }
    });

    if (response.ok) {
        currentUser = await response.json();
    }
}

function updateKYCBadge() {
    const badge = document.getElementById('kycBadge');
    const status = currentUser.kyc_status;

    if (status === 'VERIFIED') {
        badge.textContent = `✓ Verified (Tier ${currentUser.kyc_tier})`;
        badge.className = 'badge verified';
    } else if (status === 'PENDING') {
        badge.textContent = '⏳ KYC Pending';
        badge.className = 'badge pending';
    } else {
        badge.textContent = '⚠ Not Verified';
        badge.className = 'badge unverified';
    }
}

// ============ NAVIGATION ============

function showSection(section) {
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));

    event.target.classList.add('active');
    document.getElementById(section + 'Section').classList.add('active');

    // Reload data for specific sections
    if (section === 'impact') loadImpactData();
    if (section === 'history') loadTransferHistory();
    if (section === 'kyc') loadKYCStatus();
}

// ============ COUNTRIES & PROVIDERS ============

async function loadCountries() {
    const response = await fetch(`${API}/countries`);
    if (response.ok) {
        countries = await response.json();
        const select = document.getElementById('recipientCountry');
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country.code;
            option.textContent = `${country.flag} ${country.name}`;
            select.appendChild(option);
        });
    }
}

function loadProviders() {
    const countryCode = document.getElementById('recipientCountry').value;
    const country = countries.find(c => c.code === countryCode);
    const select = document.getElementById('recipientProvider');

    select.innerHTML = '<option value="">Select Mobile Money Provider...</option>';

    if (country) {
        country.providers.forEach(provider => {
            const option = document.createElement('option');
            option.value = provider;
            option.textContent = provider;
            select.appendChild(option);
        });
    }
}

// ============ RECIPIENTS ============

async function loadRecipients() {
    const response = await fetch(`${API}/recipients`, {
        headers: { 'Authorization': token }
    });

    if (response.ok) {
        recipients = await response.json();
        displayRecipients();
        updateRecipientSelect();
    }
}

function displayRecipients() {
    const list = document.getElementById('recipientsList');
    list.innerHTML = '';

    if (recipients.length === 0) {
        list.innerHTML = '<p class="empty-state">No recipients yet. Add your first recipient above.</p>';
        return;
    }

    recipients.forEach(recipient => {
        const country = countries.find(c => c.code === recipient.country);
        const card = document.createElement('div');
        card.className = 'recipient-card';
        card.innerHTML = `
            <div>
                <strong>${recipient.name}</strong>
                <p>${country ? country.flag : ''} ${recipient.country} - ${recipient.provider}</p>
                <p>${recipient.number}</p>
            </div>
            <button onclick="deleteRecipient(${recipient.id})" class="btn-danger">Delete</button>
        `;
        list.appendChild(card);
    });
}

function updateRecipientSelect() {
    const select = document.getElementById('transferRecipient');
    select.innerHTML = '<option value="">Choose recipient...</option>';

    recipients.forEach(recipient => {
        const country = countries.find(c => c.code === recipient.country);
        const option = document.createElement('option');
        option.value = recipient.id;
        option.dataset.country = recipient.country;
        option.textContent = `${recipient.name} (${country ? country.flag : ''} ${recipient.country})`;
        select.appendChild(option);
    });
}

async function addRecipient() {
    const data = {
        name: document.getElementById('recipientName').value,
        phone: document.getElementById('recipientPhone').value,
        country: document.getElementById('recipientCountry').value,
        mobile_money_provider: document.getElementById('recipientProvider').value,
        mobile_money_number: document.getElementById('recipientMMNumber').value
    };

    if (!data.name || !data.phone || !data.country || !data.mobile_money_provider || !data.mobile_money_number) {
        showNotification('Please fill all fields', 'error');
        return;
    }

    const response = await fetch(`${API}/recipients`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        showNotification('Recipient added!', 'success');
        document.getElementById('recipientName').value = '';
        document.getElementById('recipientPhone').value = '';
        document.getElementById('recipientMMNumber').value = '';
        await loadRecipients();
    } else {
        const error = await response.json();
        showNotification(error.detail || 'Failed to add recipient', 'error');
    }
}

async function deleteRecipient(id) {
    if (!confirm('Delete this recipient?')) return;

    const response = await fetch(`${API}/recipients/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': token }
    });

    if (response.ok) {
        showNotification('Recipient deleted', 'success');
        await loadRecipients();
    }
}

// ============ TRANSFERS ============

async function updateQuote() {
    const recipientSelect = document.getElementById('transferRecipient');
    const amount = parseFloat(document.getElementById('sendAmount').value);

    if (!recipientSelect.value || !amount || amount <= 0) {
        document.getElementById('quoteBox').style.display = 'none';
        return;
    }

    const recipientId = parseInt(recipientSelect.value);
    const recipient = recipients.find(r => r.id === recipientId);

    if (!recipient) return;

    // Get currency for country
    const currencyMap = {
        'LR': 'LRD', 'GH': 'GHS', 'NG': 'NGN',
        'SN': 'XOF', 'SL': 'SLL', 'CI': 'XOF'
    };
    const currency = currencyMap[recipient.country] || 'XOF';

    const response = await fetch(`${API}/quote?amount=${amount}&to_currency=${currency}`);

    if (response.ok) {
        quoteData = await response.json();
        quoteData.currency = currency;

        document.getElementById('quoteRate').textContent = `1 USD = ${quoteData.exchange_rate} ${currency}`;
        document.getElementById('quoteFee').textContent = `$${quoteData.fee_amount}`;
        document.getElementById('quoteReceive').textContent = `${quoteData.receive_amount.toFixed(2)} ${currency}`;
        document.getElementById('quoteEducation').textContent = `$${quoteData.education_contribution}`;
        document.getElementById('quoteTotal').textContent = `$${quoteData.total_cost}`;

        document.getElementById('quoteBox').style.display = 'block';
    }
}

async function sendMoney() {
    const recipientId = parseInt(document.getElementById('transferRecipient').value);
    const amount = parseFloat(document.getElementById('sendAmount').value);

    if (!recipientId || !amount) {
        showNotification('Please select recipient and amount', 'error');
        return;
    }

    if (!quoteData) {
        showNotification('Please wait for quote to load', 'error');
        return;
    }

    const data = {
        recipient_id: recipientId,
        send_amount: amount,
        receive_currency: quoteData.currency
    };

    try {
        const response = await fetch(`${API}/transfers`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            showNotification(
                `Transfer successful! ${result.message}`,
                'success'
            );
            document.getElementById('sendAmount').value = '';
            document.getElementById('quoteBox').style.display = 'none';
            await loadTransferHistory();
            await loadImpactData();
        } else {
            showNotification(result.detail || 'Transfer failed', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

async function loadTransferHistory() {
    const response = await fetch(`${API}/transfers`, {
        headers: { 'Authorization': token }
    });

    if (response.ok) {
        const transfers = await response.json();
        const container = document.getElementById('transferHistory');

        if (transfers.length === 0) {
            container.innerHTML = '<p class="empty-state">No transfers yet</p>';
            return;
        }

        container.innerHTML = '';
        transfers.forEach(transfer => {
            const card = document.createElement('div');
            card.className = 'transfer-card';

            const date = new Date(transfer.created_at).toLocaleDateString();
            const statusClass = transfer.status.toLowerCase();

            card.innerHTML = `
                <div class="transfer-header">
                    <strong>${transfer.recipient}</strong>
                    <span class="status ${statusClass}">${transfer.status}</span>
                </div>
                <div class="transfer-details">
                    <p>Sent: $${transfer.send_amount.toFixed(2)}</p>
                    <p>Received: ${transfer.receive_amount.toFixed(2)} ${transfer.currency}</p>
                    <p>Fee: $${transfer.fee.toFixed(2)}</p>
                    <p class="education-highlight">Education: $${transfer.education_contribution.toFixed(2)}</p>
                    <p class="transfer-date">${date}</p>
                </div>
            `;
            container.appendChild(card);
        });
    }
}

// ============ IMPACT & ANALYTICS ============

async function loadImpactData() {
    const response = await fetch(`${API}/analytics/impact`, {
        headers: { 'Authorization': token }
    });

    if (response.ok) {
        const data = await response.json();

        // Update stats
        document.getElementById('impactTransfers').textContent = data.your_impact.transfers;
        document.getElementById('impactSent').textContent = `$${data.your_impact.total_sent.toFixed(2)}`;
        document.getElementById('impactEducation').textContent = `$${data.your_impact.education_contribution.toFixed(2)}`;

        document.getElementById('platformEducation').textContent = `$${data.platform_impact.total_education_fund.toFixed(2)}`;
        document.getElementById('platformTransfers').textContent = data.platform_impact.total_transfers;

        // Load heat map
        await loadHeatMap();

        // Show education partners
        displayEducationPartners(data.your_impact.by_country);
    }
}

async function loadHeatMap() {
    const response = await fetch(`${API}/analytics/heatmap`, {
        headers: { 'Authorization': token }
    });

    if (response.ok) {
        const data = await response.json();
        const container = document.getElementById('heatMap');

        if (data.length === 0) {
            container.innerHTML = '<p class="empty-state">Start sending money to see your impact map</p>';
            return;
        }

        container.innerHTML = '';
        data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'heat-map-card';

            // Calculate intensity for visual effect
            const intensity = Math.min(item.total_sent_usd / 1000, 1);
            const bgColor = `rgba(46, 204, 113, ${0.2 + intensity * 0.8})`;

            card.style.backgroundColor = bgColor;
            card.innerHTML = `
                <div class="heat-map-header">
                    <span class="flag">${item.flag}</span>
                    <strong>${item.country_name}</strong>
                </div>
                <div class="heat-map-stats">
                    <p>Transfers: ${item.transfer_count}</p>
                    <p>Total Sent: $${item.total_sent_usd.toFixed(2)}</p>
                    <p class="education-highlight">Education: $${item.education_contribution_usd.toFixed(2)}</p>
                </div>
            `;
            container.appendChild(card);
        });
    }
}

function displayEducationPartners(byCountry) {
    const container = document.getElementById('educationPartners');
    container.innerHTML = '';

    if (byCountry.length === 0) {
        container.innerHTML = '<p class="empty-state">Your contributions will appear here</p>';
        return;
    }

    byCountry.forEach(item => {
        const country = countries.find(c => c.code === item.country);
        const card = document.createElement('div');
        card.className = 'partner-card';
        card.innerHTML = `
            <h4>${country ? country.flag : ''} ${country ? country.name : item.country}</h4>
            <p><strong>${item.partner || 'Local Education Initiative'}</strong></p>
            <p class="education-amount">Your contribution: $${item.amount.toFixed(2)}</p>
        `;
        container.appendChild(card);
    });
}

// ============ KYC ============

async function loadKYCStatus() {
    const response = await fetch(`${API}/kyc/status`, {
        headers: { 'Authorization': token }
    });

    if (response.ok) {
        const data = await response.json();

        document.getElementById('kycStatus').textContent = data.status;
        document.getElementById('kycTier').textContent = data.tier;

        // Show limits
        if (currentUser && currentUser.limits) {
            const limitsDiv = document.getElementById('kycLimits');
            limitsDiv.innerHTML = `
                <p>Daily Limit: $${currentUser.limits.daily}</p>
                <p>Monthly Limit: $${currentUser.limits.monthly}</p>
                <p>Per Transaction: $${currentUser.limits.per_transaction}</p>
            `;
        }

        // Show documents
        const docsContainer = document.getElementById('kycDocuments');
        docsContainer.innerHTML = '<h3>Uploaded Documents</h3>';

        if (data.documents.length === 0) {
            docsContainer.innerHTML += '<p class="empty-state">No documents uploaded yet</p>';
            return;
        }

        data.documents.forEach(doc => {
            const card = document.createElement('div');
            card.className = 'kyc-doc-card';

            const statusClass = doc.status.toLowerCase();
            const statusEmoji = doc.status === 'APPROVED' ? '✓' : doc.status === 'REJECTED' ? '✗' : '⏳';

            card.innerHTML = `
                <div>
                    <strong>${doc.type}</strong>
                    <span class="status ${statusClass}">${statusEmoji} ${doc.status}</span>
                </div>
                <p>Uploaded: ${new Date(doc.uploaded_at).toLocaleDateString()}</p>
                ${doc.rejection_reason ? `<p class="error">Reason: ${doc.rejection_reason}</p>` : ''}
            `;
            docsContainer.appendChild(card);
        });
    }
}

async function uploadKYC() {
    const docType = document.getElementById('documentType').value;
    const docNumber = document.getElementById('documentNumber').value;
    const fileInput = document.getElementById('documentFile');

    if (!docType || !docNumber || !fileInput.files[0]) {
        showNotification('Please fill all fields and select a file', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('document_type', docType);
    formData.append('document_number', docNumber);
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch(`${API}/kyc/upload`, {
            method: 'POST',
            headers: { 'Authorization': token },
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showNotification('Document uploaded! Review in progress.', 'success');
            document.getElementById('documentType').value = '';
            document.getElementById('documentNumber').value = '';
            fileInput.value = '';
            await loadKYCStatus();
            await loadUserProfile();
            updateKYCBadge();
        } else {
            showNotification(result.detail || 'Upload failed', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

// ============ UTILITIES ============

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 4000);
}
