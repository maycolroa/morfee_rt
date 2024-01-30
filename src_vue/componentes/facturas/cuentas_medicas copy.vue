<template>
    <div>
        <div class="d-flex justify-content-between mt-2 mb-3">
            <div>
                <h5 class="txt-dark mb-0">CUENTAS MÉDICAS</h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de reservas técnicas</div>
            </div>
            <div class="d-flex">
                <temporizador ref="timecop"></temporizador>
                <button :class="'btn btn-success ' + status" @click="exeQuery(true)"><i class="fa fa-refresh"></i></button>
            </div>
        </div>
        <div :class="'d-flex justify-content-between mb-4 df-options ' + status">
            <a :class="section == elm.code? 'flex-fill bg-target': 'flex-fill bg-custom'" href="javascript:void(0)" v-for="(elm, i) in opt" :key="i" @click="setSection(elm.code)">
                <div class="d-flex align-items-center">
                    <span class="lc-icon d-flex align-items-center justify-content-center me-2"><i :class="section == elm.code? 'fa fa-folder-open-o': 'fa fa-folder-o'"></i></span>
                    <span>{{ elm.tx }}</span>
                </div>
            </a>
        </div>
        <div v-if="status == state.LOADING">
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="d-flex align-items-center" style="color:#000">
                            <i class="fa fa-spinner fa-spin me-2 fs-3"></i>
                            <span>Cargando datos...</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div :class="status == state.LOADING? 'd-none': ''">
            <div class="row">
                <div class="col-sm-6">
                    <div class="row">
                        <div class="col-sm-5">
                            <contador-light ref="c_per" texto="Periodos FRAD" valor="0" duracion="1" icono="fa fa-calendar"></contador-light>
                        </div>
                        <div class="col-sm-7">
                            <contador-light ref="c_fac" pretag="$ " texto="Valor facturado" valor="0" duracion="1" icono="fa fa-line-chart"></contador-light>
                        </div>
                    </div>
                </div>
                <div class="col-sm-6">
                    <div class="row">
                        <div class="col-sm-7">
                            <contador-light ref="c_glo" pretag="$ " texto="Valor glosado" valor="0" duracion="1" icono="fa fa-line-chart"></contador-light>
                        </div>
                        <div class="col-sm-5">
                            <contador-light ref="c_percent" texto="% de glosa" valor="0" duracion="1" icono="fa fa-percent"></contador-light>
                        </div>
                    </div>
                </div>
            </div>
            <div :class="section == 'vertical'? '': 'd-none'">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">FACTURADO vs GLOSADO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                <div class="txt-dark">CAPITAL SALUD</div>
                            </div>
                            <div>
                                <a href="javascript:void(0)" class="me-2" click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                            </div>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div :class="'panel-body ' + status">
                            <amchart-barra-two 
                            ref="gp_bi"
                            campo_valor="Glosado:Glosado,Facturado:Facturado" 
                            paleta="#F31559,#337CCF"
                            unidad="80" 
                            tooltip
                            redondeado
                            pretag="$ "
                            cursor></amchart-barra-two>
                        </div>
                    </div>
                </div><!-- End panel -->
            </div>
            <div :class="section == 'line-1'? '': 'd-none'">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">FACTURADO vs GLOSADO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                <div class="txt-dark">CAPITAL SALUD</div>
                            </div>
                            <div>
                                <a href="javascript:void(0)" class="me-2" click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                            </div>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <amchart-linea 
                                ref="gp_line" 
                                altura="450" 
                                grosor="3"
                                suave
                                puntos
                                grilla=".2"
                                tooltip
                                cursor
                                enmarcado
                                rotar
                                leyenda="bottom"
                                campo_valor="Glosado,Facturado" 
                                paleta="#A367DC,#67B7DC"
                            ></amchart-linea>
                        </div>
                    </div>
                </div><!-- End panel -->
            </div>
            <div :class="section == 'line-2'? '': 'd-none'">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">VALORES PAGADOS<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                <div class="txt-dark">CAPITAL SALUD</div>
                            </div>
                            <div>
                                <a href="javascript:void(0)" class="me-2" click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                            </div>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <amchart-linea 
                                ref="gp_pag" 
                                altura="450"
                                min="0"
                                enmarcado
                                grosor="2"
                                grilla=".2"
                                leyenda="bottom"
                                rotar
                                campo_valor="PBS,PM,PAC" 
                                paleta="#179D82,#337CCF,#FC8452"
                                tooltip cursor>
                            </amchart-linea>
                        </div>
                    </div>
                </div><!-- End panel -->
            </div>
            <div :class="section == 'line-3'? '': 'd-none'">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">VALORES EN RESERVA<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                <div class="txt-dark">CAPITAL SALUD</div>
                            </div>
                            <div>
                                <a href="javascript:void(0)" class="me-2" click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                            </div>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <amchart-linea 
                                ref="gp_res" 
                                altura="450" 
                                min="0"
                                enmarcado
                                grosor="2"
                                grilla=".2"
                                leyenda="bottom"
                                rotar
                                campo_valor="PBS,PM,PAC" 
                                paleta="#179D82,#337CCF,#FC8452"
                                tooltip cursor>
                            </amchart-linea>
                        </div>
                    </div>
                </div><!-- End panel -->
            </div>
        </div>
        <!-- Desechos -->
        <div class="panel panel-default card-view border d-none">
            <div class="panel-heading">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="panel-title txt-dark text-bold text-upper mb-0" v-if="display == 'barra'">{{ titles[campo] }}<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                        <h6 class="panel-title txt-dark text-bold text-upper mb-0" v-else>COMPARATIVO ENTRE VALOR FACTURADO Y GLOSADO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                        <div class="txt-dark">CAPITAL SALUD</div>
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
                        <amchart-barra ref="gp_bar" paleta="#337CCF" pretag="$ " redondeado etiquetas grilla="0" tooltip cursor sin_valores puntos></amchart-barra>
                        <div class="d-flex justify-content-center mt-2">
                            <div class="btn-group btn-group-sm">
                                <button :class="getCss('facturado')" @click="setCampo('facturado')">Facturado</button>
                                <button :class="getCss('glosado')" @click="setCampo('glosado')">Glosado</button>
                                <button :class="getCss('relacion')" @click="setCampo('relacion')">Relación %</button>
                            </div>
                        </div>
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
            section: 'vertical',
            opt: [
                {'tx': 'Facturado vs Glosado', 'code': 'vertical'}, 
                {'tx': 'Tendencia (F vs G)', 'code': 'line-1'}, 
                {'tx': 'Valores pagados', 'code': 'line-2'}, 
                {'tx': 'Valores reserva', 'code': 'line-3'},
            ],
            titles: {'facturado': 'VALORES FACTURADOS POR PERIODOS', 'glosado': 'GLOSAS POR PERIODO', 'relacion': 'PORCENTAJE DE GLOSAS EN RELACIÓN CON VALORES FACTURADOS'},
            campo: 'facturado',     // facturado | glosado | relacion
			datos: [],
            numper: 0,
            sum_fac: 0,
            sum_glo: 0,
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
        miles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        numfixed: function(num, dec=1, always=true){
            if(num % 1){
                return Number.parseFloat(num).toFixed(dec);
            }
            return always? Number.parseFloat(num).toFixed(dec): num;
        },
        sortDesc: function(a, b){
            if(a == b){
                return 0;
            }
            return (a < b)? 1: -1;
        },
        prettyPer: function(arg){
            let a = arg.slice(0, 4);
            let b = arg.slice(-2);
            return `${a}-${b}`;
        },
        setSection: function(arg){
            this.section = arg;
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
        postResult: function(res){
            this.sum_fac = 0;
            this.sum_glo = 0;
            this.datos = res[0].result;
            this.datos.forEach(elm => {
                this.sum_fac += elm.v_facturado;
                this.sum_glo += elm.v_glosado;
            });
            this.$refs.c_per.setValor(this.datos.length);
            this.$refs.c_fac.setValor(this.miles(this.numfixed(this.sum_fac, 2, false)));
            this.$refs.c_glo.setValor(this.miles(this.numfixed(this.sum_glo, 2, false)));
            let xnum = this.numfixed((this.sum_glo / this.sum_fac) * 100);
            this.$refs.c_percent.setValor(`${xnum} %`);
            this.setCampo(this.campo);
            this.$refs.gp_bi.setDatos(this.datos.map(elm => {
                return {'categoria': this.prettyPer(elm._id), 'Glosado': elm.v_glosado, 'Facturado': elm.v_facturado}
            }).sort((a, b) => this.sortDesc(a.categoria, b.categoria)));
            this.$refs.gp_line.setDatos(this.datos.map(elm => {
                return {'categoria': this.prettyPer(elm._id), 'Glosado': elm.v_glosado, 'Facturado': elm.v_facturado}
            }));
            this.$refs.gp_pag.setDatos(this.datos.map(elm => {
                return {'categoria': this.prettyPer(elm._id), 'PBS': elm.pag_pbs, 'PM': elm.pag_pm, 'PAC': elm.pag_pac}
            }));
            this.$refs.gp_res.setDatos(this.datos.map(elm => {
                return {'categoria': this.prettyPer(elm._id), 'PBS': elm.res_pbs, 'PM': elm.res_pm, 'PAC': elm.res_pac}
            }));
        },
        exeQuery: function(force){
            this.status = this.state.LOADING;
            this.$refs.timecop.dispatchQuery('raw_cmed', this.pathdata, {}, null, force);
        },
        listen: function(){
            this.$eventBus.$on('search-finish', res => {
                this.postResult(res.contenido);
                this.status = this.state.LOADED;
            });
        }
    },
    mounted() {
        this.listen();
        this.exeQuery(false);
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
	.loading {opacity: .45; pointer-events: none; user-select: none}
</style>
