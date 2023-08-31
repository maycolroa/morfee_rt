<template>
    <div>
        <div class="row">
            <div class="col-sm-6">
                <div class="row">
                    <div class="col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">Mes servicio:</label>
                            <input type="number" class="form-control" v-model="mes_servicio">
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">Valor factura:</label>
                            <input type="number" class="form-control" v-model="valor_factura">
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">Tipo contrato:</label>
                            <input type="text" class="form-control" v-model="tipo_contrato">
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">Modalidad contrato:</label>
                            <input type="text" class="form-control" v-model="modalidad_contrato">
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-6">
                <div class="row">
                    <div class="col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">Municipio afiliado:</label>
                            <input type="text" class="form-control" v-model="municipio_afiliado">
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">Depto afiliado:</label>
                            <input type="text" class="form-control" v-model="departamento_afiliado">
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">Tipo régimen:</label>
                            <input type="text" class="form-control" v-model="tipo_regimen">
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">POS:</label>
                            <input type="text" class="form-control" v-model="pos">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="text-center">
            <button class="btn btn-success" @click="prediccion">Predecir</button>
        </div>
        <div class="mt-4">{{ status }}</div>
    </div>
</template>
<script>
export default {
    props: {
        pathmodel: {type: String, default: ''},
    },
    data() {
        return {
            modelo: null,
            mes_servicio: '',
            valor_factura: '',
            tipo_contrato: '',
            modalidad_contrato: '',
            municipio_afiliado: '',
            departamento_afiliado: '',
            tipo_regimen: '',
            pos: '',
			datos: [],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        loadModel: async function(){
            this.status = 'Cargando modelo...';
            this.modelo = await tf.loadLayersModel(this.pathmodel);
            this.status = 'Modelo cargado';
        },
        prediccion: function(){
            if(this.modelo){
                console.log('Prediciendo...');
                let inputData = tf.tensor2d([
                    this.mes_servicio, 
                    this.valor_factura, 
                    this.tipo_contrato, 
                    this.modalidad_contrato, 
                    this.municipio_afiliado, 
                    this.departamento_afiliado, 
                    this.tipo_regimen, 
                    this.pos
                ], [1, 8]);
                let result = this.modelo.predict(inputData);
                result.print();
                console.log('Listo...');
            }
        }
    },
    mounted() {
        const plugin = document.createElement('script');
        plugin.setAttribute("src", "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest");
        plugin.async = true;
        plugin.onload = () => this.loadModel();
        document.head.appendChild(plugin);
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
	.loading {opacity: .45; pointer-events: none; user-select: none}
</style>
