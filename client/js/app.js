let id = false;
let email = false;
const list_email = [];

const SERVER_URL = 'http://127.0.0.1:8000/api/v1/email';


const getMail = function(user_id, email_id) {
    let htmlBody = '';
    $.ajax({
        type: 'GET',
        async: false,
        url: SERVER_URL + '/get/mail',
        data: { user_id, email_id }
    }).done(function(data) {
        htmlBody = data.htmlBody;
    }).fail(function() {
        alert('Ошибка сервера');
    });

    return htmlBody;
}


const getMails = function(user_id) {
    $.ajax({
        type: 'GET',
        url: SERVER_URL + '/get/all',
        data: { user_id }
    }).done(function(data) {
        console.log(data)
        if (data.length === 0) {
            alert('Почтовый ящик пуст');
            return;
        }

        $('.mail_list').html('');

        data.forEach(element => {
            const content = getMail(user_id, element.id)
            console.log('Content: ',content)
            $('.mail_list').append(`
            <div class="mail_item" data-id="${element.id}">
                <div class="mail_item-wrapper">
                    <div class="mail_item-info">
                        <p>От кого: ${element.from}</p>
                        <p>Тема: ${element.subject}</p>
                        <p>Когда: ${element.date}</p>
                    </div>

                    <div class="mail_item-actions" style="display: none;">
                        <button class="button">Просмотреть</button>
                    </div>
                </div>


                <div class="mail_item-content">
                    ${content}
                </div>
            </div>`)



            /* */
        });

        $('.mail_list').show();

        // id = data.id;
        // email = data.email

        // $('[data-current-id]').text(id);
        // $('[data-current-email]').text(email);

        // $('.start_display').hide();
        // $('.mail_display').show();

        
    }).fail(function() {
        alert('Ошибка сервера');
    });
}

const register = function() {
    $.ajax({
        type: 'POST',
        url: SERVER_URL + '/create',
    }).done(function(data) {
        console.log(data)

        id = data.id;
        email = data.email

        $('[data-current-id]').text(id);
        $('[data-current-email]').text(email);

        $('.start_display').hide();
        $('.mail_display').show();

        getMails(data.id)
    }).fail(function() {
        alert('Ошибка сервера');
    });
}

const login = function(user_id) {
    $.ajax({
        type: 'GET',
        url: SERVER_URL + '/create',
        data: { user_id }
    }).done(function(data) {
        console.log(data)

        id = data.id;
        email = data.email

        $('[data-current-id]').text(id);
        $('[data-current-email]').text(email);

        $('.start_display').hide();
        $('.mail_display').show();

        getMails(data.id)
    }).fail(function() {
        alert('Ошибка сервера');
    });
}

$( document ).ready(function() {
    
    $('[data-get-mail]').on('click', function() {
        getMails(id)
    })

});

$( document ).ready(function() {
    
    $('[data-register]').on('click', function() {
        register()
    })
    
    $('[data-login]').on('click', function() {
        let input = $('[data-login-input]').val()
        if (input.length === 0) {
            alert('Укажите ID')
            return
        }
        login(input)
    })


});

