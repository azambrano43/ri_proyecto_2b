document.getElementById('queryForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const popup = document.getElementById('backupPopup');
    popup.style.display = 'flex';

    const formData = new FormData(this);

    fetch('/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.text())
    .then(data => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(data, 'text/html');

        // Seleccionar la nueva respuesta y contexto
        const newResult = doc.querySelector('.result');
        const newContext = doc.getElementById('contextSection');
        const newMetrics = doc.getElementById('metrics');

        // Insertar la respuesta después del formulario
        insertAfter(document.getElementById('queryForm'), newResult);

        // Insertar el contexto después del botón de "Mostrar/Ocultar Contexto"
        const toggleContextButton = document.getElementById('toggleContextButton');
        if (toggleContextButton) insertAfter(toggleContextButton, newContext);

        // Actualizar las métricas en su lugar original
        updateElement('#metrics', newMetrics);
        popup.style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al procesar la consulta');
        popup.style.display = 'none';
    });
});

// Función para insertar un elemento después de otro
function insertAfter(referenceNode, newNode) {
    if (newNode) {
        referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
    }
}

// Función para actualizar elementos si existen
function updateElement(selector, newElement) {
    const oldElement = document.querySelector(selector);
    if (newElement) {
        if (oldElement) {
            oldElement.replaceWith(newElement);
        } else {
            document.querySelector('.container').appendChild(newElement);
        }
    } else if (oldElement) {
        oldElement.remove();  // Si no hay contenido nuevo, se elimina el anterior
    }
}







function toggleMetrics() {
    var metrics = document.getElementById("metrics");
    metrics.style.display = (metrics.style.display === "none" || metrics.style.display === "") ? "block" : "none";
}

function toggleContext() {
    var contextSection = document.getElementById("contextSection");
    contextSection.style.display = (contextSection.style.display === "none" || contextSection.style.display === "") ? "block" : "none";
}

function toggleRow(button) {
    var row = button.closest("tr").nextElementSibling;
    if (row.classList.contains("row-hidden")) {
        row.classList.remove("row-hidden");
        button.textContent = "Ver menos";
    } else {
        row.classList.add("row-hidden");
        button.textContent = "Ver más";
    }
}
