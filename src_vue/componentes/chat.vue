<template>
    <div>
        <div class="border p-2 mb-4" style="background:#F1F1F1">
            <div class="form-group">
                <label for="" class="control-label">Escribe un mensaje:</label>
                <input type="text" class="form-control" v-model="f_text" @keypress.enter="enviar" autofocus>
            </div>
        </div>
        <div class="border p-4">
            <div class="msn" v-for="(elm, i) in mensajes" :key="i">
                {{ elm }}
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        pathself: {type: String, default: ''}
    },
    data() {
        return {
            f_text: '',
            ruta: '',
            chatSocket: null,
            mensajes: []
        }
    },
    methods: {
        inicio: function(){
            console.log('Función inicio ejecutándose!');
            this.ruta = `ws://${window.location.host}/ws/socket-server/`;
            this.chatSocket = new WebSocket(this.ruta);
            this.chatSocket.onmessage = (e) => {
                let data = JSON.parse(e.data);
                console.log('Data: ', data);
                if(data.type === 'chat'){
                    this.mensajes.push(data.message);
                }
            };
        },
        enviar: function(e){
            console.log('Se envió!');
            this.chatSocket.send(JSON.stringify( {'message': this.f_text} ));
            this.f_text = '';
        }
    },
    mounted() {
        this.inicio();
    }
}
</script>
