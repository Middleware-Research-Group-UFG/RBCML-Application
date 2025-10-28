const jsonUrl = '/static/model.json';


let slideIndex = 0; 
let slideData = null;

async function initSlider() {
    try {
        const response = await fetch(jsonUrl);
        slideData = await response.json(); 
        renderslider(); 
        showNextImage(); 
        setInterval(showNextImage, 10000); 
    } catch (error) {
        console.error("Erro ao carregar os dados do slider:", error);
    }
}

function showNextImage() {
    if (!slideData) return;

    const currentSlideObject = slideData[slideIndex];
    const imageUrl = currentSlideObject.imagem.src;
    const altText = currentSlideObject.imagem.alt;  
    const imgElement = document.querySelector('.slides img');

    const ModelID = currentSlideObject.id;
    const createCallButton = document.querySelector('.create-session-button');

    if (imgElement) {
        imgElement.src = imageUrl;
        imgElement.alt = altText;
    
        if (createCallButton) {
            createCallButton.href = `/createcall?model_id=${ModelID}`;
        }

        slideIndex++;
        if (slideIndex >= slideData.length) {
            slideIndex = 0;
        }
    }
}


function renderslider() {
    document.querySelector('.slide').innerHTML = `
    <div class="slides">
    <button class="left" id="go.left"> < </button>
    <img src= "" alt="">
    <button class="right" id="go.right"> > </button>    
        <button class="create-session">
            <a href="/createcall" class="create-session-button">
                <h1>Criar Sessão</h1>
            </a>
        </button>
    </div>
    `
}

initSlider();