<template>
    <div>
        <div class="input-group" v-if="clock != null">
            <div class="input-group-addon" style="background:#FFF">
                <i class="icon-clock"></i>
            </div>
            <input type="text" class="form-control" :value="clock_human">
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
            clock: null,
            clock_human: '',
            seg: 0,
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        clock_up: function(){
            if(this.clock != null){
                clearInterval(this.clock);
                this.clock = null;
            }
            this.seg = 0;
            this.clock = setInterval(() => {
                this.seg++;
                this.clock_human = this.getTime();
            }, 1000);
        },
        clock_down: function(){
            if(this.clock != null){
                clearInterval(this.clock);
            }
            this.clock = null;
            this.seg = 0;
        },
        getTime: function(){
            let mn = Math.floor(this.seg / 60).toString().padStart(2, '0');
            let rs = (this.seg % 60).toString().padStart(2, '0');
            return `${mn}:${rs} segundos`;
        },
        getTimestamp: function(){
            return (new Date()).toString().slice(11, 24);
        }
    },
    mounted() {
        // this.clock_up();
    }
}
</script>
<style scoped>
	.loading {opacity: .45; pointer-events: none; user-select: none}
</style>
