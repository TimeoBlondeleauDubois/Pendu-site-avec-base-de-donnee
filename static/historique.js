document.addEventListener('DOMContentLoaded', function() {
    // Afficher par défaut
    afficherTableau('table_facile');
    afficherTableau('table_moyen');
    afficherTableau('table_difficile');
});


function masquerTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.visibility = 'hidden';
}

function afficherTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.visibility = 'visible';
}

function toggleTable(idTableau, idArrow) {
    var tableau = document.getElementById(idTableau);
    if (tableau.style.visibility === 'hidden') {
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
