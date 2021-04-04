$(function() {
    $('.ui.dropdown').dropdown();
});

$('.ui.checkbox')
    .checkbox()
;


$('.ui.modal')
    .modal('show')
;
let map = L.map('map').setView([46.3223 , 2.2549], 6);

// Theme URL format in XYZ PNG format; see our themes documentation for more options
L.tileLayer('https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png?api_key=2dfe87d3-d850-40b9-ba36-de6937681f4a', {
    maxZoom: 20,
    attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org">OpenMapTiles</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
}).addTo(map);

let markerGroup = new L.MarkerClusterGroup();
map.addLayer(markerGroup)

let mapper = {
    "Paris":[48.8534, 2.3488],
    "Rennes":[48.11198,-1.67429],
    "All":[46.3223 , 2.2549],
    "Lyon":[45.764043, 4.835659]
}

let zoom = {
    "Paris":13,
    "Rennes":15,
    "All":6,
    "Lyon":14
}

let cache = {}



let network = "All"
function selector(name){
    network = name
    document.getElementById("ok")
    for(elem of document.getElementsByClassName("network")){
        if (elem.innerText.includes(name)){
            network = name
            elem.classList.add("blue")
        }else{
            elem.classList.remove("blue")
        }
    }
    const pos = mapper[name]
    map.panTo(new L.LatLng(pos[0], pos[1]));
    map.setZoom(zoom[name])
    document.getElementById("cities").innerHTML = cache[name]
}

const coreQuery = () => {
    const vals = $('.ui.dropdown').dropdown('get values')
    let initial = `filter regex(?net, "${network}") . `
    if(network === 'All'){
        initial = ""
    }
    let citieslist = 'filter regex(?city,  "'
    if(vals.length > 0){
        for(const elem of vals){
            citieslist += elem+"|"
        }
        return initial + citieslist.slice(0,-1)+'") . '
    }
    return initial
}

let initCache = async () => {
    for(const city of ["Paris", "Lyon", "Rennes"]){
        const temp = await query(`PREFIX ex: <http://example.org/> prefix ns1:   <http://dbpedia.org/ontology/> SELECT distinct ?city WHERE {  ?id ns1:network ?net . filter(?net = "${city}") .  ?id ns1:city ?city . }`)
        cache[city] = ""
        for(elem of temp.results.bindings){
            cache[city] += `<option value="${elem.city.value}">${elem.city.value}</option>`
        }
    }
    cache.all = cache["Paris"]+cache["Lyon"]+cache["Rennes"]
    document.getElementById("cities").innerHTML = cache["all"]
}


let query = async (query) => {
    return await $.ajax({
        dataType: "jsonp",
        url: "http://localhost:3030/DataminingProject",
        data: {
            "query": query,
            "output": "json"
        },
    }).then(res => {
        return (res)
    })
}

const queryBase = `prefix ns1: <http://dbpedia.org/ontology/> 
    prefix ns2: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    prefix ns3: <http://example.org/> 
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    select ?city ?bikes ?ebikes ?total ?adocks ?docks ?label ?lat ?long  where{
    ?id ns1:city ?city .
    ?id ns3:bikes ?bikes .
    ?id ns3:ebikes ?ebikes .
    ?id ns3:available ?adocks .
    ?id ns3:total ?total .
    ?id ns3:docks ?docks .
    ?id rdfs:label ?label .
    ?id ns2:lat ?lat .
    ?id ns2:long ?long .
    ?id ns1:network ?net . `.replace('\t','').replace('\n','')

const rentBike= async () => {
    document.getElementById("rent").classList.add("loading")
    var querytext = queryBase
    querytext+=coreQuery()
    let quantity = 0
    if(Number.isInteger(parseInt(document.getElementById("abikes").value))){
        quantity = Math.max(document.getElementById("abikes").value,0)
    }
    if($('.ui.checkbox').checkbox("is checked")[0] && !$('.ui.checkbox').checkbox("is checked")[1]){
        querytext += `filter (?ebikes >= ${quantity}) .`
    }
    if($('.ui.checkbox').checkbox("is checked")[1] && !$('.ui.checkbox').checkbox("is checked")[0]){
        querytext += `filter (?bikes >= ${quantity}) .`
    }

    if($('.ui.checkbox').checkbox("is checked")[1] === $('.ui.checkbox').checkbox("is checked")[0]){
        querytext += `filter (?total >= ${quantity}) .`
    }
    querytext+='}'
    console.log(querytext)
    const result = await query(querytext)
    populatemap(result)
    document.getElementById("rent").classList.remove("loading")
}

const populatemap = (res) => {
    markerGroup.clearLayers();
    for(const elem of res.results.bindings){
        const data = {
            label:elem.label.value,
            lat:elem.lat.value,
            long:elem.long.value,
            city:elem.city.value,
            bikes:elem.bikes.value,
            ebikes:elem.ebikes.value,
            totalstands:elem.docks.value,
            stands:elem.adocks.value
        }
        createMarker(data)

    }
}


const returnBike = async () => {
    document.getElementById("return").classList.add("loading")
    var querytext = queryBase
    querytext+=coreQuery()
    if(Number.isInteger(parseInt(document.getElementById("adocks").value))){
        quantity = Math.max(document.getElementById("adocks").value,0)
        querytext += `filter (?adocks >= ${quantity}) .`
    }

    if(Number.isInteger(parseInt(document.getElementById("ndock").value))){
        quantity = Math.max(document.getElementById("ndock").value,0)
        querytext += `filter (?docks >= ${quantity}) .`
    }
    querytext+='}'
    console.log(querytext)
    const result = await query(querytext)
    populatemap(result)
    document.getElementById("return").classList.remove("loading")
}

const createMarker = (data) => {
    var latLng = new L.LatLng(data.lat, data.long);
    var marker = new L.Marker(latLng);
    marker.bindPopup(`
    <h4>${data.label}</h4>
    <div><i class="bi bi-building"></i> city : ${data.city}</div>
    <div><i class="bi bi-bicycle"></i> bikes : ${data.bikes}</div>
    <div><i class="bi bi-lightning-charge"></i> ebikes : ${data.ebikes}</div>
    <div>stand available : ${data.stands}/${data.totalstands}</div>
    `)
    markerGroup.addLayer(marker)
}

initCache()