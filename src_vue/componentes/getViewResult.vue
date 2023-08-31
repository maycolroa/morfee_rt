<template>
    <div>
        <h5>
            {{ success }}
        </h5>
    </div>
</template>
<script>
export default {
    data() {
        return {
            success : '',
            cm : 'cm_views',
			datos: [],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        loadData: function(){
            let pam = {};
            this.status = this.state.LOADING;
            axios.post(this.pathdata, pam).then(res => {
                this.datos = res.data;
                this.status = this.state.LOADED;
            }).catch(err => {
                this.status = this.state.FAILED;
                console.log(err);
            });
        }
    },
    loadData: function(){
        if(this.status != this.state.LOADING){
            this.status = this.state.LOADING;
            let pam = new FormData();
            pam.append('collections', this.cm);
            axios.post(path_app + "vue/getView", pam).then(res => {
                this.datos = res.data;
                this.status = this.state.LOADED;               
            }).catch(err => {
                console.log(err);
                this.status = this.state.FAILED;
                alert('error:'+err);
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
</style>