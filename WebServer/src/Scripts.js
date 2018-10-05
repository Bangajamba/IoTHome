var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent
// IoTBroker
var jsonNodes = "";
const defaultNodes = '{"MQTT":[{"ID": 0, "name": "TestNode", "pubTopic": "TestNode/Out", "subTopic": "TestNode/In", "lastSendMsg": "", "lastReceivedMsg": ""}, {"ID": 1, "name": "TestNode1", "pubTopic": "TestNode1/Out", "subTopic": "TestNode1/In", "lastSendMsg": "", "lastReceivedMsg": ""}, {"ID": 2, "name": "TestNode2", "pubTopic": "TestNode2/Out", "subTopic": "TestNode2/In", "lastSendMsg": "", "lastReceivedMsg": ""}]}';
const updateTime = 10000; // Swap solution in future

var events = [];
var eventSrc = [];
var eventDes = [];

// SpeechRecognizer
var grammar = '#JSGF V1.0; grammar colors; public <color> = aqua | azure | beige | bisque | black | blue | brown | chocolate | coral | crimson | cyan | fuchsia | ghostwhite | gold | goldenrod | gray | green | indigo | ivory | khaki | lavender | lime | linen | magenta | maroon | moccasin | navy | olive | orange | orchid | peru | pink | plum | purple | red | salmon | sienna | silver | snow | tan | teal | thistle | tomato | turquoise | violet | white | yellow ;'
var recognition = new SpeechRecognition();
var speechRecognitionList = new SpeechGrammarList();
speechRecognitionList.addFromString(grammar, 1);
recognition.grammars = speechRecognitionList;
//recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

function send(command, msg){
    var client = new XMLHttpRequest();
    client.open('POST', 'http://localhost:8080', false)
    client.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    client.onreadystatechange = function()
    {
        // console.log(client.responseText);
    }

    var newMsg = createMsg(command, msg);
    console.log(newMsg);
    client.send(newMsg); 
}

function createMsg(command, msg)
{
    var packet = {};//= command + "," + msg
    packet.command = command;
    packet.msg = msg;
    return JSON.stringify(packet);
}

function startGetNodes(){
    try
    {
        getNodes();
        console.log(jsonNodes);
        //setInterval(getNodes, updateTime);
    }
    catch(err)
    {
        console.log(jsonNodes);
        jsonNodes = JSON.parse(defaultNodes);
    }

    createNodes()
    createEvents()
}

function getNodes(){
    var client = new XMLHttpRequest();
    client.open('POST', 'http://localhost:8080', false)
    client.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    client.onreadystatechange = function()
    {
        //console.log(client.responseText);
        jsonNodes = JSON.parse(client.responseText);
    }

    var newMsg = createMsg("GetNodes", "");
    //console.log(newMsg);
    client.send(newMsg); 
}

function createNodes(){

    // Show List
    var result = ""
    for (var i = 0; i < jsonNodes['MQTT'].length; i++)
    {
        result += jsonNodes['MQTT'][i].name + "</br>";
    }
    document.getElementById("ShowDiv").innerHTML = result;

    // Add
    var inputAddElement = document.createElement("INPUT");
    inputAddElement.id = "addInput";
    var btnAddElement = document.createElement("BUTTON");
    btnAddElement.innerHTML = "Add";
    btnAddElement.onclick = function()
    {
        send("Add", document.getElementById("addInput").value)
    };

    document.getElementById("AddDiv").appendChild(inputAddElement);
    document.getElementById("AddDiv").appendChild(btnAddElement);

    // Remove
    var dropdownRemove = document.createElement("SELECT");
    dropdownRemove.id = "removeDropdown"
    for (var i = 0; i < jsonNodes['MQTT'].length; i++)
    {
        var node = document.createElement("option");
        node.innerText = jsonNodes['MQTT'][i]['name'];
        dropdownRemove.appendChild(node);
    }

    var btnRemoveElement = document.createElement("BUTTON");
    btnRemoveElement.innerHTML = "Remove";
    btnRemoveElement.onclick = function()
    {
        send("Remove", document.getElementById("removeDropdown").value)
    };

    document.getElementById("RemoveDiv").appendChild(dropdownRemove);
    document.getElementById("RemoveDiv").appendChild(btnRemoveElement);

    // Test Publish
    var dropdownTest = document.createElement("SELECT");
    dropdownTest.id = "testDropdown"
    for (var i = 0; i < jsonNodes['MQTT'].length; i++)
    {
        var node = document.createElement("option");
        node.innerText = jsonNodes['MQTT'][i]['name'];
        dropdownTest.appendChild(node);
    }

    var inputTestElement = document.createElement("INPUT");
    inputTestElement.id = "testInput";

    var btnTestElement = document.createElement("BUTTON");
    btnTestElement.innerHTML = "Test";
    btnTestElement.onclick = function()
    {
        send("Test", document.getElementById("testDropdown").value + "," + document.getElementById("testInput").value)
    };

    document.getElementById("TestDiv").appendChild(dropdownTest);
    document.getElementById("TestDiv").appendChild(inputTestElement);
    document.getElementById("TestDiv").appendChild(btnTestElement);
};

function createEvents()
{
    // Src
    //div = document.getElementById("SrcSchedule")
    /*
    textElement = document.createElement("TEXT")
    textElement.innerHTML = "Choose Trigger:"
    
    radioNode = document.createElement("INPUT")
    radioTimer = document.createElement("INPUT")
    radioSpeech = document.createElement("INPUT")
    radioNode.setAttribute("type", "radio");
    radioTimer.setAttribute("type", "radio");
    radioSpeech.setAttribute("type", "radio");
    radioNode.name = "srcRadio"
    radioTimer.name = "srcRadio"
    radioSpeech.name = "srcRadio"
    NodeLabel = document.createElement("TEXT")
    NodeLabel.innerHTML = "Node"
    TimerLabel = document.createElement("TEXT")
    TimerLabel.innerHTML = "Timer"
    SpeechLabel = document.createElement("TEXT")
    SpeechLabel.innerHTML = "Speech"

    div.appendChild(textElement);
    div.appendChild(document.createElement("BR"))
    div.appendChild(radioNode);
    div.appendChild(NodeLabel)
    div.appendChild(document.createElement("BR"))
    div.appendChild(radioTimer);
    div.appendChild(TimerLabel)
    div.appendChild(document.createElement("BR"))
    div.appendChild(radioSpeech);
    div.appendChild(SpeechLabel)
    */

    // Node Src
    divNode = document.getElementById("SrcEventNode")
    var dropdownNode = document.createElement("SELECT");
    dropdownNode.id = "EventNodeDropdown"
    for (var i = 0; i < jsonNodes['MQTT'].length; i++)
    {
        var node = document.createElement("option");
        node.innerText = jsonNodes['MQTT'][i]['name'];
        dropdownNode.appendChild(node);
    }
    var inputSrcNode = document.createElement("INPUT")
    inputSrcNode.id = "inputSrcNode"
    inputSrcNode.placeholder = "trigger message"

    divNode.appendChild(dropdownNode)
    divNode.appendChild(inputSrcNode)

    // Timer Src

    // Speech Src
    divSpeech = document.getElementById("SrcEventSpeech")
    var inputSrcSpeech = document.createElement("INPUT")
    inputSrcSpeech.id = "inputSrcSpeech"
    inputSrcSpeech.placeholder = "voice message"
    divSpeech.appendChild(inputSrcSpeech)

    // Des
    var dropdownDes = document.createElement("SELECT");
    dropdownDes.id = "desDropdown"
    for (var i = 0; i < jsonNodes['MQTT'].length; i++)
    {
        var node = document.createElement("option");
        node.innerText = jsonNodes['MQTT'][i]['name'];
        dropdownDes.appendChild(node);
    }

    var inputDesElement = document.createElement("INPUT");
    inputDesElement.id = "desInput";
    inputDesElement.placeholder = "Message to sent";

    var btnDesElement = document.createElement("BUTTON");
    btnDesElement.innerHTML = "Add";
    btnDesElement.onclick = function()
    {
        des = {}
        des.nodeId = document.getElementById("desDropdown").value
        des.payloadMsg = document.getElementById("desInput").value
        eventDes.push(des)  
        //document.getElementById("desInput").value = "";
        updateEventList(); 
    };

    desDiv = document.getElementById("DesEvent")
    desDiv.appendChild(dropdownDes)
    desDiv.appendChild(inputDesElement)
    desDiv.appendChild(btnDesElement)
}

function setupMic(){
    document.getElementById("mic").onclick = function() {
        recognition.start();
        console.log('Listen for commands...');
    }

    recognition.onresult = function(event) {
        send("SpeechCall", event.results[0][0].transcript);
        console.log(event.results[0][0].transcript);
    }
}

function changeTriggerEvent(myRadio){

    divNode = document.getElementById("SrcEventNode")
    divTimer = document.getElementById("SrcEventTimer")
    divSpeech = document.getElementById("SrcEventSpeech")
    divNode.style.display = "none";
    divTimer.style.display = "none";
    divSpeech.style.display = "none";
    if(myRadio.value == "Node"){
        divNode.style.display = "block";
    }
    else if(myRadio.value == "Timer"){
        divTimer.style.display = "block";
    }
    else if(myRadio.value == "Speech"){
        divSpeech.style.display = "block";
    }
}

function addSourceTrigger(){
    var value = document.querySelector('input[name="srcRadio"]:checked').value;
    var src = {}
    src.type = value
    var nameElement = document.getElementById("SrcEventInput");
    src.name = nameElement.value
    nameElement.value = ""
    if(value == "Node"){
        src.nodeId = document.getElementById("EventNodeDropdown").value
        src.triggerMsg = document.getElementById("inputSrcNode").value
    }
    else if(value == "Timer"){

    }
    else if(value == "Speech"){
        src.voiceMsg = document.getElementById("inputSrcSpeech").value
    }

    eventSrc.push(src)
    updateEventList()
}

function updateEventList(){

    srcResult = "Src<br>"
    for (var i = 0; i < eventSrc.length; i++)
    {
        srcResult += eventSrc[i].name + "<br>";
    }
    document.getElementById("SrcNodes").innerHTML = srcResult;



    desResult = "Des<br>"
    for (var i = 0; i < eventDes.length; i++)
    {
        desResult += eventDes[i].nodeId + " " + eventDes[i].payloadMsg + "<br>";
    }
    document.getElementById("DesNodes").innerHTML = desResult;
}

function addEvent(){
    
    if (eventSrc.length == 0 || eventDes.length == 0)
    {
        alert("Src and Des can't be empty")
        return;
    }
    var event = {};
    event.src = eventSrc;
    event.des = eventDes;
    eventSrc = [];
    eventDes = [];
    updateEventList();

    events.push(event)
    console.log(event)
    send("AddEvent", event)
}