document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileStatus = document.getElementById('file-status');
    const filenameDisplay = document.getElementById('filename-display');

    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    const systemStatus = document.getElementById('system-status');
    const statusText = document.getElementById('status-text');

    // State
    let isProcessing = false;

    // --- Upload Handling ---
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleUpload(e.target.files[0]);
        }
    });

    async function handleUpload(file) {
        // Check MIME type or file extension
        if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
            showError('Only PDF files are supported.');
            return;
        }

        updateStatus('Processing...', 'busy');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Upload failed');
            }

            const data = await response.json();

            // UI Update
            dropZone.style.display = 'none';
            fileStatus.style.display = 'block';
            filenameDisplay.textContent = file.name;

            updateStatus('Online', 'active');
            enableChat();
            addBotMessage(`Analysis complete. I have processed ${data.chunks} segments from "${file.name}". Ready for queries.`);

        } catch (error) {
            console.error(error);
            updateStatus('Error', 'error');
            showError(`Failed to process file: ${error.message}`);
        }
    }

    // --- Chat Handling ---
    function enableChat() {
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text || isProcessing) return;

        // Add User Message
        addUserMessage(text);
        userInput.value = '';
        isProcessing = true;

        // Show Typing Indicator
        const typingId = addTypingIndicator();
        updateStatus('Thinking...', 'busy');

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text })
            });

            const data = await response.json();

            // Remove Typing Indicator
            removeMessage(typingId);

            if (data.answer) {
                addBotMessage(data.answer);
            } else {
                addBotMessage("I couldn't find a relevant answer in the document.");
            }

        } catch (error) {
            removeMessage(typingId);
            addBotMessage("System Error: Unable to retrieve response.");
        } finally {
            isProcessing = false;
            updateStatus('Online', 'active');
        }
    }

    // --- UI Helpers ---
    function addUserMessage(text) {
        const div = document.createElement('div');
        div.className = 'message user-message';
        div.textContent = text;
        appendMessage(div);
    }

    function addBotMessage(text) {
        const div = document.createElement('div');
        div.className = 'message bot-message';
        div.textContent = text;
        appendMessage(div);
    }

    function addTypingIndicator() {
        const id = 'typing-' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.className = 'typing-indicator';
        div.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        appendMessage(div);
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function appendMessage(el) {
        chatMessages.appendChild(el);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function updateStatus(text, state) {
        statusText.textContent = text;
        systemStatus.className = 'status-dot'; // reset
        if (state === 'active') systemStatus.classList.add('active');
        if (state === 'busy') systemStatus.style.background = '#ffbb00';
        if (state === 'error') systemStatus.style.background = '#ff0055';
    }

    function showError(msg) {
        alert(msg); // Simple alert for now, could be a toast
    }
});
