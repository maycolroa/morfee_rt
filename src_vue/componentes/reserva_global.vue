<template>
    <div>
        <div class="d-flex justify-content-end mb-4">
            <get-view-periodo :class="status" sinmargen collections="retec_autorizaciones"></get-view-periodo>
        </div>
        <div class="row">
            <div class="col-sm-6">
                <contador-light ref="cnt_1" class="border" texto="TOTAL RESERVA CONOCIDA NO LIQUIDADA" valor="0" duracion="1" miles></contador-light>
            </div>
            <div class="col-sm-6">
                <contador-light ref="cnt_1" class="border" texto="TOTAL RESERVA CONOCIDA LIQUIDADA" valor="0" duracion="1" miles></contador-light>
            </div>
            <div class="col-sm-6">
                <contador-light ref="cnt_1" class="border" texto="TOTAL RESERVA NO CONOCIDA - IBNR (CHAIN LADDER)" valor="0" duracion="1" miles></contador-light>
            </div>
            <div class="col-sm-6">
                <contador-light ref="cnt_1" class="border" texto="TOTAL RESERVA TÉCNICA" valor="0" duracion="1" miles></contador-light>
            </div>
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
            periodo: '',
			datos: [],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        loadData: function(){
            let pam = {};
            this.status = this.state.LOADING;
            axios.post('', pam).then(res => {
                this.datos = res.data;
                this.status = this.state.LOADED;
            }).catch(err => {
                this.status = this.state.FAILED;
                console.log(err);
            });
        },
        loadConsulta: function(){
            let caut = 'raw_aut_ctr' + this.periodo;
            let pam = new FormData();
            pam.append('consulta', caut);
            axios.post(root_path + 'consulta/load', pam).then(res => {
                console.log('listo');
                console.log(res.data);
            }).catch(err => {
                console.log(err);
            });
        },
        listen: function(){
            this.$eventBus.$on('time-select', obj => {
                console.log('time-select dispatch');
                this.periodo = obj.periodo;
                console.log(this.periodo);
                this.loadConsulta();
            });
            this.$eventBus.$on('time-refresh', obj => {
                console.log('time-refresh dispatch');
                this.periodo = obj.periodo;
                console.log(this.periodo);
                this.loadConsulta();
            });
        }
    },
    mounted() {
        this.listen();
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
	.loading {opacity: .45; pointer-events: none; user-select: none}
</style>
