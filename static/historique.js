
function masquerTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.display = 'none';
}

function afficherTableau(idTableau) {
    var tableau = document.getElementById(idTableau);
    tableau.style.display = 'table';
}

document.querySelector('.table-section:nth-child(1) .title-container2').addEventListener('click', function() {
    var tableauFacile = document.getElementById('table_facile');
    if (tableauFacile.style.display === 'none') {
        afficherTableau('table_facile');
    } else {
        masquerTableau('table_facile');
    }
});

document.querySelector('.table-section:nth-child(2) .title-container2').addEventListener('click', function() {
    var tableauMoyen = document.getElementById('table_moyen');
    if (tableauMoyen.style.display === 'none') {
        afficherTableau('table_moyen');
    } else {
        masquerTableau('table_moyen');
    }
});

document.querySelector('.table-section:nth-child(3) .title-container2').addEventListener('click', function() {
    var tableauDifficile = document.getElementById('table_difficile');
    if (tableauDifficile.style.display === 'none') {
        afficherTableau('table_difficile');
    } else {
        masquerTableau('table_difficile');
    }
});
