let roomsData = null;

async function initSlider() {
    try {
        // Caminho correto para acessar o arquivo JSON no Flask
        const response = await fetch('/static/model.json');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        roomsData = await response.json(); 
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

    const roomsHtml = roomsData.map((room, index) => {
        // Para Flask routes, usar caminhos relativos ou absolutos corretos
        const href = index === 0 
            ? `/createModel?nome=${encodeURIComponent(room.name)}`
            : `/createcall?nome=${encodeURIComponent(room.name)}`;
        
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