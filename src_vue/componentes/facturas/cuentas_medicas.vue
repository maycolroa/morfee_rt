<template>
    <div>
        <div class="d-flex justify-content-between mt-2 mb-3">
            <div>
                <h5 class="txt-dark mb-0">CUENTAS MÉDICAS</h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de reservas técnicas</div>
            </div>
            <div class="btn-group">
                <button :class="display == 'barra'? 'btn btn-success': 'btn btn-default'" @click="display = 'barra'"><i class="fa fa-bar-chart"></i></button>
                <button :class="display == 'line'? 'btn btn-success': 'btn btn-default'" @click="display = 'line'"><i class="fa fa-line-chart"></i></button>
            </div>
        </div>
        <div class="mt-2 mb-3">
        </div>
        <div class="panel panel-default card-view border">
            <div class="panel-heading">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="panel-title txt-dark text-bold text-upper mb-0" v-if="display == 'barra'">{{ titles[campo] }}<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                        <h6 class="panel-title txt-dark text-bold text-upper mb-0" v-else>COMPARATIVO ENTRE VALOR FACTURADO Y GLOSADO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                        <div class="txt-dark">FAMISANAR</div>
                    </div>
                    <div>
                        <a href="javascript:void(0)" class="me-2" click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                        <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                    </div>
                </div>
            </div>
            <div class="panel-wrapper collapse in">
                <div :class="'panel-body ' + status">
                    <div :class="display == 'barra'? '': 'd-none'">
                        <amchart-barra ref="gp_bar" paleta="#337CCF" redondeado etiquetas grilla="0" tooltip cursor sin_valores puntos></amchart-barra>
                        <div class="d-flex justify-content-center mt-2">
                            <div class="btn-group btn-group-sm">
                                <button :class="getCss('facturado')" @click="setCampo('facturado')">Facturado</button>
                                <button :class="getCss('glosado')" @click="setCampo('glosado')">Glosado</button>
                                <button :class="getCss('relacion')" @click="setCampo('relacion')">Relación %</button>
                            </div>
                        </div>
                    </div>
                    <div :class="display == 'line'? '': 'd-none'">
                        <amchart-linea 
                            ref="gp_line" 
                            altura="400" 
                            sin_valores
                            grosor="1"
                            leyenda="right"
                            campo_valor="Glosado,Facturado" 
                            paleta="#179D82,#337CCF"
                            tooltip cursor>
                        </amchart-linea>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        pathdata: {type: String, default: ''},
    },
    data() {
        return {
            display: 'barra', // barra | line
            titles: {'facturado': 'VALORES FACTURADOS POR PERIODOS', 'glosado': 'GLOSAS POR PERIODO', 'relacion': 'PORCENTAJE DE GLOSAS EN RELACIÓN CON VALORES FACTURADOS'},
            campo: 'facturado',     // facturado | glosado | relacion
			datos: [],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        getCss: function(arg){
            return (arg == this.campo)? 'btn btn-success px-4': 'btn btn-default px-4';
        },
        getPercent: function(glo, fac){
            let num = glo / fac;
            let rs = (num % 1)? parseFloat(num.toFixed(2)): num;
            console.log(rs, rs * 100);
            return rs * 100;
        },
        setCampo: function(arg){
            this.campo = arg;
            let cls = {'facturado': '#337CCF', 'glosado': '#179D82', 'relacion': '#9A60B4'};
            let tm = [];
            if(['facturado', 'glosado'].includes(this.campo)){
                tm = this.datos.map(elm => {
                    return {'categoria': elm._id, 'valor': elm['v_' + this.campo]};
                });
            }else{
                tm = this.datos.map(elm => {
                    return {'categoria': elm._id, 'valor': this.getPercent(elm.v_glosado, elm.v_facturado)};
                });
            }
            this.$refs.gp_bar.setColor(cls[arg]);
            this.$refs.gp_bar.setDatos(tm);
        },
        loadData: function(){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                axios.post(this.pathdata).then(res => {
                    this.datos = res.data;
                    console.log('Listo hermano!');
                    console.log(this.datos);
                    this.setCampo(this.campo);
                    this.$refs.gp_line.setDatos(this.datos.map(elm => {
                        return {'categoria': elm._id, 'Glosado': elm.v_glosado, 'Facturado': elm.v_facturado}
                    }));
                    this.status = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        }
    },
    mounted() {
        this.loadData();
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
	.loading {opacity: .45; pointer-events: none; user-select: none}
</style>
