const API = "http://127.0.0.1:8000";
let adminToken = "";
let currentAdmin = null;
let currentKYCUser = null;

// ============ ADMIN AUTH ============

async function adminLogin() {
    const data = {
        email: document.getElementById('adminEmail').value,
        password: document.getElementById('adminPassword').value
    };

    try {
        const response = await fetch(`${API}/admin/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            adminToken = result.token;
            currentAdmin = result.admin;
            showDashboard();
            showNotification(`Welcome, ${result.admin.name}!`, 'success');
        } else {
            showNotification(result.detail || 'Login failed', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    }
}

function adminLogout() {
    adminToken = "";
    currentAdmin = null;
    document.getElementById('adminLogin').style.display = 'block';
    document.getElementById('adminDashboard').style.display = 'none';
    showNotification('Logged out', 'success');
}

async function showDashboard() {
    document.getElementById('adminLogin').style.display = 'none';
    document.getElementById('adminDashboard').style.display = 'block';

    document.getElementById('adminName').textContent = currentAdmin.name;

    await loadDashboardStats();
    await loadKYCQueue();
    await loadEducationFund();
}

// ============ NAVIGATION ============

function showAdminSection(section) {
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));

    event.target.classList.add('active');
    document.getElementById(section + 'Section').classList.add('active');

    // Reload data
    if (section === 'kyc') loadKYCQueue();
    if (section === 'education') loadEducationFund();
}

// ============ DASHBOARD STATS ============

async function loadDashboardStats() {
    const response = await fetch(`${API}/admin/dashboard`, {
        headers: { 'Authorization': adminToken }
    });

    if (response.ok) {
        const data = await response.json();

        document.getElementById('totalUsers').textContent = data.total_users;
        document.getElementById('pendingKYC').textContent = data.pending_kyc;
        document.getElementById('totalTransfers').textContent = data.total_transfers;
        document.getElementById('totalVolume').textContent = `$${data.total_volume.toFixed(2)}`;
        document.getElementById('totalFees').textContent = `$${data.total_fees.toFixed(2)}`;
        document.getElementById('totalEducation').textContent = `$${data.total_education_fund.toFixed(2)}`;

        // Recent transfers
        displayRecentTransfers(data.recent_transfers);
    }
}

function displayRecentTransfers(transfers) {
    const container = document.getElementById('recentTransfers');

    if (transfers.length === 0) {
        container.innerHTML = '<p class="empty-state">No recent transfers</p>';
        return;
    }

    let html = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>User</th>
                    <th>Amount</th>
                    <th>Currency</th>
                    <th>Status</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
    `;

    transfers.forEach(t => {
        const date = new Date(t.created_at).toLocaleString();
        html += `
            <tr>
                <td>#${t.id}</td>
                <td>${t.name}</td>
                <td>$${t.send_amount.toFixed(2)}</td>
                <td>${t.receive_currency}</td>
                <td><span class="status ${t.status.toLowerCase()}">${t.status}</span></td>
                <td>${date}</td>
            </tr>
        `;
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

// ============ KYC REVIEW ============

async function loadKYCQueue() {
    const response = await fetch(`${API}/admin/kyc/pending`, {
        headers: { 'Authorization': adminToken }
    });

    if (response.ok) {
        const pending = await response.json();
        displayKYCQueue(pending);
    }
}

function displayKYCQueue(queue) {
    const container = document.getElementById('kycQueue');

    if (queue.length === 0) {
        container.innerHTML = '<p class="empty-state">No pending KYC reviews</p>';
        return;
    }

    container.innerHTML = '';
    queue.forEach(item => {
        const card = document.createElement('div');
        card.className = 'kyc-card';

        const date = new Date(item.submitted_at).toLocaleString();

        card.innerHTML = `
            <div class="kyc-card-header">
                <div>
                    <strong>${item.name}</strong>
                    <p>${item.email}</p>
                </div>
                <button onclick="reviewKYC(${item.user_id})" class="btn-primary">Review</button>
            </div>
            <div class="kyc-card-info">
                <p>Documents: ${item.documents_count}</p>
                <p>Submitted: ${date}</p>
            </div>
        `;

        container.appendChild(card);
    });
}

async function reviewKYC(userId) {
    currentKYCUser = userId;

    const response = await fetch(`${API}/admin/kyc/${userId}/documents`, {
        headers: { 'Authorization': adminToken }
    });

    if (response.ok) {
        const documents = await response.json();
        displayKYCDocuments(documents);
        document.getElementById('kycModal').style.display = 'block';
    }
}

function displayKYCDocuments(documents) {
    const container = document.getElementById('kycDetails');
    container.innerHTML = '';

    documents.forEach(doc => {
        const card = document.createElement('div');
        card.className = 'kyc-doc-review';

        const uploadDate = new Date(doc.uploaded_at).toLocaleString();
        const statusClass = doc.status.toLowerCase();

        card.innerHTML = `
            <div class="doc-header">
                <h3>${doc.type}</h3>
                <span class="status ${statusClass}">${doc.status}</span>
            </div>
            <p>Document Number: ${doc.number || 'N/A'}</p>
            <p>Uploaded: ${uploadDate}</p>
            <p>File: ${doc.file_path}</p>

            ${doc.status === 'PENDING' ? `
                <div class="review-actions">
                    <button onclick="approveDocument(${doc.id})" class="btn-success">✓ Approve</button>
                    <button onclick="rejectDocument(${doc.id})" class="btn-danger">✗ Reject</button>
                </div>
            ` : ''}
        `;

        container.appendChild(card);
    });
}

async function approveDocument(docId) {
    const data = {
        document_id: docId,
        status: 'APPROVED'
    };

    const response = await fetch(`${API}/admin/kyc/review`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': adminToken
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        showNotification('Document approved', 'success');
        await reviewKYC(currentKYCUser);
        await loadKYCQueue();
        await loadDashboardStats();
    }
}

async function rejectDocument(docId) {
    const reason = prompt('Rejection reason:');
    if (!reason) return;

    const data = {
        document_id: docId,
        status: 'REJECTED',
        rejection_reason: reason
    };

    const response = await fetch(`${API}/admin/kyc/review`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': adminToken
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        showNotification('Document rejected', 'success');
        await reviewKYC(currentKYCUser);
        await loadKYCQueue();
    }
}

function closeKYCModal() {
    document.getElementById('kycModal').style.display = 'none';
    currentKYCUser = null;
}

// ============ EDUCATION FUND ============

async function loadEducationFund() {
    const response = await fetch(`${API}/admin/education-fund`, {
        headers: { 'Authorization': adminToken }
    });

    if (response.ok) {
        const stats = await response.json();
        displayEducationFund(stats);
    }
}

function displayEducationFund(stats) {
    const container = document.getElementById('educationFund');

    if (stats.length === 0) {
        container.innerHTML = '<p class="empty-state">No education fund contributions yet</p>';
        return;
    }

    container.innerHTML = '';
    stats.forEach(item => {
        const card = document.createElement('div');
        card.className = 'education-card';

        card.innerHTML = `
            <h3>${item.country_name || item.country}</h3>
            <div class="education-stats">
                <div class="stat-row">
                    <span>Contributions:</span>
                    <strong>${item.contributions}</strong>
                </div>
                <div class="stat-row">
                    <span>Total Fund:</span>
                    <strong>$${item.total_usd.toFixed(2)}</strong>
                </div>
                <div class="stat-row">
                    <span>Disbursed:</span>
                    <strong>$${item.disbursed_usd.toFixed(2)}</strong>
                </div>
                <div class="stat-row highlight">
                    <span>Pending:</span>
                    <strong>$${item.pending_usd.toFixed(2)}</strong>
                </div>
            </div>
            <p class="partner"><strong>Partner:</strong> ${item.partner || 'N/A'}</p>
        `;

        container.appendChild(card);
    });
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

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('kycModal');
    if (event.target == modal) {
        closeKYCModal();
    }
}
