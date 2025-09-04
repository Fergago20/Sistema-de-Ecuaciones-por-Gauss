const numEcuacionesInput = document.getElementById("numEcuaciones");
const numIncognitasInput = document.getElementById("numIncognitas");
const btnGenerar = document.getElementById("btnGenerar");
const ecuacionesContainer = document.getElementById("ecuacionesContainer");
const ecuacionesInputs = document.getElementById("ecuacionesInputs");
const btnResolver = document.getElementById("btnResolver");
const resultadoContainer = document.getElementById("resultadoContainer");
const resultadoTabla = document.getElementById("resultadoTabla");
const errorMsg = document.getElementById("errorMsg");

let ecuaciones = [];

// Generar los campos dinámicos
btnGenerar.addEventListener("click", async () => {
    const numEcuaciones = parseInt(numEcuacionesInput.value);
    const numIncognitas = parseInt(numIncognitasInput.value);

    resultadoContainer.classList.add("hidden");
    errorMsg.classList.add("hidden");

    if (!numEcuaciones || !numIncognitas || numEcuaciones <= 0 || numIncognitas <= 0) {
        mostrarError("Número de ecuaciones e incógnitas deben ser enteros positivos.");
        return;
    }

    // Inicializar la matriz con ceros
    ecuaciones = Array(numEcuaciones)
        .fill(null)
        .map(() => Array(numIncognitas + 1).fill(0));

    generarInputs(numEcuaciones, numIncognitas);
    ecuacionesContainer.classList.remove("hidden");
});

// Crear inputs de la matriz
function generarInputs(filas, columnas) {
    ecuacionesInputs.innerHTML = "";
    for (let i = 0; i < filas; i++) {
        const filaDiv = document.createElement("div");
        filaDiv.className = "flex gap-2 justify-center mb-2";
        for (let j = 0; j < columnas + 1; j++) {
            const input = document.createElement("input");
            input.type = "number";
            input.step = "any";
            input.value = 0;
            input.placeholder = j === columnas ? "b" : `x${j + 1}`;
            input.className = "border p-2 rounded-lg w-16 text-center";
            input.addEventListener("input", (e) => handleInputChange(i, j, e.target.value));
            filaDiv.appendChild(input);
        }
        ecuacionesInputs.appendChild(filaDiv);
    }
}

// Manejar cambios en los inputs
function handleInputChange(i, j, value) {
    const nuevas = ecuaciones.map((fila) => [...fila]);
    let val = parseFloat(value);
    if (isNaN(val)) val = 0; // si está vacío o inválido
    nuevas[i][j] = val;
    ecuaciones = nuevas;
}

// Resolver el sistema
btnResolver.addEventListener("click", async () => {
    resultadoContainer.classList.add("hidden");
    errorMsg.classList.add("hidden");

    try {
        // Asegurarse de que todos los valores sean números
        const enviarEcuaciones = ecuaciones.map(fila =>
            fila.map(x => parseFloat(x) || 0)
        );

        const res = await fetch("/resolver", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ecuaciones: enviarEcuaciones }),
        });

        const data = await res.json();
        if (!res.ok) {
            mostrarError(data.error);
            return;
        }

        mostrarResultado(data.matriz_resuelta);
    } catch (err) {
        mostrarError("Error al conectar con el servidor.");
    }
});

// Mostrar el resultado en tabla
function mostrarResultado(matriz) {
    resultadoTabla.innerHTML = "";
    matriz.forEach((fila) => {
        const tr = document.createElement("tr");
        fila.forEach((valor) => {
            const td = document.createElement("td");
            td.className = "border p-2 text-center";
            td.textContent = Number(valor).toFixed(2);
            tr.appendChild(td);
        });
        resultadoTabla.appendChild(tr);
    });
    resultadoContainer.classList.remove("hidden");
}

// Mostrar error
function mostrarError(msg) {
    errorMsg.textContent = msg;
    errorMsg.classList.remove("hidden");
}
