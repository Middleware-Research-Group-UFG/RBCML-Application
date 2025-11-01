async function getId() {
    const urlParams = new URLSearchParams(window.location.search);
    const modelId = urlParams.get('model_id');
    
    console.log("URL params:", window.location.search);
    console.log("Model ID from URL:", modelId);

    if (!modelId) {
        console.error("Nenhum 'model_id' encontrado na URL.");
        return null;
    }

    try {
        // Buscar modelo específico da API
        const response = await fetch(`/api/model/${modelId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const modelData = await response.json();
        
        console.log("Model loaded:", modelData);
        return modelData;

    } catch (error) {
        console.error("Erro ao carregar o modelo:", error);
        return null;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const model = await getId(); 
  
    if (model) {
        console.log("Modelo selecionado:", model);
        console.log("Roles do modelo:", model.definition.roles);
    
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
    
    const roles = model.definition.roles || [];
    console.log("Model roles:", roles);
    
    if (!roles || roles.length === 0) {
        console.warn("Modelo não possui roles definidas.");
        container.innerHTML = '<p>Este modelo não possui roles definidas.</p>';
        return;
    }
    
    const formsHtml = roles.map(roleName => {
        return `
        <form action="/invite" method="POST">
        <div class="RoleType">
            <div class="Role-name">
                <h2>${roleName}</h2>
            </div>
            <div class="email-input-container">
                <input type="email" name="email" placeholder="Digite o email" required>
                <input type="hidden" name="role" value="${roleName}">
                <input type="hidden" name="model_id" value="${model.id}">
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
