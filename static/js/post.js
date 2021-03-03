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
                    <div class="comment-user"><strong>${response.commenter}</strong><span>time</span></div>
                    <div style="word-break:break-all; margin-right: 3vmin;">${response.comment}</div></div></div>
                    `)
                $('#comment-form')[0].reset();
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