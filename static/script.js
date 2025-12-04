// API Configuration
const API_BASE = 'http://localhost:8000/api/v1';

// State
let accessToken = null;
let currentUser = null;
let cy = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Check if token exists in localStorage
    const token = localStorage.getItem('access_token');
    if (token) {
        accessToken = token;
        const user = localStorage.getItem('current_user');
        if (user) {
            currentUser = JSON.parse(user);
            showApp();
        }
    }

    // Setup event listeners
    setupAuthEvents();
    setupAppEvents();
});

// Auth Events
function setupAuthEvents() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tab = e.target.dataset.tab;
            switchTab(tab);
        });
    });

    // Forms
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    document.getElementById('verifyForm').addEventListener('submit', handleVerify);
}

function setupAppEvents() {
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
    document.getElementById('addMechanicBtn').addEventListener('click', addMechanic);
    document.getElementById('addLinkBtn').addEventListener('click', addLink);
    document.getElementById('viewTreeBtn').addEventListener('click', viewTree);
}

function switchTab(tab) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

    // Update forms
    document.querySelectorAll('.tab-content').forEach(form => {
        form.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tab}"].tab-content`).classList.add('active');
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const errorEl = document.getElementById('loginError');

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Login failed');
        }

        const data = await response.json();
        accessToken = data.access_token;
        currentUser = data.user;

        // Save to localStorage
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('current_user', JSON.stringify(currentUser));

        errorEl.textContent = '';
        showApp();
    } catch (error) {
        errorEl.textContent = error.message;
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const errorEl = document.getElementById('registerError');

    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Registration failed');
        }

        errorEl.textContent = '';
        alert(`Registration successful! Check your email for verification link.`);
        
        // Switch to verify tab
        switchTab('verify');
    } catch (error) {
        errorEl.textContent = error.message;
    }
}

async function handleVerify(e) {
    e.preventDefault();
    const token = document.getElementById('verifyToken').value;
    const errorEl = document.getElementById('verifyError');

    try {
        const response = await fetch(`${API_BASE}/auth/verify-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Verification failed');
        }

        errorEl.textContent = '';
        alert('Email verified! You can now login.');
        switchTab('login');
    } catch (error) {
        errorEl.textContent = error.message;
    }
}

function handleLogout() {
    accessToken = null;
    currentUser = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('current_user');
    showAuth();
    // Reset forms
    document.getElementById('loginForm').reset();
    document.getElementById('registerForm').reset();
}

function showAuth() {
    document.getElementById('authSection').style.display = 'flex';
    document.getElementById('appSection').style.display = 'none';
}

function showApp() {
    document.getElementById('authSection').style.display = 'none';
    document.getElementById('appSection').style.display = 'flex';
    
    // Update user info
    document.querySelector('#userInfo strong').textContent = currentUser.username;
    
    // Initialize Cytoscape
    initCytoscape();
    loadAllMechanics();
}

function getAuthHeaders() {
    return {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
    };
}

// Cytoscape initialization
function initCytoscape() {
    cy = cytoscape({
        container: document.getElementById('cy'),
        style: [
            {
                selector: 'node',
                style: {
                    'content': 'data(label)',
                    'background-color': '#667eea',
                    'color': '#fff',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': '80px',
                    'height': '80px',
                    'padding': '10px',
                    'font-size': '12px',
                    'border-width': '2px',
                    'border-color': '#764ba2'
                }
            },
            {
                selector: 'node:selected',
                style: {
                    'background-color': '#764ba2',
                    'border-width': '3px'
                }
            },
            {
                selector: 'edge',
                style: {
                    'target-arrow-shape': 'triangle',
                    'line-color': '#ddd',
                    'target-arrow-color': '#ddd',
                    'curve-style': 'bezier',
                    'width': '2px',
                    'label': 'data(type)',
                    'font-size': '11px',
                    'text-background-color': '#fff',
                    'text-background-padding': '3px',
                    'text-background-opacity': 0.9
                }
            }
        ],
        layout: {
            name: 'cose-bilkent',
            directed: true,
            animate: true
        }
    });

    // Handle node selection
    cy.on('tap', 'node', function(e) {
        const node = e.target;
        showNodeInfo(node.data());
    });

    // Handle drag
    cy.on('dragfree', 'node', function(e) {
        // Nodes are freely draggable
    });
}

function showNodeInfo(data) {
    const infoEl = document.getElementById('nodeInfo');
    infoEl.innerHTML = `
        <strong>ID:</strong> ${data.id}<br>
        <strong>Name:</strong> ${data.label}<br>
        ${data.description ? `<strong>Desc:</strong> ${data.description}<br>` : ''}
        ${data.year ? `<strong>Year:</strong> ${data.year}<br>` : ''}
    `;
}

// App functions
async function loadAllMechanics() {
    try {
        const response = await fetch(`${API_BASE}/mechanics/`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) throw new Error('Failed to load mechanics');

        const mechanics = await response.json();
        
        // Load links too
        const linksResponse = await fetch(`${API_BASE}/mechanics/links`, {
            headers: getAuthHeaders()
        });
        
        const links = linksResponse.ok ? await linksResponse.json() : [];

        // Display graph
        displayGraph(mechanics, links);
    } catch (error) {
        console.error('Error loading mechanics:', error);
    }
}

function displayGraph(mechanics, links) {
    const elements = [];

    // Add nodes
    mechanics.forEach(m => {
        elements.push({
            data: {
                id: `node-${m.id}`,
                label: m.name,
                description: m.description,
                year: m.year,
                mechanicId: m.id
            }
        });
    });

    // Add edges
    links.forEach(l => {
        elements.push({
            data: {
                id: `edge-${l.id}`,
                source: `node-${l.from_id}`,
                target: `node-${l.to_id}`,
                type: l.type
            }
        });
    });

    if (cy) {
        cy.elements().remove();
        cy.add(elements);
        cy.layout({ name: 'cose-bilkent', directed: true, animate: true }).run();
    }
}

async function addMechanic() {
    const name = document.getElementById('mechanicName').value.trim();
    const description = document.getElementById('mechanicDesc').value.trim();
    const year = parseInt(document.getElementById('mechanicYear').value) || null;

    if (!name) {
        alert('Please enter mechanic name');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/mechanics/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ name, description: description || null, year })
        });

        if (!response.ok) throw new Error('Failed to add mechanic');

        document.getElementById('mechanicName').value = '';
        document.getElementById('mechanicDesc').value = '';
        document.getElementById('mechanicYear').value = '';

        alert('Mechanic added!');
        loadAllMechanics();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function addLink() {
    const from_id = parseInt(document.getElementById('linkFrom').value);
    const to_id = parseInt(document.getElementById('linkTo').value);
    const type = document.getElementById('linkType').value;

    if (!from_id || !to_id) {
        alert('Please enter both IDs');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/mechanics/links`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ from_id, to_id, type })
        });

        if (!response.ok) throw new Error('Failed to add link');

        document.getElementById('linkFrom').value = '';
        document.getElementById('linkTo').value = '';

        alert('Link added!');
        loadAllMechanics();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function viewTree() {
    const rootId = parseInt(document.getElementById('treeRootId').value);

    if (!rootId) {
        alert('Please enter root mechanic ID');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/mechanics/${rootId}/tree`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) throw new Error('Failed to load tree');

        const tree = await response.json();
        displayTree(tree.root);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function displayTree(root) {
    const elements = [];
    const visited = new Set();

    function buildElements(node, parentId = null) {
        if (visited.has(node.id)) return;
        visited.add(node.id);

        elements.push({
            data: {
                id: `node-${node.id}`,
                label: node.name,
                description: node.description,
                year: node.year,
                mechanicId: node.id
            }
        });

        if (node.children) {
            node.children.forEach(child => {
                if (!child.node.cycle) {
                    buildElements(child.node, node.id);
                    elements.push({
                        data: {
                            id: `edge-${node.id}-${child.node.id}`,
                            source: `node-${node.id}`,
                            target: `node-${child.node.id}`,
                            type: child.type
                        }
                    });
                }
            });
        }
    }

    buildElements(root);

    if (cy) {
        cy.elements().remove();
        cy.add(elements);
        cy.layout({ name: 'cose-bilkent', directed: true, animate: true }).run();
    }
}