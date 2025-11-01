let roomsData = null;

async function initSlider() {
    try {
        // Buscar modelos da API do backend
        const response = await fetch('/api/models');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const models = await response.json();
        
        // Adicionar o card "Crie um Room" no início
        roomsData = [
            {
                "id": "new",
                "name": "Crie um Room",
                "description": "Crie seu proprio Room.",
                "imagem": {
                    "src": "images/plus.png",
                    "alt": "Plus"
                }
            },
            ...models
        ];
        
        renderRooms(); 
    } catch (error) {
        console.error("Erro ao carregar os dados das salas:", error);
        const roomsContainer = document.getElementById('rooms-container-id');
        if (roomsContainer) {
            roomsContainer.innerHTML = '<p style="color: red; text-align: center;">Erro ao carregar as salas.</p>';
        }
    }
}

function renderRooms() {
    if (!roomsData || !Array.isArray(roomsData)) {
        console.warn("Dados das salas não estão disponíveis");
        return;
    }

    const roomsContainer = document.getElementById('rooms-container-id');
    
    if (!roomsContainer) {
        console.error("Container de salas não encontrado");
        return;
    }

    const roomsHtml = roomsData.map((room) => {
        // Para o primeiro item (id === "new"), vai para createModel
        // Para os outros, vai para createcall com o model_id
        const href = room.id === "new"
            ? `/createModel`
            : `/createcall?model_id=${room.id}`;
        
        // Garantir que o caminho da imagem está correto
        const imgSrc = room.imagem.src.startsWith('/static/') 
            ? room.imagem.src 
            : `/static/${room.imagem.src}`;
        
        return `
        <div class="rooms-card">
            <a href="${href}" class="rooms-link"> 
                <img src="${imgSrc}" alt="${room.imagem.alt}" loading="lazy">
                <p>${room.description}</p>
                <h3>${room.name}</h3>
            </a>
        </div>
        `;
    }).join('');
    
    roomsContainer.innerHTML = roomsHtml;
}

// Inicializar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSlider);
} else {
    initSlider();
}