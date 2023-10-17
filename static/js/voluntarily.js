
$(document).on('click', '.duzenle', function() {
    let id = $(this).data('id');
    let teyit = $(`.teyit[data-id="${id}"]`).is(':checked') ? 'Evet' : 'Hayır';
    let karsilandi = $(`.karsilandi[data-id="${id}"]`).is(':checked') ? 'Evet' : 'Hayır';

    $.ajax({
        url: `/duzenle/${id}`,
        method: 'POST',
        data: {
            teyit: teyit,
            karsilandi: karsilandi
        },
        success: function(response) {
            if (response.status === 'success') {
                alert('Değişiklikler başarıyla kaydedildi!');
            } else {
                alert('Bir hata oluştu.');
            }
        }
    });
});
function updateTable() {
    var searchValue = $("#searchInput").val().toLowerCase();

    var teyitChecked = $("#filterTeyit").is(':checked');
    var karsilandiChecked = $("#filterKarsilandi").is(':checked');

    $("tbody tr").each(function() {
        var currentRow = $(this);
        var teyitValue = currentRow.find('.teyit').prop('checked');
        var karsilandiValue = currentRow.find('.karsilandi').prop('checked');

        var rowText = currentRow.text().toLowerCase();
        var showRow = true;

        if (searchValue && !rowText.includes(searchValue)) {
            showRow = false;
        }

        if (teyitChecked && !teyitValue) {
            showRow = false;
        }

        if (karsilandiChecked && !karsilandiValue) {
            showRow = false;
        }

        if (showRow) {
            currentRow.show();
        } else {
            currentRow.hide();
        }
    });
}

$("#searchInput").on('keyup', updateTable);
$("#filterTeyit, #filterKarsilandi").on('change', updateTable);