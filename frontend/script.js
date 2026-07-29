const API_BASE = '';
let token = null;
let user_id = '';

// Show profile modal after login
async function manualLogin() {
    const input = document.getElementById('username-input');
    user_id = input.value.trim();
    if (!user_id) {
        alert('Please enter a username');
        return;
    }
    try {
        const resp = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id })
        });
        const data = await resp.json();
        token = data.token;
        document.querySelector('.user-badge span').textContent = user_id;
        document.getElementById('login-btn').disabled = true;
        document.getElementById('username-input').disabled = true;
        
        // Show profile modal instead of auto-setting profile
        showProfileModal();
    } catch (err) {
        alert('Login failed: ' + err.message);
    }
}

function showProfileModal() {
    document.getElementById('profile-modal').classList.add('active');
}

// Handle profile form submission
document.getElementById('profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const profile = {
        amount: parseFloat(document.getElementById('amount').value),
        purpose: document.getElementById('purpose').value,
        monthly_income: parseFloat(document.getElementById('monthly_income').value),
        existing_emi: parseFloat(document.getElementById('existing_emi').value) || 0,
        tenure: parseInt(document.getElementById('tenure').value),
        employment_type: document.getElementById('employment_type').value,
        risk_profile: document.getElementById('risk_profile').value,
        business_income: parseFloat(document.getElementById('business_income').value) || 0
    };
    
    try {
        await fetch('/api/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(profile)
        });
        
        // Hide modal
        document.getElementById('profile-modal').classList.remove('active');
        
        // Welcome message
        document.getElementById('messages').innerHTML = '';
        addMessage('bot', `👋 Hello ${user_id}! I'm your AI Loan Advisor.Ask me anything!`);
    } catch (err) {
        alert('Failed to save profile: ' + err.message);
    }
});

// Add chat message function
function addMessage(sender, text) {
    const container = document.getElementById('messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    if (sender === 'bot') {
        bubble.innerHTML = marked.parse(text);
    } else {
        bubble.textContent = text;
    }

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(bubble);
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
}

// Send message function
async function sendMessage() {
    const input = document.getElementById('user-input');
    const query = input.value.trim();
    if (!query) return;
    input.value = '';
    addMessage('user', query);

    try {
        const resp = await fetch('/api/advise', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({ query })
        });
        const data = await resp.json();
        if (data.detail) {
            addMessage('bot', 'Error: ' + data.detail);
        } else {
            let fullText = data.advice || '';
            if (data.recommendations && data.recommendations.length) {
                let recText = '\n\n📊 **Top Recommendations**\n';
                data.recommendations.forEach((r, i) => {
                    const p = r.product;
                    const d = r.details;
                    recText += `\n${i+1}. **${p.name}** – EMI ₹${d.emi}, Total Interest ₹${d.total_interest}, Total ₹${d.total_payment}`;
                });
                fullText += recText;
            }
            addMessage('bot', fullText);
        }
    } catch (err) {
        addMessage('bot', 'Error: ' + err.message);
    }
}

// Event listeners
document.getElementById('login-btn').addEventListener('click', manualLogin);
document.getElementById('username-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') manualLogin();
});
document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Auto-login as demo_user on load
window.addEventListener('load', () => {
    document.getElementById('username-input').value = 'demo_user';
    // Uncomment below to auto-login
    // manualLogin();
});