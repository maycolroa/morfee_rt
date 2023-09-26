<template>
    <div>
        <div :class="running? 'panel panel-default card-view border loading': 'panel panel-default card-view border'">
            <div class="panel-wrapper collapse in">
                <div class="panel-body">
                    <h5>Predicción Cuentas Médicas - Innovación Analítica</h5>
                    <div class="my-4"></div>
                    <div :class="'row ' + status">
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">Id Prestador:</label>
                                <input type="number" class="form-control" v-model="prestador">
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">Plan Salud:</label>
                                <select class="form-control" v-model="plansalud">
                                    <option value=""></option>
                                    <option value="1">S</option>
                                    <option value="2">V</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">TContra:</label>
                                <select class="form-control" v-model="tcontra">
                                    <option value=""></option>
                                    <option value="1">CAP</option>
                                    <option value="2">EVE</option>
                                    <option value="3">PGP</option>
                                    <option value="4">OTR</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">Ámbito:</label>
                                <select class="form-control" v-model="ambito">
                                    <option value=""></option>
                                    <option value="1">U</option>
                                    <option value="2">A</option>
                                    <option value="3">H</option>
                                    <option value="4">D</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">FPres:</label>
                                <input type="number" class="form-control" v-model="fpres">
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">FRad:</label>
                                <input type="number" class="form-control" v-model="frad">
                            </div>
                        </div>

                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">Glosa definitiva:</label>
                                <input type="number" class="form-control" v-model="glosadefinitiva">
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">MecPago:</label>
                                <input type="number" class="form-control" v-model="mecpago">
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">Vlr. Pagado PBS:</label>
                                <input type="number" class="form-control" v-model="pbs">
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">Vlr. Pagado PAC:</label>
                                <input type="number" class="form-control" v-model="pac">
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">Vlr. Pagado PM:</label>
                                <input type="number" class="form-control" v-model="pm">
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">FPago:</label>
                                <input type="number" class="form-control" v-model="fpago">
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">Pres Max:</label>
                                <input type="number" class="form-control" v-model="pres">
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label for="" class="control-label">Covid:</label>
                                <input type="number" class="form-control" v-model="covid">
                            </div>
                        </div>
                    </div>
                    <div :class="'d-flex justify-content-center mt-4 ' + status">
                        <button class="btn btn-warning" @click="fillData">Datos de prueba</button>
                        <button class="btn btn-primary mx-2" @click="resetear">Resetear</button>
                        <button class="btn btn-success btn-icon-anim px-5" :disabled="is_valid() == false" @click="loadPredict">Predecir</button>
                    </div>
                </div>
            </div>
        </div>
        <div :class="running? 'panel panel-default card-view border': 'd-none'">
            <div class="panel-wrapper collapse in">
                <div class="panel-body">
                    <div class="text-center mb-3">
                        <div class="d-flex align-items-center">
                            <i class="fa fa-spinner fa-spin fs-2 me-2"></i>
                            <span>Generando proyección...</span>
                        </div>
                    </div>
                    <neuronas></neuronas>
                </div>
            </div>
        </div>
        <div :class="status == state.LOADED && !running? 'mt-4 d-flex justify-content-center': 'd-none'">
            <div style="min-width:350px">
                <contador-light ref="df_neu" texto="VALOR FACTURADO" pretag="$ " miles duracion="1"></contador-light>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        pathpredict: {type: String, default: ''},
        pathmodel: {type: String, default: ''},
    },
    data() {
        return {
            campos: ['prestador', 'plansalud', 'tcontra', 'ambito', 'fpres', 'frad', 'glosadefinitiva', 'mecpago', 'pbs', 'pac', 'pm', 'fpago', 'pres', 'covid'],
            prestador: '',
            plansalud: '',
            tcontra: '',
            ambito: '',
            fpres: '', 
            frad: '', 
            glosadefinitiva: '', 
            mecpago: '', 
            pbs: '', 
            pac: '', 
            pm: '', 
            fpago: '', 
            pres: '', 
            covid: '',
            resultado: '',
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            clock: null,
            seg: 0,
            running: false,
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
                this.clock = setInterval(() => {
                    this.seg++;
                    if(this.status == this.state.LOADED && this.seg > 9){
                        this.clock_down();
                    }
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
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        is_valid: function(){
            let rs = this.campos.reduce((ac, elm) => ac? !this.isEmpty(this[elm]): ac, true)
            return rs;
        },
        loadPredict: function(){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                this.clock_up();
                let pam = new FormData();
                this.campos.forEach(elm => {
                    pam.append(elm, this[elm]);
                });
                axios.post(this.pathpredict, pam).then(res => {
                    console.log('Listo');
                    console.log(res.data);
                    this.resultado = res.data.resultado;
                    this.$refs.df_neu.setValor(this.resultado);
                    this.status = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
        fillData: function(){
            this.status = this.state.INI;
            this.resultado = '';
            this.prestador = '860035992';
            this.plansalud = '2';
            this.tcontra = '2';
            this.ambito = '1';
            this.fpres = '20211027';
            this.frad = '20211116';
            this.glosadefinitiva = '0';
            this.mecpago = '1';
            this.pbs = '528';
            this.pac = '0';
            this.pm = '0';
            this.fpago = '20211130';
            this.pres = '0';
            this.covid = '0';
        }, 
        resetear: function(){
            this.status = this.state.INI;
            this.resultado = '';
            this.campos.forEach(elm => this[elm] = '');
        }        
    },
    mounted() {
        /*
        const plugin = document.createElement('script');
        plugin.setAttribute("src", "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest");
        plugin.async = true;
        plugin.onload = () => this.loadModel();
        document.head.appendChild(plugin);
        */
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
	.loading {opacity: .45; pointer-events: none; user-select: none}
    label.control-label {letter-spacing: 2px}
</style>
