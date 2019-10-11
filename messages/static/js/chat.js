$(function(){
    
    const ws_scheme = window.location.protocol === "https:" ? "wss":"ws";
    const ws_path = ws_scheme + "://" + window.location.host + "/ws/"+ currentUser +"/"
    const ws = new ReconnectingWebSocket(ws_path)
    //监听后端发送过来的消息
    ws.onmessage = function(event){
        const data = JSON.parse(event.data);
        var html = '<div style="border:solid 1px; margin:10px;"><p>'+data['sender']+' |' +data['message']+'</p><p>'+data['created_at']+'</p></div>'
        //$(".send_message").before(html);
        if (data['sender'] === activeUser){
            $(".send_message").before(html);

        }
    }

});
