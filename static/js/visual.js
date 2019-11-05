width = 200;
height = 300;
function getNewRenderer(width,height) {
    var renderer0 = new THREE.WebGLRenderer({
        antialias : true
    });
    renderer0.setSize(width, height);
    return renderer0;
}
function initThree(obj,id,width,height) {
    obj.renderer = getNewRenderer(width,height);

    document.getElementById(id).appendChild(obj.renderer.domElement);

    // renderer1 = getNewRenderer(300,400);
    // document.getElementById('icanvas1').appendChild(renderer1.domElement);
    obj.renderer.setClearColor(0x000000, 1.0);
}


function initScene(obj) {
    obj.scene = new THREE.Scene();
}

///////相机
function initCamera(obj) {
    obj.camera = new THREE.PerspectiveCamera(45, width / height, 1, 10000);
    obj.camera.position.x = -30;
    obj.camera.position.y = 20;
    obj.camera.position.z = 80;
    obj.camera.lookAt(new THREE.Vector3(0,20,-30));

}

function initLight(obj) {
    obj.light = new THREE.SpotLight( 0xffffff );
    obj.light.position.set( -40, 60, -10 );
    obj.scene.add( obj.light );
}


var cube;
var curve;
function initObject(obj,arr) {
    var material1 = new THREE.LineBasicMaterial({
        color: '#2cff3e'
    });
    var material2 = new THREE.LineBasicMaterial({
        color: '#e86dff'
    });

    var i = 0;
    var j = 0;
    while(i < arr.length){
        j = 0;
        var geometry = new THREE.Geometry();
        while(j < arr[i].length){
            geometry.vertices.push(new THREE.Vector3(arr[i][j][1],
                arr[i][j][2],
                arr[i][j][3]));
            geometry.colors.push(new THREE.Color( 0xfefefe ));
            j++;
            flg = arr[i][j-1][0];
        }

        var material;
        if(parseInt(flg) === 3){
            material = material1;
        }
        else material = material2;
        var line = new THREE.Line( geometry, material );
        obj.scene.add( line );
        i++;
    }

    var geometry = new THREE.BoxGeometry(1, 1, 1);
    var material = new THREE.MeshLambertMaterial( { color: 0x00ff00} );
    cube = new THREE.Mesh( geometry, material );
    //scene.add( cube );
    // var g = new MeshLine();
    // g.setGeometry(createCurve(),function( p ) { return 1 - p; });
    // var material1 = new MeshLineMaterial({color:0x444444})
    // curve = new THREE.Mesh( g.geometry, material1 );
    // scene.add( curve );
}

function render(obj,id) {

    if (obj.renderEnabled) {
        obj.controls.update();
        obj.renderer.render(obj.scene, obj.camera );
    }

    // console.log(camera.position.x +" "
    //     + camera.position.y + " "
    //     + camera.position.z + "\n");
    requestAnimationFrame( function() {render(obj,id)} );
}
var mouse = new THREE.Vector2();
function onMouseMove( e ) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
}
function newframe(obj,id,arr) {
    //obj = new Object();
    obj.renderEnabled = false;
    initThree(obj,id,width,height);
    initScene(obj);
    initLight(obj);
    initCamera(obj);
    obj.controls = new THREE.TrackballControls( obj.camera,
                        obj.renderer.domElement);
    obj.controls.target = new THREE.Vector3(0,30,-20);
    obj.controls.update();
    obj.controls.rotateSpeed = 0.5;
    //obj.renderer.domElement.addEventListener('click', onMouseMove );
    //document.getElementById(id).addEventListener('click', onMouseMove );
    initObject(obj,arr);
    obj.renderer.clear();
    render(obj,id);
    obj.renderer.render(obj.scene, obj.camera );
}

function threeStart(ar,names) {
    //console.log(ar[0]);
    var ele = document.getElementById("picListDiv");

    for(var i = 0; i < ele.childNodes.length; i++){
        ele.removeChild(ele.childNodes[i]);
    }
    var i = 0;
    var objs = new Array();
    while (i < names.length){
        var div = document.createElement("div");
        div.setAttribute("class","canvas_frame");
        var canvas = document.createElement("div");
        canvas.setAttribute("id","canvas"+i.toString());


        var label = document.createElement("div");
        label.setAttribute("class","canvas_label");
        label.setAttribute("id","label"+i.toString());
        label.innerHTML = names[i];

        document.getElementById('picListDiv').appendChild(div);
        div.appendChild(canvas);
        div.appendChild(label);
        objs[i] = new Object();
        newframe(objs[i],"canvas"+i.toString(),
            ar[i]);  //创建新的webgl框架
        //console.log(objs[i].renderEnabled);


        document.getElementById("canvas"+i.toString()).onmouseover = function () {
            a = this.id.toString();
            iid = parseInt(this.id.substring(6,a.length));
            objs[iid].renderEnabled = true;
        }
        document.getElementById("canvas"+i.toString()).onmouseleave = function () {
            a = this.id.toString();
            iid = parseInt(this.id.substring(6,a.length));
            objs[iid].renderEnabled = false;
        }
        i++;
    }
}


function fileLoad(ar) { //ar : 点集  问题出在这个ar是字符串类型
    width = 400;
    height = 300;
    console.log(ar);
    obj = new Object();
    var ele = document.getElementById("picFiled");
    ele.removeChild(ele.childNodes[0]);
    var file = document.createElement("div");
    file.setAttribute("id","custom_file");
    ele.appendChild(file);
    newframe(obj,"custom_file",ar);  //创建新的webgl框架
    //console.log(objs[i].renderEnabled);



    document.getElementById("custom_file").onmouseover = function () {
        a = this.id.toString();
        iid = parseInt(this.id.substring(6,a.length));
        obj.renderEnabled = true;
    }
    document.getElementById("custom_file").onmouseleave = function () {
        a = this.id.toString();
        iid = parseInt(this.id.substring(6,a.length));
        obj.renderEnabled = false;
    }

    width = 200;
    height = 300;
}