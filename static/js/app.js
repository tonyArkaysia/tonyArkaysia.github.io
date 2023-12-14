// Access the JSON data for Eastern Conference from the HTML element
const eastConfDataJsonString = document.getElementById('east-conf-data').getAttribute('data-east-conf-standings');

// Access the JSON data for Western Conference from the HTML element
const westConfDataJsonString = document.getElementById('west-conf-data').getAttribute('data-west-conf-standings');

// Parse the JSON strings to JavaScript objects
const eastConfData = JSON.parse(eastConfDataJsonString);
const westConfData = JSON.parse(westConfDataJsonString);

// Now, you can work with the 'eastConfData' and 'westConfData' objects in JavaScript
console.log('Eastern Conference Standings:', eastConfData);
console.log('Western Conference Standings:', westConfData);
