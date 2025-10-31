const jsonUrl = 'model.json';

async function initSlider() {
    try {
        const response = await fetch(jsonUrl);
        roomsData = await response.json(); 
        renderRooms(); 
    } catch (error) {
        console.error("Erro ao carregar os dados das salas:", error);
    }
}

function renderRooms() {
    if (!roomsData) return;

    const roomsContainer = document.getElementById('rooms-container-id');

    const roomsHtml = roomsData.map((room, index) => {
        const href = index === 0 
            ? `static/pages/createModel.html?nome=${encodeURIComponent(room.name)}`
            : `static/pages/createcall.html?nome=${encodeURIComponent(room.name)}`;
        return `
        <div class="rooms-card">
            <a href="${href}" class="rooms-link"> 
                <img src="${room.imagem.src}" alt="${room.imagem.alt}">
                <p>${room.description}</p>
                <h3>${room.name}</h3>
            </a>
        </div>
        `;
    }).join('');
    
    roomsContainer.innerHTML = roomsHtml;
}

initSlider();