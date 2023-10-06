<template>
    <div :class="'component-' + status">
        <div class="d-flex justify-content-between mt-3 mb-3">
            <div>
                <h5 class="txt-dark mb-0">{{ clientetx }} - <strong>PAGOS</strong><br></h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de reservas técnicas</div>
            </div>
            <div class="d-flex">
                <temporizador ref="timecop"></temporizador>
                <get-view-periodo :class="status" collections="retec_pagos"></get-view-periodo>
                <!-- <select-periodo ref="xtime" :coleccion="fuente" :alias="krache_time"></select-periodo> -->
                <div :class="section == 'basic'? 'btn-group dk-disabled ' + status: 'btn-group ' + status">
                    <button :class="display == 'chart'? 'btn btn-success': 'btn btn-default'" @click="display = 'chart'"><i class="fa fa-bar-chart"></i></button>
                    <button :class="display == 'table'? 'btn btn-success': 'btn btn-default'" @click="display = 'table'"><i class="fa fa-table"></i></button>
                </div>
            </div>
        </div>
        <div class="d-flex justify-content-between mb-4 df-options">
            <a :class="sectionStyle(elm.code)" href="javascript:void(0)" v-for="(elm, i) in opt" :key="i" @click="setSection(elm.code)">
                <div class="d-flex align-items-center">
                    <span class="lc-icon d-flex align-items-center justify-content-center me-2"><i :class="section == elm.code? 'fa fa-folder-open-o': 'fa fa-folder-o'"></i></span>
                    <span>{{ elm.tx }}</span>
                </div>
            </a>
        </div>
        <!-- contadores -->
        <div class="row">
            <div class="col-sm-7">
                <div class="row">
                    <div class="col-sm-4">
                        <local-counter ref="cnt_all" class="border" texto="REGISTROS" valor="0" fontsize="20px" duracion="1" miles></local-counter>
                    </div>
                    <div class="col-sm-4">
                        <local-counter ref="cnt_vdo" class="border" texto="Total VLRFACTURADO" fontsize="20px" valor="0" duracion="1" miles></local-counter>
                    </div>
                    <div class="col-sm-4">
                        <local-counter ref="cnt_gde" class="border" texto="Total GLOSADEFINITIVA" fontsize="20px" valor="0" duracion="1" miles></local-counter>
                    </div>
                </div>
            </div>
            <div class="col-sm-5">
                <div class="row">
                    <div class="col-sm-6">
                        <local-counter ref="cnt_pbs" class="border" texto="VALOR PAGADO PBS" fontsize="20px" valor=" " duracion="1" miles></local-counter>
                    </div>
                    <div class="col-sm-6">
                        <local-counter ref="cnt_pm" class="border" texto="VALOR PAGADO PM" fontsize="20px" valor=" " duracion="1" miles></local-counter>
                    </div>
                </div>
            </div>
        </div>
        <!-- fin contadores-->     
        <div :class="section == 'basic' ? '': 'd-none'">
            <div class="row">
                <div class="col-sm-4">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPO DE CONTRATO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_2.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar 
                                    ref="gp_2" 
                                    altura="160" 
                                    campo_categoria="_id" 
                                    campo_valor="total:Recuento" 
                                    redondeado
                                    tooltip 
                                    etiquetas 
                                    sin_valores 
                                    multicolor 
                                    grilla="0" 
                                    cursor 
                                    lanzarevento="select-tra" 
                                    empty_category="(Vacío)">
                                </am-bar>
                            </div>
                        </div>
                    </div>
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">PRESUPUESTOS MÁXIMOS<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_pmx.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar 
                                    ref="gp_pmx" 
                                    altura="160" 
                                    campo_categoria="_id" 
                                    campo_valor="total:Recuento" 
                                    empty_category="(Vacío)"
                                    redondeado
                                    tooltip 
                                    etiquetas 
                                    sin_valores 
                                    paleta="#1d4e89,#00b2ca,#7dcfb6,#fbd1a2,#f79256" 
                                    multicolor 
                                    grilla="0" 
                                    cursor 
                                    lanzarevento="select-pmx">
                                </am-bar>
                            </div>
                        </div>
                    </div>
                    <!-- NUEVO GRÁFICO ID TIPO PRESTADOR -->
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPO ID PRESTADOR<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_new_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar 
                                    ref="gp_new_1" 
                                    altura="160" 
                                    campo_categoria="_id" 
                                    campo_valor="total:Recuento" 
                                    redondeado
                                    tooltip 
                                    etiquetas 
                                    sin_valores 
                                    multicolor 
                                    grilla="0" 
                                    cursor 
                                    altura_minima="95" 
                                    unidad="24"
                                    empty_category="(Vacío)">
                                </am-bar>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-4">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">ÁMBITO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_3.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar 
                                    ref="gp_3" 
                                    altura="160" 
                                    campo_categoria="_id" 
                                    campo_valor="total:Recuento" 
                                    tooltip 
                                    etiquetas 
                                    sin_valores 
                                    paleta="#1d4e89,#00b2ca,#7dcfb6,#fbd1a2,#f79256" 
                                    multicolor 
                                    redondeado
                                    grilla="0" 
                                    cursor 
                                    altura_minima="95" 
                                    unidad="24"
                                    lanzarevento="select-amb" 
                                    empty_category="(Vacío)">
                                </am-bar>
                            </div>
                        </div>
                    </div>
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">PLAN SALUD<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar 
                                    ref="gp_1" 
                                    altura="160" 
                                    campo_categoria="_id" 
                                    campo_valor="total:Recuento" 
                                    tooltip 
                                    etiquetas 
                                    sin_valores 
                                    paleta="#8ecae6,#219ebc,#023047,#ffb703,#fb8500" 
                                    multicolor 
                                    grilla="0" 
                                    cursor 
                                    redondeado
                                    lanzarevento="select-pla" 
                                    empty_category="(Vacío)">
                                </am-bar>
                            </div>
                        </div>
                    </div>
                    <!-- NUEVO GRÁFICO MECANISMO DE PAGO -->
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">MECANISMO DE PAGO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_new_2.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar 
                                    ref="gp_new_2" 
                                    altura="160" 
                                    campo_categoria="_id" 
                                    campo_valor="total:Recuento" 
                                    redondeado
                                    tooltip 
                                    etiquetas 
                                    sin_valores 
                                    multicolor 
                                    grilla="0" 
                                    cursor 
                                    empty_category="(Vacío)">
                                </am-bar>
                            </div>
                        </div>
                    </div>                    
                </div>
                <div class="col-sm-4">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPOS DE USUARIOS<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_4.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-ver ref="gp_4" grilla="0" multicolor campo_categoria="_id" campo_valor="total" tooltip cursor etiquetas sin_valores altura_minima="100" unidad="34" lanzarevento="select-tus" empty_category="(Vacío)"></am-ver>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Ranking RS-->
        <div :class="section == 'ranking-rs'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE PAGOS PBS - RÉGIMEN SUBSIDIADO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.ran_1a.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_1a" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="ran_1a" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="valor" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            truncar
                            custom="Valor: {valueX}, Registros: {total}" 
                            custom_label="{valueX} ({total} registros)" 
                            empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE PAGOS PM - RÉGIMEN SUBSIDIADO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.ran_1b.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_1b" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="ran_1b" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="valor" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            truncar
                            custom="Valor: {valueX}, Registros: {total}" 
                            custom_label="{valueX} ({total} registros)" 
                            empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
        </div>
        <!-- End Ranking RS-->
        <!-- Ranking RC-->
         <div :class="section == 'ranking-rc'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE PAGOS PBS - RÉGIMEN CONTRIBUTIVO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.ran_2a.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_2a" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="ran_2a" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="valor" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            truncar
                            custom="Valor: {valueX}, Registros: {total}" 
                            custom_label="{valueX} ({total} registros)" 
                            empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE PAGOS PM - RÉGIMEN CONTRIBUTIVO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.ran_2b.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_2b" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="ran_2b" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="valor" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            truncar
                            custom="Valor: {valueX}, Registros: {total}" 
                            custom_label="{valueX} ({total} registros)" 
                            empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
        </div>
        <!-- End Ranking RC-->
        <!-- Ranking PAC-->
        <div :class="section == 'ranking-pac'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE PAGOS PBS - PAC<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.ran_3a.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_3a" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="ran_3a" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="valor" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            truncar
                            custom="Valor: {valueX}, Registros: {total}" 
                            custom_label="{valueX} ({total} registros)" 
                            empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE PAGOS PRESUPUESTOS MÁXIMOS - PAC<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.ran_3b.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_3b" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="ran_3b" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="valor" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            truncar
                            custom="Valor: {valueX}, Registros: {total}" 
                            custom_label="{valueX} ({total} registros)" 
                            empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
        </div>
        <!-- End Ranking PAC-->

        <div :class="section == 'schema'? '': 'd-none'">
            <div class="row">
                <div class="col-sm-3">
                    <div class="panel panel-default card-view border pt-4 pb-3">
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body py-0">
                                <span class="uppercase-font weight-500 font-14 block text-center txt-dark">TOTAL REGISTROS</span>
                                <div class="weight-500 txt-success text-center mt-2 fs-1" v-if="status_sch == state.LOADING">
                                    <i class="fa fa-spin fa-spinner"></i>
                                </div>
                                <div class="weight-500 txt-success text-center mt-2 fs-5" v-else-if="num_registros == -1">
                                    Sin analizar
                                </div>
                                <div class="weight-500 txt-success text-center mt-0 fs-1" style="line-height:1.2em" v-else>
                                    {{ numformat(num_registros) }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- END PANEL -->
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="pull-left">
                                <h6 class="panel-title txt-dark">Métricas</h6>
                            </div>
                            <div class="clearfix"></div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div  class="panel-body">
                                <div class="d-flex align-items-center pt-0 pb-3" v-if="status_sch == state.LOADING">
                                    <i class="fa fa-spin fa-spinner me-2 fs-4"></i> <span>Cargando métricas...</span>
                                </div>
                                <div v-else-if="status_sch == state.LOADED">
                                    <div v-for="(elm, i) in campos" :key="i">
                                        <span class="font-12 head-font txt-dark">{{ pairs[elm] }}<span class="pull-right">{{ getPercent(rawSchema['n_' + elm]) }}%</span></span>
                                        <div class="progress mt-0 mb-3">
                                            <div :class="rawSchema['n_' + elm] == num_registros? 'progress-bar progress-bar-success': 'progress-bar progress-bar-danger'" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" :style="{width: getPercent(rawSchema['n_' + elm]) + '%'}" role="progressbar"> <span class="sr-only">85% Complete (success)</span></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-9">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">ESTRUCTURA DE LA BASE DE DATOS DE FACTURAS</h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" v-if="status_sch == state.LOADING"><i class="fa fa-spin fa-spinner"></i></a>
                                    <a href="javascript:void(0)" class="refresh me-2" v-on:click="getSchema(true)" v-else><i class="zmdi zmdi-replay"></i></a>
                                    <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body">
                                <div class="" v-if="status_sch == state.LOADING">
                                    <div class="d-flex align-items-center pt-0 pb-3">
                                        <i class="fa fa-spin fa-spinner me-3 fs-2"></i>
                                        <div>
                                            <div>Analizando campos requeridos de la base de datos...</div>
                                        </div>
                                    </div>
                                    <div class="progress progress-lg mt-3">
                                        <div class="progress-bar progress-bar-success" :style="{width: porcion[pinload].per}" role="progressbar">{{ porcion[pinload].per }}</div>
                                    </div>
                                </div>
                                <table class="table" v-if="status_sch == state.LOADED">
                                    <thead>
                                        <tr>
                                            <th class="colmin text-center">No.</th>
                                            <th>Nombre del campo</th>
                                            <th>Nombre corto</th>
                                            <th class="colmin text-center">Apariciones del campo</th>
                                            <th class="colmin text-center">Estado</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(elm, i) in campos" :key="i">
                                            <td class="text-center">{{ i + 1 }}</td>
                                            <td>{{ pairs[elm] }}</td>
                                            <td>{{ elm }}</td>
                                            <td class="text-right">{{ numformat(rawSchema['n_' + elm]) }}</td>
                                            <td class="text-center">
                                                <span class="label label-success px-2" v-if="num_registros == rawSchema['n_' + elm]"><i class="fa fa-check me-1"></i>Completo</span>
                                                <span class="label label-danger px-2 dk-hand" @click="showRecord(elm)" v-else>- {{ num_registros - rawSchema['n_' + elm] }}</span>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- End section SCHEMA -->
        <div :class="section == 'controls'? '': 'd-none'">
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr class="tr-center">
                                        <th class="text-bold">VLR FACTURADO</th>
                                        <th class="text-bold">VLR GLOSADO</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row" v-if="rawCtr != null">
                                        <td class="text-center">{{ numformat(clearNumber(rawCtr.s_vdo)) }}</td>
                                        <td class="text-center">{{ numformat(clearNumber(rawCtr.s_gde)) }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr>
                                        <th colspan="5" class="pt-0 pb-2" style="letter-spacing:1px; font-family:Arial">
                                            PAGOS PBS
                                            <div>{{ human_period }}</div>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row tr-25" v-if="rawCtr != null">
                                        <td>
                                            <div class="text-bold">FACTURADO PBS</div>{{ numformat(clearNumber(rawCtr.f_pbs)) }}
                                        </td>
                                        <td>
                                            <div class="text-bold">GLOSADO PBS</div>{{ numformat(clearNumber(rawCtr.g_pbs)) }}
                                        </td>
                                        <td>
                                            <div class="text-bold">PAGADO PBS</div>{{ numformat(clearNumber(rawCtr.s_vpbs)) }}
                                        </td>
                                        <td :class="(rawCtr.f_pbs - (rawCtr.g_pbs + rawCtr.s_vpbs)) == 0? 'dk-success': 'txt-danger'">
                                            <div class="text-bold">DIFERENCIA</div>
                                            {{ numformat(clearNumber(rawCtr.f_pbs - (rawCtr.g_pbs + rawCtr.s_vpbs))) }}
                                        </td>
                                    </tr>
                                    <tr v-if="status == state.LOADING">
                                        <td colspan="5">
                                            <div class="d-flex align-items-center">
                                                <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                                                <span>Cargando...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr>
                                        <th colspan="5" class="pt-0 pb-2" style="letter-spacing:1px; font-family:Arial">
                                            PAGOS PM
                                            <div>{{ human_period }}</div>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row tr-25" v-if="rawCtr != null">
                                        <td>
                                            <div class="text-bold">FACTURADO PM</div>{{ numformat(clearNumber(rawCtr.f_pm)) }}
                                        </td>
                                        <td>
                                            <div class="text-bold">GLOSADO PM</div>{{ numformat(clearNumber(rawCtr.g_pm)) }}
                                        </td>
                                        <td>
                                            <div class="text-bold">PAGADO PM</div>{{ numformat(clearNumber(rawCtr.s_vppm)) }}
                                        </td>
                                        <td :class="(rawCtr.f_pm - (rawCtr.g_pm + rawCtr.s_vppm)) == 0? 'dk-success': 'txt-danger'">
                                            <div class="text-bold">DIFERENCIA</div>
                                            {{ numformat(clearNumber(rawCtr.f_pm - (rawCtr.g_pm + rawCtr.s_vppm))) }}
                                        </td>
                                    </tr>
                                    <tr v-if="status == state.LOADING">
                                        <td colspan="5">
                                            <div class="d-flex align-items-center">
                                                <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                                                <span>Cargando...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

        </div>
        <!-- End section CONTROLS -->
        <div :class="section == 'import'? '': 'd-none'">
            <import-basic 
                :destino="fuente" 
                separador_mode="normal" 
                subtitulo="RESERVAS TÉCNICAS - PAGOS" 
                separador="|" 
                sindiccionario
                head="file_parse"
                fields="ifa:idFactura|tpp:tipoIdPrestador|idp:idPrestador|nmp:nombrePrestador|pla:planSalud|tra:Tcontra|idc:idContrato|tus:tipoIdUsuario|ius:idUsuario|iau:idAvisado|fau:FAvis|amb:Ambito|ids:idServicio|ser:DesServicio|dia:DiagPpal|can:Cant|fp:FPres|fr:FRad|vdo:VlrFacturado|gde:glosaDefinitiva|mpa:MecPago|vpbs:VlrPagadoPBS|vpac:VlrPagadoPAC|vppm:VlrPagadoPM|fpa:Fpago|pmx:pres_Max|pac:PAct|ume:UMed|ffa:FFarma|cov:Covid"
                rules=""
                codec_mode="show"
                error="ignore"
                error_mode="show"
                info
                extra
                withperiodo
                realtime
                :clientetx="clientetx">
            </import-basic>
            <div class="my-4"></div>
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <import-list :coleccion="fuente" titulo="BASE DE DATOS DE PAGOS"></import-list>
                    </div>
                </div>
            </div>
        </div>
        <local-modal 
            :coleccion="fuente" 
            cantidad="50"
            campos="ifa:idFactura,tpp:tipoIdPrestador,idp:idPrestador,nmp:nombrePrestador,pla:planSalud,tra:Tcontra,idc:idContrato,tus:tipoIdUsuario,ius:idUsuario,iau:idAvisado,fau:FAvis,amb:Ambito,ids:idServicio,ser:DesServicio,dia:DiagPpal,can:Cant,fp:FPres,fr:FRad,vdo:VlrFacturado,gde:glosaDefinitiva,mpa:MecPago,vpbs:VlrPagadoPBS,vpac:VlrPagadoPAC,vppm:VlrPagadoPM,fpa:Fpago,pmx:pres_Max,pac:PAct,ume:UMed,ffa:FFarma,cov:Covid,crx:Periodo">
        </local-modal>
    </div>
</template>
<script>
import Counter from './../Contador_light.vue';
import PieChart from './../amcharts/pie.vue';
import BarChart from './../amcharts/bar.vue';
import VBarChart from './../amcharts/bar-vertical.vue';
import Ztime from './../select-periodos.vue';
import Modal from './../modal_table_data.vue';

export default {
    components: {'local-counter': Counter, 'am-pie': PieChart, 'am-bar': BarChart, 'am-ver': VBarChart, 'select-periodo': Ztime, 'local-modal': Modal},
    props: {
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''},
        cliente: {type: String, default: ''},
        clientetx: {type: String, default: ''},
        urol: {type: String, default: ''},
    },
    data() {
        return {
            tokens: {},
            keycode: '',
            fuente: 'retec_pagos',
            // fuente: '7_retec_pagos',
            krache: 'dash_pagos_' + this.cliente,
            krache_time: 'time_pago_' + this.cliente,
            section: 'basic',
            display: 'chart',       // table | chart
            opt: [
                {'tx': 'General', 'code': 'basic'}, 
                {'tx': 'Pagos RS', 'code': 'ranking-rs'}, //ranking-1
                {'tx': 'Pagos RC', 'code': 'ranking-rc'},
                {'tx': 'Pagos PAC', 'code': 'ranking-pac'}, 
                {'tx': 'Estructura', 'code': 'schema'}, 
                {'tx': 'Pagos por plan', 'code': 'controls'}, 
                {'tx': 'Importar', 'code': 'import'}
            ],
            meses: {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'},
            campos: ['ifa', 'tpp', 'idp', 'nmp', 'pla', 'tra', 'idc', 'tus', 'ius', 'iau', 'fau', 'amb', 'ids', 'ser', 'dia', 'can', 'fp', 'fr', 'vdo', 'gde', 'mpa', 'vpbs', 'vpac', 'vppm', 'fpa', 'pmx', 'pac', 'ume', 'ffa', 'cov'],
            pairs: {_id:'Total registros', ifa:'idFactura', tpp:'tipoIdPrestador', idp:'idPrestador', nmp:'nombrePrestador', pla:'planSalud', tra:'Tcontra', idc:'idContrato', tus:'tipoIdUsuario', ius:'idUsuario', iau:'idAvisado', fau:'FAvis', amb:'Ambito', ids:'idServicio', ser:'DesServicio', dia:'DiagPpal', can:'Cant', fp:'FPres', fr:'FRad', vdo:'VlrFacturado', gde:'glosaDefinitiva', mpa:'MecPago', vpbs:'VlrPagadoPBS', vpac:'VlrPagadoPAC', vppm:'VlrPagadoPM', fpa:'Fpago', pmx:'pres_Max', pac:'PAct', ume:'UMed', ffa:'FFarma', cov:'Covid'},
            // campos: ['tpo', 'ifa', 'tpp', 'idp', 'nmp', 'pla', 'tra', 'idc', 'tus', 'ius', 'iau', 'fau', 'amb', 'ids', 'ser', 'dia', 'can', 'fp', 'fr', 'vdo', 'vpbs', 'vpac', 'vppm', 'vgl'],
            // pairs: {_id:'TOTAL REGISTROS', tpo:'TIPOOBLIGACION', ifa:'IDFACTURA', tpp:'TIPOIDPRESTADOR', idp:'IDPRESTADOR', nmp:'NOMBREPRESTADOR', pla:'PLANSALUD', tra:'TCONTRA', idc:'IDCONTRATO', tus:'TIPOIDUSUARIO', ius:'IDUSUARIO', iau:'IDAUTORIZACION', fau:'FAUTO', amb:'AMBITO', ids:'IDSERVICIO', ser:'DESSERVICIO', dia:'DIAGPPAL', can:'CANT', fp:'FPRES', fr:'FRAD', vdo:'VLRFACTURADO', vpbs:'VLRPAGADOPBS', vpac:'VLRPAGADOPAC', vppm:'VLRPAGADOPM', vgl:'VLRGLOSADO'},
            rawData: null,
            rawCtr: null,
            rawSchema: [],
            periodo: 202106,
			datos: [],
            num_registros: -1,
            status: 'ini',
            status_sch: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            pinload: 0,
            porcion: [{'a': 0, 'b': 5, 'per': '0'}, {'a': 5, 'b': 10, 'per': '33%'}, {'a': 10, 'b': 15, 'per': '67%'}, {'per': '100%'}],
        }
    },
    computed: {
        human_period: function(){
            let ym = this.periodo.toString();
            if(ym.length == 6){
                let anio = ym.slice(0, 4);
                let ms = ym.slice(-2);
                return this.meses[ms] + ' de ' + anio;
            }
            return '';
        }
    },
    methods: {
        makeToken: function(){
            let str = '';
            for(let i = 0; i < 5; i++){
                let num = Math.round(Math.random() * 25 + 65);
                str += String.fromCharCode(num);
            }
            str += Math.round(Math.random() * 999 + 1000);
            return str;
        },
        sectionStyle: function(code){
            let acc = (this.status == this.state.LOADING)? ' loading': '';
            return (this.section == code)? 'flex-fill bg-target' + acc: 'flex-fill bg-custom' + acc;
        },
        isEmpty: function(arg){
            if([undefined, null, ''].includes(arg)) return true;
            return /^\s*$/.test(arg);
        },
        clearNumber: function(num){
            return (num % 1 == 0)? num: parseFloat(num).toFixed(2);
        },
        numformat: function(snum){
            let tm = new String(snum);
            return tm.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        altCss: function(bool, a='', b='d-none'){
            return bool? a: b;
        },
        getPercent: function(num){
            let tm = (num / this.num_registros) * 100;
            if(tm >= 99.9 && tm < 100){
                return 99.99;
            }
            return (tm % 1 == 0)? tm: tm.toFixed(2);
        },
        openModal: function(bool){
            this.$eventBus.$emit('open-modal', {'open': bool});
        },
        setSection: function(arg){
            if(this.status != this.state.LOADING && this.status_sch != this.state.LOADING){
                this.section = arg;
                this.manager();
            }
        },
        writeCards: function(){
            // rs:0: Total
            // rs_1: Plan salud
            // rs_2: Tcontra
            // rs_3: Ámbito
            // rs_4: Tipo Usuario
            if(this.rawData != null){
                if(this.rawData['rs_0'].length == 0){
                    this.$refs.cnt_all.setValor('');
                    this.$refs.cnt_vdo.setValor('');
                    this.$refs.cnt_gde.setValor('');
                    this.$refs.cnt_pbs.setValor('');
                    this.$refs.cnt_pm.setValor('');
                    console.log('No se encontraron datos!');
                }else{
                    this.$refs.cnt_all.setValor(this.rawData['rs_0'][0].total);
                    this.$refs.cnt_vdo.setValor(Math.round(this.clearNumber(this.rawData['rs_0'][0].sum_vdo)));
                    this.$refs.cnt_gde.setValor(Math.round(this.clearNumber(this.rawData['rs_0'][0].sum_gde)));
                    this.$refs.cnt_pbs.setValor(this.clearNumber(Math.round(this.rawData['rs_0'][0].r_pbs)));
                    this.$refs.cnt_pm.setValor(this.clearNumber(Math.round(this.rawData['rs_0'][0].r_pm)));
                }
                this.$refs.gp_1.setDatos(this.rawData['rs_1']); // Plan salud
                this.$refs.gp_2.setDatos(this.rawData['rs_2']); // TContra
                this.$refs.gp_3.setDatos(this.rawData['rs_3']); // Ámbito
                this.$refs.gp_4.setDatos(this.rawData['rs_4']); // TIPO USUARIO
                this.$refs.gp_new_1.setDatos(this.rawData['new_1']); // TIPO ID PRESTADOR
                this.$refs.gp_new_2.setDatos(this.rawData['new_2']); // MECANISMO DE PAGO
                //Ranking RS
                this.$refs.tb_1a.setDatos(this.parseNull(this.rawData['ran_1a']), '$ ');
                this.$refs.ran_1a.setDatos(this.rawData['ran_1a'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ '); //grafico 1a
                this.$refs.tb_1b.setDatos(this.parseNull(this.rawData['ran_1b']), '$ ');
                this.$refs.ran_1b.setDatos(this.rawData['ran_1b'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ '); //grafico 1b
                //End Ranking RS
                //Ranking RC
                this.$refs.tb_2a.setDatos(this.parseNull(this.rawData['ran_2a']), '$ ');
                this.$refs.ran_2a.setDatos(this.rawData['ran_2a'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ '); //grafico 1a
                this.$refs.tb_2b.setDatos(this.parseNull(this.rawData['ran_2b']), '$ ');
                this.$refs.ran_2b.setDatos(this.rawData['ran_2b'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ '); //grafico 1b
                //End Ranking RC
                //Ranking PAC
                this.$refs.tb_3a.setDatos(this.parseNull(this.rawData['ran_3a']), '$ ');
                this.$refs.ran_3a.setDatos(this.rawData['ran_3a'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ '); //grafico 1a
                this.$refs.tb_3b.setDatos(this.parseNull(this.rawData['ran_3b']), '$ ');
                this.$refs.ran_3b.setDatos(this.rawData['ran_3b'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ '); //grafico 1b
                //End Ranking PAC
                if(Array.isArray(this.rawData['pmx'])){
                    let aux = {};
                    this.rawData['pmx'].forEach(elm => {
                        let kd = String(elm._id);
                        if(aux[kd] == undefined){
                            aux[kd] = {'_id': kd, 'total': 0};
                        }
                        aux[kd].total += elm.total;
                    });
                    this.$refs.gp_pmx.setDatos(Object.values(aux));
                }
            }
        },
        parseNull: function(arg, tx='(Vacío)') {
            console.log('Que estoy recibiendo?');
            console.log(arg);
            return arg.map(elm => {
                if(elm._id == null){
                    elm._id = tx;
                }
                return elm;
            });
        },
        getSchema: function(force=false){
            this.status_sch = this.state.LOADING;
            this.status = this.state.LOADING;
            this.$refs.timecop.dispatchQuery(
                'schema_pay' + this.periodo,
                this.pathdata + '/schema',
                {'tema': this.fuente, 'periodo': this.periodo},
                res => {
                    this.rawSchema = res[0];
                    this.num_registros = this.rawSchema.total;
                    this.status_sch = this.state.LOADED;
                    this.status = this.state.LOADED;
                },
                force
            );
        },
        manager: function(force=false){
            if('basic' == this.section){
                this.status = this.state.LOADING;
                this.$refs.timecop.dispatchQuery(
                    'raw_pay_dat' + this.periodo,
                    this.pathdata + '/data',
                    {'tema': this.fuente, 'periodo': this.periodo},
                    res => {
                        console.log(res);
                        this.rawData = (res.length > 0)?  res[0]: {'rs_0': [], 'rs_1': [], 'rs_2': [], 'rs_3': [], 'rs_4': [], 'rs_5': [], 'pmx': [], 'ran_1a':[], 'ran_1b':[], 'ran_2a':[], 'ran_2b':[], 'ran_3a':[], 'ran_3b':[]};
                        this.writeCards();
                        this.status = this.state.LOADED;
                    },
                    force
                );
            }else if('controls' == this.section){
                this.status = this.state.LOADING;
                this.$refs.timecop.dispatchQuery(
                    'raw_pay_ctr' + this.periodo,
                    this.pathdata + '/controls',
                    {'tema': this.fuente, 'periodo': this.periodo},
                    res => {
                        console.log(res);
                        this.rawCtr = (res.length > 0)? res[0]: null;
                        // this.rawData = (res.length > 0)?  res[0]: {'rs_0': [], 'rs_1': [], 'rs_2': [], 'rs_3': [], 'rs_4': [], 'cores': [], 's0': [], 'v0': [], 's1': [], 'v1': []};
                        this.status = this.state.LOADED;
                    },
                    force
                );
            }else if('schema' == this.section){
                this.getSchema(force);
            }
        },
        showRecord: function(field){
            this.$eventBus.$emit('open-modal', {'titulo': 'ESTRUCTURA - CAMPOS NO ENCONTRADOS', 'periodo': this.periodo, 'filtros': field + ':exists:false', 'foco': field});
        },
        listen: function(){
            this.$eventBus.$on('select-pla', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'PLAN SALUD', 'periodo': this.periodo, 'filtros': 'pla:' + arg._id, 'foco': 'pla'});
            });
            this.$eventBus.$on('select-tra', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'TIPO DE CONTRATO', 'periodo': this.periodo, 'filtros': 'tra:' + arg._id, 'foco': 'tra'});
            });
            this.$eventBus.$on('select-amb', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'ÁMBITO', 'periodo': this.periodo, 'filtros': 'amb:' + arg._id, 'foco': 'amb'});
            });
            this.$eventBus.$on('select-tus', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'TIPO DE DOCUMENTO', 'periodo': this.periodo, 'filtros': 'tus:' + arg._id, 'foco': 'tus'});
            });
            this.$eventBus.$on('select-pmx', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'PRESUPUESTOS MÁXIMOS', 'periodo': this.periodo, 'filtros': 'pmx:' + arg._id, 'foco': 'pmx'});
            });
            this.$eventBus.$on('time-select', obj => {
                console.log('time-select dispatch');
                this.periodo = obj.periodo;
                this.manager();
            });
            this.$eventBus.$on('time-refresh', obj => {
                console.log('time-refresh dispatch');
                this.periodo = obj.periodo;
                unregisterJSON(this.krache);
                this.manager(true);
            });
        }
    },
    mounted() {
        this.listen();
        if(this.urol == 'Consultor'){
            this.opt.pop();
        }
    }
}
</script>
<style>
.text-upper {text-transform: uppercase !important}
.dk-hand {cursor: pointer !important; user-select: none}
.text-bold {font-weight: bold !important}
.dk-disabled {opacity: .5 !important; user-select: none !important; pointer-events: none !important}
.dk-row {color:#000; font-family: Arial}
.dk-row td, .tr-center th {text-align: center !important}
.dk-success {color:#29B672 !important}
.tr-center th {font-weight: bold}
.tr-25 > td, .td-25 {width: 25%}
.td-25 {width: 25%}

.component-loading .card-view > div, .loading {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
.component-loading .panel-body.vega {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
.component-loading .df-options > a {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
</style>
