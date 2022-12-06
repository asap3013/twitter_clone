$(document).on('click','#ttbtn',function(){
    debugger;
    let context = document.getElementById('tweet_content').value
    
    $.ajax({
        type:'POST',
        url:"/tweets",
        data:{
           content :context 
        },
        dataType:'json',
        success:function(response){
            console.log(response[0].content)
            $("#a_tweet").html(response[0].content)
           $(".post_body").empty();
            {let item_content = '<div class="post_body"><div class="post__header"><div class="post__headerText"><h3>'+ response[0].name+'<span class="post__headerSpecial"><span class="material-icons post__badge"> verified </span>@somanathg</span></h3></div><div class="post__headerDescription"><p>'+response[0].content+'</p></div></div><img src="https://www.focus2move.com/wp-content/uploads/2020/01/Tesla-Roadster-2020-1024-03.jpg" alt=""/><div class="post__footer"><span class="material-icons"> repeat </span><span class="material-icons"> favorite_border </span><span class="material-icons"> publish </span></div></div></div>'
            $(".post_body").append(item_content)
        }},
      failure: function() {console.log("Error!");}
        
    });
    // e.preventDefault();
    return false;
});
