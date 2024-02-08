function masquerTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.display = 'none';
}

function afficherTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.display = 'table';
}

function toggleTable(idTableau, idArrow) {
    var tableau = document.getElementById(idTableau);
    if (tableau.style.display === 'none') {
        afficherTableau(idTableau);
    } else {
        masquerTableau(idTableau);
    }
    
    toggleArrow(idArrow);
}

function toggleArrow(idArrow) {
    var arrow = document.getElementById(idArrow);
    var image = arrow.querySelector('img');
    if (image.getAttribute('src') === '/static/images/oeil-ferme.png') {
        image.setAttribute('src', '/static/images/oeil-ouvert.png');
    } else {
        image.setAttribute('src', '/static/images/oeil-ferme.png');
    }
}


document.getElementById('facile-arrow').addEventListener('click', function() {
    toggleTable('table_facile', 'facile-arrow');
});

document.getElementById('moyen-arrow').addEventListener('click', function() {
    toggleTable('table_moyen', 'moyen-arrow');
});

document.getElementById('difficile-arrow').addEventListener('click', function() {
    toggleTable('table_difficile', 'difficile-arrow');
});

document.addEventListener('DOMContentLoaded', function() {  /*ne pas pouvoir surligner d'élément dans la page (peut être pénible quand on clique sur l'oeil)*/
    document.addEventListener('selectstart', function(e) {
        e.preventDefault();
    });
});