$(document).ready(function(){


    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    $('.box').click(function(){
        var username = $(this).data('username');
        var postid = $(this).data('postid');
        $.ajax({
            url:'/likeunlike/' + username + '/' + postid,
            data:{
                csrfmiddlewaretoken: window.CSRF_TOKEN,
                post_user : username,
                post_id : postid
            },
            method : 'GET',
            success : function(response){
                var iconbox = $(`[data-likeid=${postid}]`)[0]
                var icon = iconbox.children[0]
                var likecount = $(`[data-likecountid=${postid}]`)[0]
                if(icon.className=="bi bi-heart-fill"){
                    icon.classList[0].remove;
                    icon.setAttribute('class','bi bi-heart')
                }
                else if(icon.className=="bi bi-heart"){
                    icon.classList[0].remove;
                    icon.setAttribute('class','bi bi-heart-fill')
                }
                likecount.innerText=response.likes
            }
        })
    })
})