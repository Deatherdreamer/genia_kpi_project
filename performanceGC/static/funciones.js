

const funciones = document.querySelectorAll('table:first-of-type input[type="number"]');
const pesos = document.querySelectorAll('table:first-of-type input[name^="peso"]');
const resultados = document.querySelectorAll('table:first-of-type input[name^="valor"]');
const totales = document.querySelectorAll('table:first-of-type input[name^="total"]');

function calcularTotalFunciones() {
	let totalFunciones = 0;
	for (let i = 0; i < funciones.length; i++) {
		if (pesos[i].value !== '' && resultados[i].value !== '') {
			const total = pesos[i].value / 100 * resultados[i].value;
			totales[i].value = total.toFixed(2);
			totalFunciones += total;
		} else {
			totales[i].value = '';
		}
	}
	document.querySelector('input[name="total"]').value = totalFunciones.toFixed(2);
}

for (let i = 0; i < funciones.length; i++) {
	pesos[i].addEventListener('input', calcularTotalFunciones);
	resultados[i].addEventListener('input', calcularTotalFunciones);
}