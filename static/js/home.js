$(document).ready(function () {


    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    $('.box').click(function () {
        var username = $(this).data('username');
        var postid = $(this).data('postid');
        $.ajax({
            url: '/likeunlike/' + username + '/' + postid,
            data: {
                csrfmiddlewaretoken: window.CSRF_TOKEN,
                post_user: username,
                post_id: postid
            },
            method: 'GET',
            success: function (response) {
                var iconbox = $(`[data-likeid=${postid}]`)[0]
                var icon = iconbox.children[0]
                var likecount = $(`[data-likecountid=${postid}]`)[0]
                if (icon.className == "bi bi-heart-fill") {
                    icon.classList[0].remove;
                    icon.setAttribute('class', 'bi bi-heart')
                }
                else if (icon.className == "bi bi-heart") {
                    icon.classList[0].remove;
                    icon.setAttribute('class', 'bi bi-heart-fill')
                }
                likecount.innerText = response.likes
            }
        })
    })
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    $('#nextone').click(function (e) {
        var prev_user = document.getElementById('slide1username').innerText
        var other_user = document.getElementById('slide2username').innerText
        document.getElementById('followone').innerText='Follow'
        document.getElementById('requestone').innerText='Request'
        $.ajax({
            url: '/ajaxhome/' + prev_user,
            data: {
                csrfmiddlewaretoken: window.CSRF_TOKEN,
                username2:other_user
            },
            method: 'POST',
            success: function (response) {
                var newuserusername = response.randomuserusername;
                var newuserpicurl = response.randomuserpic;
                var newuserid = response.randomuserid;
                document.getElementById('slide1').innerHTML = `
                <a href="/user/${newuserusername}">
                    <div class="slide-user">
                        <div class="slide-img-container">
                            <img class="slide-img" src="${newuserpicurl}" alt="">
                        </div>
                        <div class="details">
                            <strong>First User</strong>
                            <br>
                            <span id="slide1username" data-userid="${newuserid}">${newuserusername}</span>
                            <br>
                            <i>Bio</i>
                        </div>
                    </div>
                </a>
                `
                console.log(newuserid)
                console.log(document.getElementById('slide1username').dataset.userid)
            }
        })
    })
    $('#nexttwo').click(function (e) {
        var prev_user = document.getElementById('slide2username').innerText
        var other_user = document.getElementById('slide1username').innerText
        document.getElementById('followtwo').innerText='Follow'
        document.getElementById('requesttwo').innerText='Request'
        $.ajax({
            url: '/ajaxhome/' + prev_user,
            data: {
                csrfmiddlewaretoken: window.CSRF_TOKEN,
                username2:other_user
            },
            method: 'POST',
            success: function (response) {
                var newuserusername = response.randomuserusername;
                var newuserpicurl = response.randomuserpic;
                var newuserid = response.randomuserid;            
                document.getElementById('slide2').innerHTML =`
                <a href="/user/${newuserusername}">
                <div class="slide-user">
                    <div class="slide-img-container">
                        <img class="slide-img" src="${newuserpicurl}" alt="">
                    </div>
                    <div class="details">
                        <strong>First User</strong>
                        <br>
                        <span id="slide2username" data-userid="${newuserid}">${newuserusername}</span>
                        <br>
                        <i>Bio</i>
                    </div>
                </div>
            </a>
                `
            }
        })
    })

    $('#followone').click(function(e){
        e.preventDefault();
        var followid = document.getElementById('slide1username').dataset.userid
        console.log(followid)
        $.ajax({
            url:'/follow/'+followid,
            data:{
                csrfmiddlewaretoken: window.CSRF_TOKEN,
            },
            method:'POST',
            success:function(response){
                var reqbtn=document.getElementById('followone')
                reqbtn.innerText='Following'
            }
        })
    })
    $('#followtwo').click(function(e){
        e.preventDefault();
        var followid = document.getElementById('slide2username').dataset.userid
        $.ajax({
            url:'/follow/'+followid,
            data:{
                csrfmiddlewaretoken: window.CSRF_TOKEN,
            },
            method:'POST',
            success:function(response){
                var reqbtn=document.getElementById('followtwo')
                reqbtn.innerText='Following'
            }
        })
    })
    $('#requestone').click(function(e){
        e.preventDefault();
        var reqid = document.getElementById('slide1username').dataset.userid
        $.ajax({
            url:'/follow_req/'+reqid,
            data:{
                csrfmiddlewaretoken: window.CSRF_TOKEN,
            },
            method:'POST',
            success:function(response){
                var reqbtn=document.getElementById('requestone')
                reqbtn.innerText='Requested'
            }
        })
    })
    $('#requesttwo').click(function(e){
        e.preventDefault();
        var reqid = document.getElementById('slide2username').dataset.userid
        $.ajax({
            url:'/follow_req/'+reqid,
            data:{
                csrfmiddlewaretoken: window.CSRF_TOKEN,
            },
            method:'POST',
            success:function(response){
                var reqbtn=document.getElementById('requesttwo')
                reqbtn.innerText='Requested'
            }
        })
    })
})