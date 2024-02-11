fetch("https://api.open-meteo.com/v1/forecast?latitude=56.51&longitude=25.86&hourly=temperature_2m&current_weather=true&windspeed_unit=ms")
.then(response => response.json())
.then(dati => {
  document.getElementById("temp").innerHTML = "Šī brīža temperatūra Rīgā: "+dati["current_weather"]["temperature"]+"°C";
})