<template>
    <div>
        <canvas id='c'></canvas>
    </div>
</template>
<script>
export default {
    props: {
        
    },
    data(){
        return {
               w : c.width = window.innerWidth,
               h : c.height = window.innerHeight,
               ctx : c.getContext( '2d' ), 
               opts : {                   
                    range: 180,
                    baseConnections: 3,
                    addedConnections: 5,
                    baseSize: 5,
                    minSize: 1,
                    dataToConnectionSize: .4,
                    sizeMultiplier: .7,
                    allowedDist: 40,
                    baseDist: 40,
                    addedDist: 30,
                    connectionAttempts: 100,
                    
                    dataToConnections: 1,
                    baseSpeed: .04,
                    addedSpeed: .05,
                    baseGlowSpeed: .4,
                    addedGlowSpeed: .4,
                    
                    rotVelX: .003,
                    rotVelY: .002,
                    
                    repaintColor: '#900',
                    connectionColor: 'hsla(200,60%,light%,alp)',
                    rootColor: 'hsla(0,60%,light%,alp)',
                    endColor: 'hsla(160,20%,light%,alp)',
                    dataColor: 'hsla(40,80%,light%,alp)',
                    
                    wireframeWidth: .1,
                    wireframeColor: '#88f',
                    
                    depth: 250,
                    focalLength: 250,
                    vanishPoint: {
                        x: w / 2,
                        y: h / 2
                    }
                },
                
                squareRange : opts.range * opts.range,
                squareAllowed : opts.allowedDist * opts.allowedDist,
                mostDistant : opts.depth + opts.range,
                sinX : sinY = 0,
                cosX : cosY = 0,
                
                connections : [],
                toDevelop : [],
                data : [],
                all : [],
                tick : 0,
                totalProb : 0,
                
                animating : false,
                
                Tau : Math.PI * 2
        }
    },
    methods:{
         init: function(){   
            alert('isaias');
            this.this.connections.length = 0;
            this.data.length = 0;
            this.all.length = 0;
            this.toDevelop.length = 0;
      
            var connection = new Connection( 0, 0, 0, this.opts.baseSize );
            connection.step = Connection.rootStep;
            this.connections.push( connection );
            this.all.push( connection );
            connection.link();
            
            while( this.toDevelop.length > 0 ){
            
                this.toDevelop[ 0 ].link();
                this.toDevelop.shift();
            }
            
            if( !this.animating ){
                this.animating = true;
                this.anim();
            }
        },
        Connection: function( x, y, z, size ){       
            this.x = x;
            this.y = y;
            this.z = z;
            this.size = size;
            
            this.screen = {};
            
            this.links = [];
            this.probabilities = [];
            this.isEnd = false;
            
            this.glowSpeed = this.opts.baseGlowSpeed + this.opts.addedGlowSpeed * Math.random();
        },
        squareDist: function( a, b ){
            
            var x = b.x - a.x,
                    y = b.y - a.y,
                    z = b.z - a.z;
            
            return x*x + y*y + z*z;
        },

        anim: function(){   
            window.requestAnimationFrame( anim );
            this.ctx.globalCompositeOperation = 'source-over';
            this.ctx.fillStyle = this.opts.repaintColor;
            this.ctx.fillRect( 0, 0, w, h );
            ++this.tick;
            var rotX = this.tick * this.opts.rotVelX;
            var rotY = this.tick * this.opts.rotVelY;         
            this.cosX = Math.cos( rotX );
            this.sinX = Math.sin( rotX );
            this.cosY = Math.cos( rotY );
            this.sinY = Math.sin( rotY );
            
            if( this.data.length < this.connections.length * this.opts.dataToConnections ){
                var datum = new Data( this.connections[ 0 ] );
                this.data.push( datum );
                this.all.push( datum );
            }           
            this.ctx.globalCompositeOperation = 'lighter';
            this.ctx.beginPath();
            this.ctx.lineWidth = this.opts.wireframeWidth;
            this.ctx.strokeStyle = this.opts.wireframeColor;
            this.all.map( function( item ){ item.step(); } );
            this.ctx.stroke();
            this.ctx.globalCompositeOperation = 'source-over';
            this.all.sort( function( a, b ){ return b.screen.z - a.screen.z } );
            this.all.map( function( item ){ item.draw(); } );         
            /*ctx.beginPath();
            ctx.strokeStyle = 'red';
            ctx.arc( opts.vanishPoint.x, opts.vanishPoint.y, opts.range * opts.focalLength / opts.depth, 0, Tau );
            ctx.stroke();*/
        }




    },

    mounted(){      
        this.ctx.fillStyle = '#222';
        this.ctx.fillRect( 0, 0, w, h );
        this.ctx.fillStyle = '#ccc';
        this.ctx.font = '50px Verdana';
        this.ctx.fillText( 'Calculating Nodes', w / 2 - this.ctx.measureText( 'Calculating Nodes' ).width / 2, h / 2 - 15 );
        window.setTimeout( init, 4 ); // to render the loading screen
        //variables con metodos
        Connection.prototype.link = function(){
            
            if( this.size < this.opts.minSize )
                return this.isEnd = true;
            
            var links = [],
                    connectionsNum = this.opts.baseConnections + Math.random() * this.opts.addedConnections |0,
                    attempt = this.opts.connectionAttempts,
                    
                    alpha, beta, len,
                    cosA, sinA, cosB, sinB,
                    pos = {},
                    passedExisting, passedBuffered;
            
            while( links.length < connectionsNum && --attempt > 0 ){
                
                alpha = Math.random() * Math.PI;
                beta = Math.random() * this.Tau;
                len = this.opts.baseDist + this.opts.addedDist * Math.random();
                
                cosA = Math.cos( alpha );
                sinA = Math.sin( alpha );
                cosB = Math.cos( beta );
                sinB = Math.sin( beta );
                
                pos.x = this.x + len * cosA * sinB;
                pos.y = this.y + len * sinA * sinB;
                pos.z = this.z + len *        cosB;
                
                if( pos.x*pos.x + pos.y*pos.y + pos.z*pos.z < this.squareRange ){
                
                    passedExisting = true;
                    passedBuffered = true;
                    for( var i = 0; i < this.connections.length; ++i )
                        if( squareDist( pos, this.connections[ i ] ) < this.squareAllowed )
                            passedExisting = false;

                    if( passedExisting )
                        for( var i = 0; i < links.length; ++i )
                            if( squareDist( pos, links[ i ] ) < this.squareAllowed )
                                passedBuffered = false;

                    if( passedExisting && passedBuffered )
                        links.push( { x: pos.x, y: pos.y, z: pos.z } );
                    
                }
                
            }
            
            if( links.length === 0 )
                this.isEnd = true;
            else {
                for( var i = 0; i < links.length; ++i ){
                    
                    var pos = links[ i ],
                            connection = new Connection( pos.x, pos.y, pos.z, this.size * this.opts.sizeMultiplier );
                    
                    this.links[ i ] = connection;
                    this.all.push( connection );
                    this.connections.push( connection );
                }
                for( var i = 0; i < this.links.length; ++i )
                    this.toDevelop.push( this.links[ i ] );
            }
        }
        Connection.prototype.step = function(){
            
            this.setScreen();
            this.screen.color = ( this.isEnd ? this.opts.endColor : this.opts.connectionColor ).replace( 'light', 30 + ( ( this.tick * this.glowSpeed ) % 30 ) ).replace( 'alp', .2 + ( 1 - this.screen.z / this.mostDistant ) * .8 );
            
            for( var i = 0; i < this.links.length; ++i ){
                this.ctx.moveTo( this.screen.x, this.screen.y );
                this.ctx.lineTo( this.links[ i ].screen.x, this.links[ i ].screen.y );
            }
        }
        Connection.rootStep = function(){
            this.setScreen();
            this.screen.color = this.opts.rootColor.replace( 'light', 30 + ( ( this.tick * this.glowSpeed ) % 30 ) ).replace( 'alp', ( 1 - this.screen.z / this.mostDistant ) * .8 );
            
            for( var i = 0; i < this.links.length; ++i ){
                this.ctx.moveTo( this.screen.x, this.screen.y );
                this.ctx.lineTo( this.links[ i ].screen.x, this.links[ i ].screen.y );
            }
        }
        Connection.prototype.draw = function(){
            this.ctx.fillStyle = this.screen.color;
            this.ctx.beginPath();
            this.ctx.arc( this.screen.x, this.screen.y, this.screen.scale * this.size, 0, this.Tau );
            this.ctx.fill();
        }

        //espacio
        Data.prototype.reset = function(){
            
            this.setConnection( this.connections[ 0 ] );
            this.ended = 2;
        }
        Data.prototype.step = function(){
            
            this.proportion += this.speed;
            
            if( this.proportion < 1 ){
                this.x = this.ox + this.dx * this.proportion;
                this.y = this.oy + this.dy * this.proportion;
                this.z = this.oz + this.dz * this.proportion;
                this.size = ( this.os + this.ds * this.proportion ) * this.opts.dataToConnectionSize;
            } else 
                this.setConnection( this.nextConnection );
            
            this.screen.lastX = this.screen.x;
            this.screen.lastY = this.screen.y;
            this.setScreen();
            this.screen.color = this.opts.dataColor.replace( 'light', 40 + ( ( this.tick * this.glowSpeed ) % 50 ) ).replace( 'alp', .2 + ( 1 - this.screen.z / this.mostDistant ) * .6 );
            
        }
        Data.prototype.draw = function(){
            
            if( this.ended )
                return --this.ended; // not sre why the thing lasts 2 frames, but it does
            
            this.ctx.beginPath();
            this.ctx.strokeStyle = this.screen.color;
            this.ctx.lineWidth = this.size * this.screen.scale;
            this.ctx.moveTo( this.screen.lastX, this.screen.lastY );
            this.ctx.lineTo( this.screen.x, this.screen.y );
            this.ctx.stroke();
        }
        Data.prototype.setConnection = function( connection ){
            
            if( connection.isEnd )
                this.reset();
            
            else {
                
                this.connection = connection;
                this.nextConnection = connection.links[ connection.links.length * Math.random() |0 ];
                
                this.ox = connection.x; // original coordinates
                this.oy = connection.y;
                this.oz = connection.z;
                this.os = connection.size; // base size
                
                this.nx = this.nextConnection.x; // new
                this.ny = this.nextConnection.y;
                this.nz = this.nextConnection.z;
                this.ns = this.nextConnection.size;
                
                this.dx = this.nx - this.ox; // delta
                this.dy = this.ny - this.oy;
                this.dz = this.nz - this.oz;
                this.ds = this.ns - this.os;
                
                this.proportion = 0;
            }
        }
        Connection.prototype.setScreen = Data.prototype.setScreen = function(){
            
            var x = this.x,
                    y = this.y,
                    z = this.z;
            
            // apply rotation on X axis
            var Y = y;
            y = y * this.cosX - z * this.sinX;
            z = z * this.cosX + Y * this.sinX;
            
            // rot on Y
            var Z = z;
            z = z * cosY - x * this.sinY;
            x = x * cosY + Z * this.sinY;
            
            this.screen.z = z;
            
            // translate on Z
            z += this.opts.depth;
            
            this.screen.scale = this.opts.focalLength / z;
            this.screen.x = this.opts.vanishPoint.x + x * this.screen.scale;
            this.screen.y = this.opts.vanishPoint.y + y * this.screen.scale;
            
        }

        window.addEventListener( 'resize', function(){
            
            this.opts.vanishPoint.x = ( w = c.width = window.innerWidth ) / 2;
            this.opts.vanishPoint.y = ( h = c.height = window.innerHeight ) / 2;
            this.ctx.fillRect( 0, 0, w, h );
        });
        window.addEventListener( 'click', init );  
        
    }
}
</script> 
<style>
    canvas {position: absolute;top: 0;left: 0;}
</style>