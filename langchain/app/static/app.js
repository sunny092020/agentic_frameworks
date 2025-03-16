document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            // Update active button
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update active content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabId) {
                    content.classList.add('active');
                }
            });
        });
    });
    
    // Session ID for memory chat
    const sessionId = 'user_' + Math.random().toString(36).substring(2, 9);
    let documentUploaded = false;
    
    // Simple Chat
    document.getElementById('simple-send').addEventListener('click', async () => {
        const prompt = document.getElementById('simple-prompt').value.trim();
        const responseElement = document.getElementById('simple-response');
        
        if (!prompt) return;
        
        responseElement.textContent = 'Thinking...';
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: prompt })
            });
            
            const data = await response.json();
            responseElement.textContent = data.response;
        } catch (error) {
            responseElement.textContent = 'Error: ' + error.message;
        }
    });
    
    // Memory Chat
    document.getElementById('memory-send').addEventListener('click', async () => {
        const prompt = document.getElementById('memory-prompt').value.trim();
        const messagesContainer = document.getElementById('memory-messages');
        
        if (!prompt) return;
        
        // Add user message
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('user-message');
        userMessageElement.textContent = prompt;
        messagesContainer.appendChild(userMessageElement);
        
        // Add thinking message
        const thinkingElement = document.createElement('div');
        thinkingElement.classList.add('system-message');
        thinkingElement.textContent = 'Thinking...';
        messagesContainer.appendChild(thinkingElement);
        
        // Clear input
        document.getElementById('memory-prompt').value = '';
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        try {
            const response = await fetch('/chat_with_memory', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    query: prompt,
                    session_id: sessionId
                })
            });
            
            const data = await response.json();
            
            // Remove thinking message
            messagesContainer.removeChild(thinkingElement);
            
            // Add assistant message
            const assistantMessageElement = document.createElement('div');
            assistantMessageElement.classList.add('assistant-message');
            assistantMessageElement.textContent = data.response;
            messagesContainer.appendChild(assistantMessageElement);
            
            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        } catch (error) {
            // Remove thinking message
            messagesContainer.removeChild(thinkingElement);
            
            // Add error message
            const errorElement = document.createElement('div');
            errorElement.classList.add('system-message');
            errorElement.textContent = 'Error: ' + error.message;
            messagesContainer.appendChild(errorElement);
            
            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    });
    
    // Clear memory
    document.getElementById('clear-memory').addEventListener('click', () => {
        const messagesContainer = document.getElementById('memory-messages');
        messagesContainer.innerHTML = '<div class="system-message">Memory cleared. Start a new conversation!</div>';
        
        // Generate new session ID
        sessionId = 'user_' + Math.random().toString(36).substring(2, 9);
    });
    
    // Document Upload
    document.getElementById('upload-btn').addEventListener('click', async () => {
        const fileInput = document.getElementById('document-file');
        const statusElement = document.getElementById('document-status');
        const askButton = document.getElementById('document-ask');
        
        if (!fileInput.files.length) {
            statusElement.textContent = 'Please select a file first.';
            statusElement.className = 'error';
            return;
        }
        
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        statusElement.textContent = 'Uploading and processing document...';
        statusElement.className = '';
        
        try {
            const response = await fetch('/document_qa', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                statusElement.textContent = data.message || 'Document uploaded and processed successfully.';
                statusElement.className = 'success';
                askButton.disabled = false;
                documentUploaded = true;
            } else {
                statusElement.textContent = data.detail || 'Error uploading document.';
                statusElement.className = 'error';
            }
        } catch (error) {
            statusElement.textContent = 'Error: ' + error.message;
            statusElement.className = 'error';
        }
    });
    
    // Document QA
    document.getElementById('document-ask').addEventListener('click', async () => {
        const query = document.getElementById('document-query').value.trim();
        const responseElement = document.getElementById('document-response');
        const fileInput = document.getElementById('document-file');
        
        if (!query) return;
        if (!documentUploaded) {
            responseElement.textContent = 'Please upload a document first.';
            return;
        }
        
        responseElement.textContent = 'Thinking...';
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('query', query);
        
        try {
            const response = await fetch('/document_qa', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            responseElement.textContent = data.response;
        } catch (error) {
            responseElement.textContent = 'Error: ' + error.message;
        }
    });
    
    // Agent
    document.getElementById('agent-send').addEventListener('click', async () => {
        const prompt = document.getElementById('agent-prompt').value.trim();
        const responseElement = document.getElementById('agent-response');
        
        if (!prompt) return;
        
        responseElement.textContent = 'Agent is working on your task...';
        try {
            const response = await fetch('/agent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: prompt })
            });
            
            const data = await response.json();
            responseElement.textContent = data.response;
        } catch (error) {
            responseElement.textContent = 'Error: ' + error.message;
        }
    });
}); 