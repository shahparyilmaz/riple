$(document).ready(function(){


    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    $('#likebtn').click(function(){
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
                var icon = document.getElementById('likeicon')
                if(icon.className=="bi bi-heart-fill"){
                    icon.classList[0].remove;
                    icon.setAttribute('class','bi bi-heart')
                }
                else if(icon.className=="bi bi-heart"){
                    icon.classList[0].remove;
                    icon.setAttribute('class','bi bi-heart-fill')
                }
                document.getElementById('likeCount').innerText=response.likes
            }
        })
    })
})