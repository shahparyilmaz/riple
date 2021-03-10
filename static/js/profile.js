var csrfToken = $("input[name=csrfmiddlewaretoken]").val();


$('#followers').click(function(){
    $('#followerslist').css({'display':'flex'})
    $('#followinglist').css({'display':'none'})
    document.querySelectorAll('.selected').forEach(part => {
        part.classList.remove('selected')
    })
    document.getElementById('followers').classList.add('selected')
})
$('#following').click(function(){
    $('#followerslist').css({'display':'none'})
    $('#followinglist').css({'display':'flex'})
    document.querySelectorAll('.selected').forEach(part => {
        part.classList.remove('selected')
    })
    document.getElementById('following').classList.add('selected')
})

$('.unfollowbtn').click(function(e){
    e.preventDefault();
    userid = $(this).data('userid')
    var unfollowbtn=$(this)
    $.ajax({
        url:'/unfollow/'+userid,
        data:{
            csrfmiddlewaretoken : csrfToken,
        },
        method:'POST',
        success:function(response){
            unfollowbtn.text('Unfollowed')
        }
    })
})
$('.removebtn').click(function(e){
    e.preventDefault();
    userid = $(this).data('userid')
    var removebtn=$(this)
    $.ajax({
        url:'/removefollower/'+userid,
        data:{
            csrfmiddlewaretoken : csrfToken,
        },
        method:'POST',
        success:function(response){
            removebtn.text('Removed')
        }
    })
})
