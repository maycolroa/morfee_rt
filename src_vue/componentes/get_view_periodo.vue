<template>
    <div> 
        <div class="input-group me-4">
            <div class="input-group-addon" style="background:#FFF">
                <a href="javascript:void(0)" @click="openDetails"><i class="fa fa-calendar fs-5"></i></a>
            </div>
            <select v-model="periodo" class="form-control">
                <option value="">{{ status == state.LOADING? 'Cargando datos...': '' }}</option>
                <optgroup :label="elm.anio == 0? 'Sin periodo': (elm.anio == -1)? 'Todos los registros': elm.anio" v-for="(elm, i) in periodos" :key="i">
                    <option v-for="(mes, m) in elm.meses" :key="m" :value="mes">{{ mes.tx }}</option>
                </optgroup>
            </select>
            <div class="input-group-btn">
                <button class="btn btn-success" @click="reloadPeriodos" :disabled="status == state.LOADING"><i :class="status == state.LOADING? 'fa fa-refresh fa-spin': 'fa fa-refresh'"></i></button>
            </div>
        </div>

        <div id="lc_modal_view" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" style="display: none;">
            <div class="modal-dialog modal-lgx">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                        <h5 class="modal-title" id="myLargeModalLabel">DETALLES DE LA VISTA</h5>
                    </div>
                    <div :class="'modal-body ' + status">
                        <h5>{{ getCollection() }}</h5>
                    </div><!-- End modal-body -->
                    <div :class="'modal-footer ' + status">
                        <button type="button" class="btn btn-danger text-left" data-dismiss="modal">Cancelar</button>
                        <!-- <button type="button" class="btn btn-success">Guardar cambios</button> -->
                    </div>
                </div><!-- /.modal-content -->
            </div><!-- /.modal-dialog -->
        </div>        
        <!-- End modal -->
    </div>
</template>
<script>
export default {
    props : {
        collections: {type: String, default: 'retec_contratos'},
        storage: {type: String, default: ''},
    },
    data() {
        return {
            meses: {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'},
            fuentes: [],    // {'fuente': 'str', 'alias': 'str', 'min': 'str', 'data': [], 'loaded': false}
            sch_match: {},
            periodos: [],
            periodos_flat: {},
            periodo: '',
            post_refresh: false,
            prefijo: '',
            zero: null,
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
        }
    },
    watch: {
        periodo: function(val){
            if(this.status == this.state.LOADED){
                if(this.post_refresh){
                    this.post_refresh = false;
                    this.$eventBus.$emit('time-refresh', {'periodo': this.periodo.ym, 'info': this.periodo});
                }else{
                    this.$eventBus.$emit('time-select', {'periodo': this.periodo.ym, 'info': this.periodo});
                }
            }
        },
    },
    methods: {
        isEmpty: function(arg){
            return ['', undefined, null].includes(arg);
        },
        saveData: function(alias, data){
            console.log('Into saveData', alias, data);
            localStorage.setItem(alias, JSON.stringify(data));
        },
        openDetails: function(){
            $('#lc_modal_view').modal('show');
        },
        reloadPeriodos: function(){
            this.post_refresh = true;
            this.fuentes.forEach(fuente => {
                localStorage.removeItem(fuente.alias);
            });
            this.getStoreData();
        },
        timeSelect: function(per){
            this.periodo = per;
        },
        getCollection: function(){
            return this.collections.replace('retec_', '').toUpperCase();
        },
        getStoreData: function(){
            if(this.status != this.state.LOADING){
                // this.timeSelect('');
                this.status = this.state.LOADING;
                this.periodos = [];
                this.fuentes.forEach(sch => {
                    // {'fuente': 'str', 'alias': 'str', 'min': 'str', 'data': [], 'loaded': false}
                    sch.data = [];
                    sch.loaded = false;
                    let raw = localStorage.getItem(sch.alias);
                    if(raw != null){
                        let arr = JSON.parse(raw);
                        if(Array.isArray(arr)){
                            arr.forEach(elm => {
                                sch.data.push(elm);
                            });
                            sch.loaded = true;
                        }else{
                            this.loadView(sch.fuente, sch.alias);
                        }
                    }else{
                        this.loadView(sch.fuente, sch.alias);
                    }
                });
                this.buildOptions();
            }
        },
        loadView: function(collec, alias){
            console.log('load View', collec);
            this.fuentes.find(elm => {
                let bool = elm.fuente == collec;
                if(bool){
                    if(elm.loaded == false){
                        let pam = new FormData();
                        pam.append('collections', collec);
                        axios.post(root_path + "consulta/consultas_view", pam).then(res => {
                            let rs = res.data.map(arg => this.isEmpty(arg._id)? null: arg._id);
                            console.log('rs', rs);
                            this.saveData(alias, rs);
                            elm.data = [...rs];
                            elm.loaded = true;
                            this.buildOptions();
                        }).catch(err => {
                            console.log(err);
                        });
                    }
                }
                return bool;
            });
        },
        buildOptions: function(){
            console.log('Run build options...');
            console.log(this.fuentes);
            let lds = this.fuentes.reduce((ac, obj) => ac? obj.loaded: ac, true);
            if(lds){
                let pre = {};
                this.fuentes.forEach(fuente => {
                    fuente.data.forEach(elm => {
                        if(!this.isEmpty(elm)){
                            if(pre[elm] == undefined){
                                let anio = parseInt(elm.toString().slice(0, 4));
                                let mes = elm.toString().slice(-2);
                                pre[elm] = {'num': elm, 'ym': elm, 'y': anio, 'm': mes, 'tx': this.meses[mes], 'match': this.sch_match};
                            }
                            pre[elm].match[fuente.min] = true;
                        }
                    });
                });
                let tmp = {};
                Object.values(pre).forEach(elm => {
                    if(tmp[elm.y] == undefined){
                        tmp[elm.y] = {'anio': elm.y, 'meses': []}
                    }
                    tmp[elm.y].meses.push({...elm});
                });
                this.periodos = Object.values(tmp).sort((a, b) => b.y - a.y);
                if(this.periodos.length > 0){
                    this.timeSelect(this.periodos[0].meses[0]);
                }
                this.status = this.state.LOADED;
            }
            // if(this.zero != null && this.fuentes.length == 1) this.periodos.push(this.zero);
        },
    },
    mounted() {
        this.prefijo = this.isEmpty(this.storage)? '': this.storage + '_';
        this.collections.split(',').forEach(elm => {
            let short = elm.replace('retec_', '').slice(0, 3);
            this.sch_match[short] = false;
            this.fuentes.push({
                'fuente': elm,
                'alias': this.prefijo + elm,
                'min': short,
                'data': [],
                'loaded': false
            });
        });
        this.getStoreData();
    }
}
</script>
<style scoped>
.slot {cursor:pointer}
.slot.active, .slot:hover {background:#F0C54144}
.slot + .slot {border-top:1px solid #DEDEDE}
.bg-super {background: #F0C541 !important; color:#FFF; font-weight: bold; font-family: Arial; letter-spacing: 1px}
.df-option {background:#E2E2E2; border-top:1px solid #CCC; padding-top:7px; padding-bottom:7px; letter-spacing: 1px;}
</style>
