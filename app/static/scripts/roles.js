// Variáveis globais
let currentModel = null;
let participantsData = {};

async function getId() {
    const urlParams = new URLSearchParams(window.location.search);
    const modelName = urlParams.get('nome');
    
    console.log("URL params:", window.location.search);
    console.log("Model name from URL:", modelName);

    if (!modelName) {
        console.error("Nenhum 'nome' encontrado na URL.");
        return null;
    }

    try {
        const response = await fetch('/static/model.json');
        const models = await response.json();
        
        console.log("Models loaded:", models);
        console.log("Looking for model with name:", modelName);

        const selectedModel = models.find(model => model.name === modelName);

        if (!selectedModel) {
            console.error(`Modelo com name "${modelName}" não encontrado.`);
            console.error("Available models:", models.map(m => m.name));
            return null;
        }

        console.log("Selected model:", selectedModel);
        return selectedModel;

    } catch (error) {
        console.error("Erro ao carregar ou processar o model.json:", error);
        return null; 
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const model = await getId(); 
  
    if (model) {
        console.log("Modelo selecionado:", model);
        console.log("Roles do modelo:", model.roles);
        currentModel = model;
        displayRolesInvites(model);
    }
});

function displayRolesInvites(model) {
    const container = document.getElementById('roles-card-container');
    if (!container) {
        console.error("Elemento com id 'roles-card-container' não encontrado.");
        return;
    }
    
    console.log("Container found:", container);
    console.log("Model roles:", model.roles);
    
    if (!model.roles || model.roles.length === 0) {
        console.warn("Modelo não possui roles definidas.");
        container.innerHTML = '<p>Este modelo não possui roles definidas.</p>';
        return;
    }
    
    const formsHtml = model.roles.map((roleName, index) => {
        return `
        <div class="RoleType" data-role="${roleName}">
            <div class="Role-name">
                <h2>${roleName}</h2>
            </div>
            <div class="email-input-container">
                <input type="email" 
                       id="email-${index}" 
                       data-role="${roleName}"
                       placeholder="Email do participante (opcional)" 
                       class="email-input">
                <button type="button" 
                        class="circular-button add-participant-btn"
                        data-role="${roleName}"
                        data-index="${index}"
                        onclick="addParticipant(${index}, '${roleName}')">
                    <span>→</span>
                </button>
            </div>
            <div class="participants-list" id="participants-list-${index}"></div>
        </div>
        `;
    }).join('');

    console.log("Generated HTML:", formsHtml);
    container.innerHTML = formsHtml;
    console.log("Roles displayed successfully!");
}

function addParticipant(index, roleName) {
    const input = document.getElementById(`email-${index}`);
    const email = input.value.trim();
    
    if (!email) {
        return;
    }
    
    // Validação básica de email
    if (!email.includes('@')) {
        alert('Por favor, digite um email válido');
        return;
    }
    
    // Adicionar aos dados
    if (!participantsData[email]) {
        participantsData[email] = {
            email: email,
            roles: []
        };
    }
    
    if (!participantsData[email].roles.includes(roleName)) {
        participantsData[email].roles.push(roleName);
    }
    
    // Limpar input
    input.value = '';
    
    // Atualizar lista visual
    updateParticipantsList();
    
    // Feedback visual
    const button = document.querySelector(`button[data-index="${index}"]`);
    button.style.backgroundColor = '#4CAF50';
    setTimeout(() => {
        button.style.backgroundColor = '';
    }, 500);
    
    console.log('Participant added:', email, roleName);
    console.log('Current participants:', participantsData);
}

function updateParticipantsList() {
    // Limpar todas as listas
    document.querySelectorAll('.participants-list').forEach(list => {
        list.innerHTML = '';
    });
    
    // Adicionar participantes às listas correspondentes
    Object.entries(participantsData).forEach(([email, data]) => {
        data.roles.forEach(role => {
            const roleIndex = currentModel.roles.indexOf(role);
            if (roleIndex >= 0) {
                const listElement = document.getElementById(`participants-list-${roleIndex}`);
                if (listElement) {
                    const tag = document.createElement('span');
                    tag.className = 'participant-tag';
                    tag.textContent = email;
                    tag.onclick = () => removeParticipant(email, role);
                    tag.title = 'Clique para remover';
                    listElement.appendChild(tag);
                }
            }
        });
    });
}

function removeParticipant(email, role) {
    if (participantsData[email]) {
        participantsData[email].roles = participantsData[email].roles.filter(r => r !== role);
        if (participantsData[email].roles.length === 0) {
            delete participantsData[email];
        }
    }
    updateParticipantsList();
    console.log('Participant removed:', email, role);
}

async function startCall() {
    if (!currentModel) {
        alert('Erro: Modelo não carregado. Por favor, recarregue a página.');
        return;
    }
    
    console.log('Iniciando chamada...');
    console.log('Modelo:', currentModel.name);
    console.log('Participantes:', participantsData);
    
    try {
        // Criar chamada
        const response = await fetch('/api/create-call', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model_name: currentModel.name,
                participants: participantsData
            })
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            console.log('Chamada criada com sucesso!');
            console.log('Call ID:', result.call_id);
            console.log('URL:', result.call_url);
            
            const shareUrl = result.share_url;
            const callId = result.call_id;
            
            // Enviar convites por email se houver participantes
            if (Object.keys(participantsData).length > 0) {
                const invites = [];
                Object.entries(participantsData).forEach(([email, data]) => {
                    data.roles.forEach(role => {
                        invites.push({ email, role });
                    });
                });
                
                try {
                    await fetch('/api/send-invites', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            call_id: callId,
                            invites: invites
                        })
                    });
                    console.log('Convites enviados com sucesso!');
                } catch (error) {
                    console.warn('Erro ao enviar convites:', error);
                }
            }
            
            // Mostrar link compartilhável e redirecionar
            const message = `Chamada criada com sucesso!\n\n` +
                          `Link para compartilhar:\n${shareUrl}\n\n` +
                          `${Object.keys(participantsData).length > 0 ? 'Convites enviados por email!\n\n' : ''}` +
                          `Clique em OK para entrar na chamada.`;
            
            alert(message);
            
            // Redirecionar para a chamada
            window.location.href = result.call_url;
        } else {
            alert('Erro ao criar chamada: ' + (result.error || 'Erro desconhecido'));
            console.error('Error:', result.error);
        }
    } catch (error) {
        console.error('Erro ao iniciar chamada:', error);
        alert('Erro ao conectar com o servidor. Por favor, tente novamente.');
    }
}





