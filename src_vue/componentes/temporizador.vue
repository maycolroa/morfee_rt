<template>
    <div v-if="running">
        <div class="input-group df-kan">
            <div class="input-group-addon df-kan" style="background:#FFF">
                <i class="icon-clock text-bold fs-4"></i>
            </div>
            <input type="text" class="form-control df-kan df-clock" :value="clock_human">
        </div>
    </div>
</template>
<script>
export default {
    props: {
        ejemplo: {type: String, default: ''},
    },
    data() {
        return {
            pathsearch: root_path + 'consulta/dash/consulta/auto',
            clock: null,
            clock_human: '',
            seg: 0,
            keycode: '',
            runsearch: false,
            running: false,
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        clock_up: function(){
            if(this.running == false){
                this.running = true;
                if(this.clock != null){
                    clearInterval(this.clock);
                    this.clock = null;
                }
                this.seg = 0;
                this.getTime();
                this.clock = setInterval(() => {
                    this.seg++;
                    this.getTime();
                }, 1000);
            }
        },
        clock_down: function(){
            this.running = false;
            if(this.clock != null){
                clearInterval(this.clock);
            }
            this.clock = null;
            this.seg = 0;
        },
        getTime: function(){
            let mn = Math.floor(this.seg / 60).toString().padStart(2, '0');
            let rs = (this.seg % 60).toString().padStart(2, '0');
            this.clock_human = `${mn}:${rs} segundos`;
        },
        dispatchQuery: function(consulta, writepath, params, fun, force=false){
            console.log('This is Sparta!');
            this.asyncRequest(consulta, writepath, params, fun, true, '', force);
        },
        asyncRequest: function(consulta, writepath, params, fun=null, first=true, kcode='', force=false){
            let initial = first;
            if(this.runsearch == false || first == false){
                if(this.runsearch == false && first){
                    this.runsearch = true;
                    this.status = this.state.LOADING;
                    this.clock_up();
                    console.log('Se inicia proceso de asyncio!');
                }
                if(force === true){
                    this.keycode = generatorKey();
                    let param = new FormData();
                    param.append('clave', this.keycode);
                    Object.entries(params).forEach(par => param.append(par[0], par[1]));
                    customPostBlind(writepath, param).then(arg => {console.log('Return async write request! (CustomPost)')}).catch(err => {console.log(err)});
                    setTimeout(() => this.asyncRequest(consulta, writepath, {}, fun, false, this.keycode), 4000);
                    console.log('Se mandó a crear la consulta mongodb por la fuerza, con la clave: ' + this.keycode);
                }else{
                    console.log('async request in else block!');
                    let pam = new FormData();
                    pam.append('clave', kcode);
                    pam.append('consulta', consulta);
                    axios.post(this.pathsearch, pam).then(res => {
                        if(res.data.estado == 'void'){
                            if(initial){
                                this.keycode = generatorKey();
                                let param = new FormData();
                                param.append('clave', this.keycode);
                                Object.entries(params).forEach(par => param.append(par[0], par[1]));
                                customPostBlind(writepath, param).then(arg => {console.log('Return async write request! (CustomPost)')}).catch(err => {console.log(err)});
                                setTimeout(() => this.asyncRequest(consulta, writepath, {}, fun, false, this.keycode), 4000);
                                console.log('Se mandó a crear la consulta mongodb porque se encontró void, con la clave: ' + this.keycode);
                            }
                        }else if(res.data.estado == 'close'){
                            console.log(`Consulta finalizada, con clave: '${kcode}'`);
                            console.log(res.data);
                            this.runsearch = false;
                            this.status = this.state.LOADED;
                            this.clock_down();
                            if(fun != null){
                                fun(res.data.contenido);
                            }
                            this.$eventBus.$emit('search-finish', {'status': 'success', 'consulta': consulta, 'contenido': res.data.contenido});
                        }else if(res.data.estado == 'failed'){
                            console.log(`La creación de consulta mongo falló, con clave: '${kcode}'`);
                            this.runsearch = false;
                            this.status = this.state.FAILED;
                            this.clock_down();
                        }else{
                            console.log(`El estado de la consulta es: '${res.data.estado}', se verifica dentro de 4 segundos!`);
                            setTimeout(() => this.asyncRequest(consulta, writepath, {}, fun, false, kcode), 4000);
                        }
                    }).catch(err => {
                        console.log(err);
                        console.log(`asyncio falló, se verifica dentro de 4 segundos!`);
                        setTimeout(() => this.asyncRequest(consulta, writepath, {}, fun, false, kcode), 4000);
                    });
                }
            }else{
                console.log('Se desechó la invocación de asyncio, porque ya hay un hilo ejecutándose!');
            }
        },

    },
    mounted() {
        // this.clock_up();
    }
}
</script>
<style scoped>
	.input-group.df-kan {pointer-events: none; user-select: none}
    .df-clock {color:#000; letter-spacing: 1px; font-family: Verdana}
</style>
