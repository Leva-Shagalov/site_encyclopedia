const buttonConfirm = document.querySelector('#button-confirm');


buttonConfirm.addEventListener('click', function(event){
        const answer = confirm('Вы действительно желате удалить свой аккаунт?');

        if (!answer){
            event.preventDefault();
        } else {
            const answer2 = confirm('Вы точно не ошиблись? Данные будут безвозратно потеряны!');

            if (!answer2) {
                event.preventDefault()
            }
        }
})