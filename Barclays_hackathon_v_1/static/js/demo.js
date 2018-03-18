
//$(document).ready(function() {
    var $chatInput = $('#alme-input-field'),
    $loading = $('.loader');
    var dialog = "initial"; // initial-0 is for greeting 
    
    var url='';
    var intent=''
    function converse(values) {
        
        var query = ($chatInput.val());
        
        if (values!='') {
            //code
            query=values;
        }
        
        if (query=='' || query==' ') {
            alert('give some text');
        }
        else{

            if (dialog!='live agent' && dialog!='live agent active') {
                //code
                showUserQuery(query);
                scrollChatToBottom();
            }
            
        $.ajax({
            url: '/getAnswer',
            method: 'GET',
            
            data: { query: query,dialog:dialog,intent:intent},
            success: function(data) {
                console.log(data);
                var i=0;
                next();
                function next() {
                    setTimeout(function() {
                    if (i == data.response.length) {
                        return;
                    }
                    var $chatBox = $('#botReplyDiv').clone().prop('id',"botdiv"+data.id);
                        var $loading = $('.loader');
                        $chatBox.css("display", "block");

                        var ul  = document.createElement('ul');
                        var li=document.createElement('li');
                        li.appendChild(parseHTML(data.response[i]));
                        ul.appendChild(li);
                        $chatBox.find('p').html($('<p/>').html(ul));
                        $('#alme-chat-history').append($chatBox);
                        $chatBox.insertBefore($loading);
                        scrollChatToBottom();
                    // Do what you need to do   
                    i++;
                    next();
                }, 3000);
            }
                
                dialog = data.dialog;
                intent=data.intent;
                if(data.status ==true){
                    collectFeedback(data.id);
                }
                
                if (data.dialog=='live agent') {
                    //code
                    dialog='live agent active';
                    converse('live agent');
                }
            }
            
        });
        scrollChatToBottom();
        $chatInput.val("");
        return true;
    }
    }

function parseHTML(text1)
{
        var p=document.createElement('p');
        p.innerHTML=text1;
        return p;
}
function showUserQuery(query){
     var $chatBox = $('#userInputDiv').clone();
        var $loading = $('.loader');
        $chatBox.css("display", "block");
        $chatBox.find('p').html($('<p/>').html(query).text());
        $('#alme-chat-history').append($chatBox);
        $chatBox.insertBefore($loading);
        
}

function showBotReply(reply,id){
    var $chatBox = $('#botReplyDiv').clone().prop('id',"botdiv"+id);;
        var $loading = $('.loader');
        $chatBox.css("display", "block");
        for (i=0;i<reply.length;i++) {
            //code
            $chatBox.find('p').html($('<p/>').append(reply[i]));
        }
        //$chatBox.find('p').html($('<p/>').html(reply));
        
        $('#alme-chat-history').append($chatBox);
        $chatBox.insertBefore($loading);
        
}

function scrollChatToBottom(){
      
    var element = $('#alme-chat-history');
    element.animate({scrollTop: element[0].scrollHeight}, 800);
 
}

function resolveAmbiguousQuery(id,selection ){
    $.ajax({
            url: "/resolveAmbiguousQuery",
            method: 'GET',
            
            data: { id: id,selection:selection },
            success: function(data) {
                //if(data.response=="done")
                //$("#div"+id).hide("slow");
            }
        });
    
    $chatInput.val(selection );
    converse('');
}
$("#alme-input-form").submit(function(event) {
        converse('');

        event.preventDefault();
    });
    
    function speak(text){
        var msg = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(msg);
    }
    