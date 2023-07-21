//requerimos fs
const fs = require("fs");
const path = require("path"); // Agregamos la librería "path" para trabajar con rutas

// Obtenemos la ruta absoluta del archivo destinatarios.json en la carpeta src
const rutaArchivoJson = path.join(__dirname, "destinatarios.json");

//guardamos en "data" el contenido del json generado por los archivos de python
const data = fs.readFileSync(rutaArchivoJson, "utf-8");

//console.log(`eso es data antes de parsear: ${data} boooh`);
//console.log("el codigo llega hasta aqui");

//parseamos los datos y los metemos en la constante que nos sirve
const datosDestinatarios = JSON.parse(data);

// console.log("eso es datosDestinatarios, que deberia estar parseador", datosDestinatarios);

module.exports = datosDestinatarios;
