<template>
    <div> 
        <div class="input-group me-4">
            <div class="input-group-addon" style="background:#FFF">
                <a href="javascript:void(0)" @click="openDetails"><i class="fa fa-calendar fs-5"></i></a>
            </div>
            <select v-model="periodo" class="form-control">
                <option value="">{{ status == state.LOADING? 'Cargando datos...': '' }}</option>
                <optgroup :label="elm.anio == 0? 'Sin periodo': (elm.anio == -1)? 'Todos los registros': elm.anio" v-for="(elm, i) in periodos" :key="i">
                    <option v-for="(mes, m) in elm.meses" :key="m" :value="mes.ym">{{ mes.tx }}</option>
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
    },
    data() {
        return {
            meses: {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'},
            periodos: [],
            periodo: '',
            post_refresh: false,
            status: 'ini',
            state: {'INI': 'ini', 'LOA,}DING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            storage_periodo : ''
        }
    },
    watch: {
        periodo: function(val){
            if(this.status == this.state.LOADED){
                if(this.post_refresh){
                    this.post_refresh = false;
                    this.$eventBus.$emit('time-refresh', {'periodo': this.periodo});
                }else{
                    this.$eventBus.$emit('time-select', {'periodo': this.periodo});
                }
            }
        },
    },
    methods: {
        addSchema: function(data){
            localStorage.setItem(this.storage_periodo, JSON.stringify(data));
        },
        openDetails: function(){
            $('#lc_modal_view').modal('show');
        },
        reloadPeriodos: function(){
            this.post_refresh = true;
            this.cargarPeriodos();
        },
        timeSelect: function(per){
            this.periodo = per;
        },
        getCollection: function(){
            return this.collections.replace('retec_', '').toUpperCase();
        },
        getPeriodoHistory: function(){
            var tmpp = localStorage.getItem(this.storage_periodo);
            if(tmpp == null){
                this.cargarPeriodos();
            }else{
                this.timeSelect('');
                let tmp = {};
                let zero = null;
                JSON.parse(tmpp).forEach(elm => {
                    if(elm._id == null){
                        zero = {'anio': 0, 'meses': [{'ym': 0, 'mm': 0, 'tx': 'Sin periodo definido'}]};
                    }else{
                        var anio = parseInt(elm._id.toString().slice(0, 4));
                        if(tmp[anio] == undefined){
                            tmp[anio] = {'anio': anio, 'meses': []}
                        }
                        var mes = elm._id.toString().slice(-2);
                        tmp[anio].meses.push({'ym': elm._id, 'mm': mes, 'tx': this.meses[mes]});
                    }
                });
                
                this.periodos =Object.values(tmp).sort((a, b) => b.anio - a.anio);
                if(zero != null) this.periodos.push(zero);
                if(this.periodos.length > 1) this.periodos.push({'anio': -1, 'meses': [{'ym': -1, 'mm': 0, 'tx': 'Total registros'}]});
                this.status = this.state.LOADED;
                if(this.periodos.length > 0){
                    this.timeSelect(this.periodos[0].meses[0].ym);
                }
            }
        },
        cargarPeriodos : function(){
            localStorage.removeItem(this.storage_periodo);
            if(this.status != this.state.LOADING){
                var pam = new FormData();
                pam.append('collections', this.collections);
                this.status = this.state.LOADING;
                this.timeSelect('');
                axios.post(root_path + "consulta/consultas_view", pam).then(res => {
                    this.addSchema(res.data);
                    let tmp = {};
                    let zero = null;
                    res.data.forEach(elm => {
                        if(elm._id == null){
                            zero = {'anio': 0, 'meses': [{'ym': 0, 'mm': 0, 'tx': 'Sin periodo definido'}]};
                        }else{
                            var anio = parseInt(elm._id.toString().slice(0, 4));
                            if(tmp[anio] == undefined){
                                tmp[anio] = {'anio': anio, 'meses': []}
                            }
                            var mes = elm._id.toString().slice(-2);
                            tmp[anio].meses.push({'ym': elm._id, 'mm': mes, 'tx': this.meses[mes]});
                        }
                    });
                  
                    this.periodos =Object.values(tmp).sort((a, b) => b.anio - a.anio);
                    if(zero != null) this.periodos.push(zero);
                    if(this.periodos.length > 1) this.periodos.push({'anio': -1, 'meses': [{'ym': -1, 'mm': 0, 'tx': 'Total registros'}]});
                    this.status = this.state.LOADED;
                    if(this.periodos.length > 0){
                        this.timeSelect(this.periodos[0].meses[0].ym);
                    }
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
    },
    mounted() {
       this.storage_periodo = 'time_'+this.collections.split('_')[1];
      // this.cargarPeriodos();
       this.getPeriodoHistory();
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
