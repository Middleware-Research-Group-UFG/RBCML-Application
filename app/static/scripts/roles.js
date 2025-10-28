async function getId() {
    const urlParams = new URLSearchParams(window.location.search);
    const modelId = urlParams.get('model_id');

    if (!modelId) {
        console.error("Nenhum model_id encontrado na URL.");
        return null;
    }

    try {
        const response = await fetch('/static/model.json');
        const models = await response.json();

        const selectedModel = models.find(model => model.id === modelId);

        if (!selectedModel) {
            console.error(`Modelo com id ${modelId} não encontrado.`);
            return null;
        }

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
        console.error("Elemento com id 'roles-container' não encontrado.");
        return;
    }
    
    const formsHtml = model.roles.map(roleName => {
        return `
        <form action="/invite" method="POST">
        <div class="RoleType">
            <div class="Role-name">
                <h2>"${roleName}"</h2>
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

    container.innerHTML = formsHtml;
}





