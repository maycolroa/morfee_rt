<template>
    <div> 
        <div class="input-group me-4">         
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
            mes :['Enero','Febrero','Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    watch: {
        periodo: function(val){
            if(this.status == this.state.LOADED){
                this.$eventBus.$emit('time-select', {'periodo': this.periodo});
            }
        },
    },
    
    methods: {
        reloadPeriodos: function(){
            this.CargarPeriodos();
        },

        timeSelect: function(per){
            this.periodo = per;
        },

        CargarPeriodos : function(){
            if(this.status != this.state.LOADING){
                var pam = new FormData();
                pam.append('collections', this.collections);
                this.status = this.state.LOADING;
                axios.post(root_path + "consulta/consultas_view", pam).then(res => {
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

                    this.periodos = Object.values(tmp).sort((a, b) => b.anio - a.anio);
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
       this.CargarPeriodos();
    }
}
</script>
<style scoped>
.slot {cursor:pointer}
.slot.active, .slot:hover {background:#F0C54144}
.slot + .slot {border-top:1px solid #DEDEDE}
.bg-super {background: #F0C541 !important; color:#FFF; font-weight: bold; font-family: Arial; letter-spacing: 1px}
</style>
