$(document).ready(function() {
    $('.select2').select2({
        theme: 'bootstrap',
    });
});

function submitPopupForm(formId, url, entityType) {
    $(formId).on('submit', function(e) {
        e.preventDefault();
        var form = this;
        $.ajax({
            url: url,
            type: 'POST',
            data: new FormData(form),
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    window.opener.postMessage({
                        type: entityType + 'Added',
                        id: response[entityType + '_id'],
                        name: response[entityType + '_name']
                    }, '*');
                    window.close();
                } else {
                    alert('Error: ' + response.error);
                }
            },
            error: function(xhr) {
                if (xhr.status === 400) {
                    showFormErrors(xhr.responseJSON.error);
                } else {
                    alert('Error al procesar el formulario: ' + xhr.status);
                }
            }
        });
    });
}

function showFormErrors(errors) {
    $('.invalid-feedback').remove();
    $('.is-invalid').removeClass('is-invalid');
    for (let field in errors) {
        let fieldErrors = errors[field];
        let fieldElement = $(`[name="${field}"]`);
        if (fieldElement.length) {
            fieldElement.addClass('is-invalid');
            let errorHtml = '<div class="invalid-feedback d-block">';
            fieldErrors.forEach(error => {
                errorHtml += error.message + '<br>';
            });
            errorHtml += '</div>';
            fieldElement.after(errorHtml);
        }
    }
}

function openPopup(url, title, width = 800, height = 380) {
    const popup = window.open(url + `?popup=1`, title, `width=${width}, height=${height}`);
    popup.focus();
    return popup;
}

function sendAddedMessage(entityType, id, name) {
    if (window.opener) {
        window.opener.postMessage({
            type: `${entityType}Added`,
            id: id,
            name: name
        }, '*');
    }
}

function initMessageListener(callback) {
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type) {
            callback(event.data);
        }
    });
}

function initPopup(config) {
    $(document).ready(function() {
        const defaults = {
            triggerSelector: null,
            popupUrl: '',
            entityType: '',
            selectId: null,
            formSelector: 'form',
            onSuccess: null,
            width: 800,
            height: 380
        };
        const settings = {...defaults, ...config };

        if (settings.triggerSelector && settings.popupUrl) {
            $(settings.triggerSelector).on('click', function() {
                openPopup(settings.popupUrl, `Agregar ${settings.entityType}`);
            });
        }

        if (settings.selectId) {
            initMessageListener(function(data) {
                if (data.type === `${settings.entityType}Added`) {
                    const select = $(`#${settings.selectId}`);
                    const option = new Option(data.name, data.id, true, true);
                    select.append(option).trigger('change');
                }
            });
        }

    });
}

