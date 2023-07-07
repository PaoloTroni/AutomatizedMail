//requerimos los módulos necesarios
require("dotenv").config();
const nodemailer = require("nodemailer");
const datosDestinatarios = require("./destinatarios.js");

// Los datos sensibles los pasamos a traves del .env
const { host, port, email, pass } = process.env;

//Hacemos la configuración del transporte de correo
const transporter = nodemailer.createTransport({
  host: host, // Servidor SMTP  - datos ocultos
  port: port, // Puerto utilizado por el servidor de email en cuestion
  secure: false, // Es necesario usar false para el servidor de email en cuestion
  auth: {
    user: email, // Tu direccion de email - datos ocultos
    pass: pass, // La contraseña de tu dirección  - datos ocultos
  },
});

// Definimos la función para enviar el correo
function enviarCorreo(destinatario, asunto, cuerpo, adjunto) {
  const mailOptions = {
    from: email, //Tu dirección de email - datos ocultos
    to: destinatario,
    subject: asunto,
    text: cuerpo,
    attachments: [{ filename: "./Mi-CV.pdf", path: adjunto }], //ojo a poner el adjunto correcto
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.log("Error al enviar el correo para", destinatario, error);
      console.log("");
    } else {
      console.log("Correo enviado para:", destinatario, info.response);
      console.log("");
    }
  });
}

// Elaboramos el código que ejecuta la función que envía los emails

console.log(
  `Hay ${datosDestinatarios.length} destinatario(s) en lista de envío.`
);
console.log("");
console.log("Empezamos los envíos:");
console.log("");

const asunto = "Auto Candidatura Desarrollador Full Stack"; //HAY QUE EDITAR EL ASUNTO

const adjunto = "./Mi-CV.pdf"; //PONER EL ADJUNTO CORRECTO

for (let i = 0; i < datosDestinatarios.length; i++) {
  let retraso = i * 3500;
  setTimeout(() => {
    const destinatario = datosDestinatarios[i].email;
    console.log("- Destinatario:", destinatario);

    const nombreEmpresa = datosDestinatarios[i].nombreEmpresa;
    const nombreResponsable = datosDestinatarios[i].nombreResponsable;
    console.log("- Empresa:", nombreEmpresa);
    const generarTextoPersonalizado = require("./texto.js");
    const texto = generarTextoPersonalizado(nombreResponsable, nombreEmpresa);

    enviarCorreo(destinatario, asunto, texto, adjunto);
    console.log(`Se está enviando el mail num: ${i + 1} para ${destinatario}`);
    console.log("");
  }, retraso);
}
