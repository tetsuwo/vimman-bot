Vue.component(
    'informations-create',
    getPresetCreateComponent(
        'informations-create',
        {
            sendTo   : '/api/informations',
            afterDone: '#/informations',
            afterFail: null,
            sendData : {
                state   : 'information[state]',
                content : 'information[content]'
            }
        }
    )
);
