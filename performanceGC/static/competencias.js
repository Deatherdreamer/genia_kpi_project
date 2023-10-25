
// Obtener la tabla que deseas actualizar por su identificador
const table = document.getElementById('tabla-competencias');

// Obtener todos los elementos de entrada de la tabla
const valorInputs = table.querySelectorAll('input[name^="comv"]');



// Recorrer todos los elementos de entrada y agregar un controlador de eventos
valorInputs.forEach(input => {
    input.addEventListener('input', () => {
        // Obtener el valor del campo "Valor"
        const valor = input.value;

        console.log('Valor:', valor); // Depuración

        // Calcular el valor multiplicado por 0.25
        const total = valor * 0.25;

        console.log('Total:', total); // Depuración

        // Obtener el campo "Total" correspondiente y actualizar su valor
        const totalInput = input.parentNode.nextElementSibling.querySelector('input[type="text"]');
        totalInput.value = total;
    });
});



