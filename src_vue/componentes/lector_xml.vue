<template>
    <div>
		Hola Mundo Vue. Lector XML.
    </div>
</template>
<script>
export default {
    props: {
        ejemplo: {type: String, default: ''},
    },
    data() {
        return {
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
        }
    },
    mounted() {
        // alert('some');
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
	.loading {opacity: .45; pointer-events: none; user-select: none}
</style>