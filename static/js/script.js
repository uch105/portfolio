document.addEventListener('DOMContentLoaded', function() {
    const terminal = document.getElementById('terminal');
    const output = document.getElementById('output');
    const commandInput = document.getElementById('commandInput');

    // Handle command input
    commandInput.addEventListener('keydown', async function(e) {
        if (e.key === 'Enter') {
            const command = this.value.trim();
            console.log("Executing command:", command);
            this.value = '';
            
            addCommandToOutput(command);
            
            if (command.toLowerCase() === 'clear') {
                clearTerminal();
                return;
            }
            
            try {
                const response = await executeCommand(command);
                console.log("Command response:", response);
                
                if (!response) {
                    throw new Error("Empty response from server");
                }
                
                processResponse(response);
            } catch (error) {
                console.error("Command error:", error);
                addErrorToOutput(`Error: ${error.message}`);
            }
            
            scrollToBottom();
        }
    });

    // Focus input on terminal click
    terminal.addEventListener('click', function() {
        commandInput.focus();
    });

    // Execute command via POST request
    async function executeCommand(command) {
        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ command: command })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error("Fetch error:", error);
            throw error;
        }
    }

    function addCommandToOutput(command) {
        const commandElement = document.createElement('div');
        commandElement.className = 'command-output';
        commandElement.innerHTML = `<span class="prompt">guest@portfolio:~$</span> ${command}`;
        output.appendChild(commandElement);
    }

    function addErrorToOutput(message) {
        const errorElement = document.createElement('div');
        errorElement.className = 'response error';
        errorElement.innerHTML = `<p>${message}</p>`;
        output.appendChild(errorElement);
    }

    function clearTerminal() {
        output.innerHTML = `
            <pre class="ascii-owl">
          __________-------____                 ____-------__________
          \\------____-------___--__---------__--___-------____------/
           \\//////// / / / / / \\   _-------_   / \\ \\ \\ \\ \\ \\\\\\\\\\\\\\\\/
             \\////-/-/------/_/_| /___   ___\\ |_\\_\\------\\-\\-\\\\\\\\/
               --//// / /  /  //|| (O)\\ /(O) ||\\\\  \\  \\ \\ \\\\\\\\--
                    ---__/  // /| \\_  /V\\  _/ |\\ \\\\  \\__---
                         -//  / /\\_ ------- _/\\ \\  \\\\-
                           \\_/_/ /\\---------/\\ \\_\\_/
                               ----\\   |   /----
                                    | -|- |
                                   /   |   \\
                                  |____/\\___|
            </pre>
            <div class="command-output">
                <p>Welcome to my interactive portfolio!</p>
                <p>Type <span class="command">help</span> to see available commands.</p>
            </div>`;
        scrollToBottom();
    }

    function processResponse(response) {
        console.log("Processing response:", response);
        
        const responseElement = document.createElement('div');
        responseElement.className = 'response';
        
        switch (response.type) {
            case 'text':
                responseElement.innerHTML = formatTextResponse(response.content);
                break;
                
            case 'mixed':
                responseElement.innerHTML = response.content.map(item => {
                    if (item.type === 'text') {
                        return formatTextResponse(item.content);
                    } else if (item.type === 'image') {
                        return `<img src="${item.url}" alt="${item.alt}" class="response-image" width="250px" height="auto">`;
                    }
                    return '';
                }).join('');
                break;
                
            case 'gallery':
                responseElement.innerHTML = `
                    <div class="gallery">
                        ${response.content.map(item => `
                            <div class="gallery-item">
                                <img src="${item.image}" alt="${item.title}" class="response-image">
                                <h4>${item.title}</h4>
                                <p>${item.description}</p>
                                <a href="${item.link}" target="_blank" rel="noopener noreferrer">View Project</a>
                            </div>
                        `).join('')}
                    </div>`;
                break;
                
            case 'links':
                responseElement.innerHTML = `
                    <ul class="links-list">
                        ${response.content.map(item => `
                            <li><a href="${item.url}" target="_blank" rel="noopener noreferrer">${item.text}</a></li>
                        `).join('')}
                    </ul>`;
                break;
                
            case 'error':
                responseElement.className = 'response error';
                responseElement.innerHTML = `<p>${response.content}</p>`;
                break;
                
            default:
                responseElement.innerHTML = `<p>Unknown response type: ${response.type || 'undefined'}</p>`;
                console.warn("Unknown response type:", response);
        }
        
        output.appendChild(responseElement);
        scrollToBottom();
    }

    function formatTextResponse(text) {
        return text
            .replace(/^## (.*$)/gm, '<h3>$1</h3>')
            .replace(/^### (.*$)/gm, '<h4>$1</h4>')
            .replace(/^- (.*$)/gm, '<li>$1</li>')
            .replace(/\n/g, '<br>');
    }

    function scrollToBottom() {
        terminal.scrollTop = terminal.scrollHeight;
    }
});
