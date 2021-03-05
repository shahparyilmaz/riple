$(document).ready(function(){
    $('#post').click(function(){
    })
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $('#comment-btn').click(function(e){
        e.preventDefault();
        var comment = $('#comment-content').val();
        var username =  $('#comment-form').data('username');
        var id = $('#comment-form').data('id');
        //var serializedData = $('#comment-form').serialize()
        console.log(comment,username,id)
        $.ajax({
            url:'/add_comment/'+username+'/'+id,
            data:{
                csrfmiddlewaretoken: csrfToken,
                username : username,
                id : id,
                comment : comment
            },
            method:'POST',
            success:function(response){
                console.log('adding comment')
                $('#allComments').append(`<div class="comment-line"><div class="comment-img-container">
                    <img src="${response.commenter_pic}" alt=""></div><div class="usernameandcomment">
                    <div class="comment-user"><strong class="comment-username">${response.commenter}</strong><span class="comment-date">now</span></div>
                    <div class="comment-content" style="word-break:break-all; margin-right: 3vmin;">${response.comment}</div></div></div>
                    `)
                $('#comment-form')[0].reset();
                document.getElementById('commentcount').innerText = parseInt(document.getElementById('commentcount').innerText) + 1
            }
        })
    })

    $('#likebtn').click(function(e){
        e.preventDefault();
        var poster = $(this).data('username');
        var post_id = $(this).data('postid');
        $.ajax({
            url : '/likeunlike/' + poster + '/' + post_id,
            data : {
                csrfmiddlewaretoken : csrfToken,
                post_user : poster,
                post_id : post_id
            },
            method : 'GET',
            success : function(response){
                var icon = document.getElementById('likebtn')
                if(icon.className=="bi bi-heart-fill likebtn"){
                    icon.classList[0].remove;
                    icon.setAttribute('class','bi bi-heart likebtn')
                }
                else if(icon.className=="bi bi-heart likebtn"){
                    icon.classList[0].remove;
                    icon.setAttribute('class','bi bi-heart-fill likebtn')
                }
                document.getElementById('likecount').innerText=response.likes
            }
        })
    })
})

/*
{
                console.log('success')
                $('#allComments').append('<div class="comment-line"><div class="comment-img-container">
                    <img src="{{response.commenter.profile.profile_pic.url}}" alt=""></div><div class="usernameandcomment">
                    <div class="comment-user"><strong>response.commenter</strong><span>time</span></div>
                    <div style="word-break:break-all; margin-right: 3vmin;">" + response.comment + "</div></div></div>')
            }
*/