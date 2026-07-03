const express = require('express');
const mysql = require('mysql2');
const ruta = require('path');
const http = require('http'); // Necesario para socket.io
const { Server } = require('socket.io');

const aplicacion = express();
const servidorHttp = http.createServer(aplicacion);
const io = new Server(servidorHttp);

var puerto = 8080;

// Configuración de la base de datos
var conexion = mysql.createConnection({
  host: 'localhost',
  user: 'sistema', 
  password: '12345678', 
  database: 'estacion_meteorologica'
});

conexion.connect(function(error) {
  if (error) {
    console.log(error);
    return;
  }
  console.log('Conectado a mysql');
});

// Cuando un cliente web se conecta
io.on('connection', function(socket) {
  console.log('Un cliente se ha conectado a WebSockets');
});

aplicacion.get('/', function(req, res) {
  res.sendFile(__dirname + '/index.html');
});

// Endpoint para obtener datos con paginación
aplicacion.get('/obtener_datos', function(peticion, respuesta) {
  var ultimo_id = peticion.query.ultimo_id;
  var primer_id = peticion.query.primer_id;
  var direccion = peticion.query.direccion;
  
  // Por defecto, carga los últimos 10
  var consulta = 'SELECT id_lectura, id_estacion, temperatura, humedad, lluvia, velocidad_viento, direccion_viento, fecha_hora FROM lectura ORDER BY id_lectura DESC LIMIT 10';
  var parametros = [];

  // Si piden la página "siguiente", buscamos IDs menores al último visto
  if (direccion === 'siguiente' && ultimo_id) {
    consulta = 'SELECT id_lectura, id_estacion, temperatura, humedad, lluvia, velocidad_viento, direccion_viento, fecha_hora FROM lectura WHERE id_lectura < ? ORDER BY id_lectura DESC LIMIT 10';
    parametros = [ultimo_id];
  } 
  // Si piden la página "anterior", buscamos IDs mayores al primero visto y luego reordenamos
  else if (direccion === 'anterior' && primer_id) {
    consulta = 'SELECT * FROM (SELECT id_lectura, id_estacion, temperatura, humedad, lluvia, velocidad_viento, direccion_viento, fecha_hora FROM lectura WHERE id_lectura > ? ORDER BY id_lectura ASC LIMIT 10) AS t ORDER BY id_lectura DESC';
    parametros = [primer_id];
  }

  conexion.query(consulta, parametros, function(error, resultados) {
    if (error) {
      console.log('error query', error);
      respuesta.json([]); 
    } else {
      respuesta.json(resultados); 
    }
  });
});

// Endpoint para simular que llega un dato de MQTT
aplicacion.get('/simular_lectura', function(peticion, respuesta) {
  // Simular datos acordes a la base de datos real
  var nueva_lectura = {
    id_lectura: 9999 + Math.floor(Math.random() * 100),
    id_estacion: 1,
    temperatura: (Math.random() * 40).toFixed(2),
    humedad: (Math.random() * 100).toFixed(2),
    lluvia: (Math.random() * 10).toFixed(2),
    velocidad_viento: (Math.random() * 20).toFixed(2),
    direccion_viento: 'Norte',
    fecha_hora: new Date().toISOString().replace('T', ' ').substring(0, 19)
  };
  
  // Enviar a todos los clientes web conectados
  io.emit('nueva_lectura', nueva_lectura);
  respuesta.send('Simulación enviada. Revisa la página web sin recargar.');
});

servidorHttp.listen(puerto, function() {
  console.log('servidor arriba en puerto 8080');
});
