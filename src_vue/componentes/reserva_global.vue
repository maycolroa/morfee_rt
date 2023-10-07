<template>
    <div>
        <div class="d-flex justify-content-end mb-4">
            <get-view-periodo :class="status" sinmargen collections="retec_autorizaciones"></get-view-periodo>
        </div>
        <div class="row">
            <div class="col-sm-6">
                <contador-light ref="cnt_aut" class="border" texto="TOTAL RESERVA CONOCIDA NO LIQUIDADA" valor="0" duracion="1" miles></contador-light>
            </div>
            <div class="col-sm-6">
                <contador-light ref="cnt_fac" class="border" texto="TOTAL RESERVA CONOCIDA LIQUIDADA" valor="0" duracion="1" miles></contador-light>
            </div>
            <div class="col-sm-6">
                <contador-light ref="cnt_1" class="border" texto="TOTAL RESERVA NO CONOCIDA - IBNR (CHAIN LADDER)" valor="0" duracion="1" miles></contador-light>
            </div>
            <div class="col-sm-6">
                <contador-light ref="cnt_all" class="border" texto="TOTAL RESERVA TÉCNICA" valor="0" duracion="1" miles></contador-light>
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
            sum_all: 0,
            sum_aut: 0,
            sum_fac: 0,
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
        loadAuto: function(){
            this.sum_aut = 0;
            let caut = 'raw_aut_dat' + this.periodo;
            let pam = new FormData();
            pam.append('consulta', caut);
            axios.post(root_path + 'consulta/load', pam).then(res => {
                console.log('listo');
                console.log(res.data);
                let raw = res.data.contenido;
                if(raw.length > 0){
                    let rawData = raw[0];
                    if(rawData['facet_vbs'].length > 0){
                        this.sum_aut += rawData['facet_vbs'][0].n;
                    }
                    if(rawData['facet_vpm'].length > 0){
                        this.sum_aut += rawData['facet_vpm'][0].n;
                    }
                    if(rawData['facet_vac'].length > 0){
                        this.sum_aut += rawData['facet_vac'][0].n;
                    }
                    this.sum_aut > 0? this.$refs.cnt_aut.setValor(Math.round(this.sum_aut)): this.$refs.cnt_aut.setValor('');
                    this.sum_all += this.sum_aut;
                    this.$refs.cnt_all.setValor(Math.round(this.sum_all));
                }
            }).catch(err => {
                console.log(err);
                this.$refs.cnt_aut.setValor('');
            });
        },
        loadFacturas: function(){
            this.sum_fac = 0;
            let cfac = 'raw_facet_fac' + this.periodo;
            let pam = new FormData();
            pam.append('consulta', cfac);
            axios.post(root_path + 'consulta/load', pam).then(res => {
                console.log('listo rawpalinga');
                let raw = res.data.contenido;
                console.log(raw);
                if(raw.length > 0){
                    let cores = raw[0].cores[0];
                    this.sum_fac = cores.sum_vbs + cores.sum_vpm + cores.sum_vac;
                    this.sum_all += this.sum_fac;
                    this.$refs.cnt_fac.setValor(Math.round(this.sum_fac));
                    this.$refs.cnt_all.setValor(Math.round(this.sum_all));
                }else{
                    this.$refs.cnt_fac.setValor('');
                }
            }).catch(err => {
                console.log(err);
                this.$refs.cnt_fac.setValor('');
            });
        },
        listen: function(){
            this.$eventBus.$on('time-select', obj => {
                console.log('time-select dispatch');
                this.periodo = obj.periodo;
                console.log(this.periodo);
                this.sum_all = 0;
                this.loadAuto();
                this.loadFacturas();
            });
            this.$eventBus.$on('time-refresh', obj => {
                console.log('time-refresh dispatch');
                this.periodo = obj.periodo;
                console.log(this.periodo);
                this.sum_all = 0;
                this.loadAuto();
                this.loadFacturas();
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
