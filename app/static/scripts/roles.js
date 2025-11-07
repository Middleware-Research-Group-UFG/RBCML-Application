async function getId() {
    const urlParams = new URLSearchParams(window.location.search);
    const modelId = urlParams.get('nome');
    
    console.log("URL params:", window.location.search);
    console.log("Model ID from URL:", modelId);

    if (!modelId) {
        console.error("Nenhum 'nome' encontrado na URL.");
        return null;
    }

    try {
        const response = await fetch('../../model.json');
        const models = await response.json();
        
        console.log("Models loaded:", models);
        console.log("Looking for model with name:", modelId);

        const selectedModel = models.find(model => model.name === modelId);

        if (!selectedModel) {
            console.error(`Modelo com name "${modelId}" não encontrado.`);
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
    
    const formsHtml = model.roles.map(roleName => {
        return `
        <form action="/invite" method="POST">
        <div class="RoleType">
            <div class="Role-name">
                <h2>${roleName}</h2>
            </div>
            <div class="email-input-container">
                <input type="email" name="email" placeholder="Digite o email" required>
                <button type="submit" class="circular-button">
                    <span>→</span>
                </button>
            </div>
        </div>
      </form>
        `;
    }).join('');

    console.log("Generated HTML:", formsHtml);
    container.innerHTML = formsHtml;
    console.log("Roles displayed successfully!");
}





