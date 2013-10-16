function btnClick(){
    var user = $("#txtUser").val();
    var email= $("#txtEmail").val();
    var content = $("#txtContent").val().replace(/\n/g,"<br/>");
    
    var ret = submit_valid(user, email, content);
    switch(ret)
    {
        case 1:
            $("#divWarning").html("昵称不得为空");
            break;
        case 2:
            $("#divWarning").html("邮箱不得为空");
            break;
        case 3:
            $("#divWarning").html("评论内容不得为空");
            break;
        case 4:
            $("#divWarning").html("邮箱格式错误");
            break;
        case 5:
            $("#divWarning").html("内容长度不得低于5个字");
            break;
        default:
            $("#txtUser").val("");
            $("#txtEmail").val("");
            $("#txtContent").val("");
            $.post("{% url 'blog.views.show_blog' blog.id %}",
                    {"user":user,"email":email,"content":content},
                    function(data){
                        if(data){
                            $("#divComment").append("<div class='row'><div class='span2 text-info'>"+user+"</div><div class='span2 offset2 muted text-right'><p>"+data+"</p></div></div><br/><div class='row'><div class='span6'>"+content+"</div></div><br/><hr/>");
                        }
                        else{
                            alert("评论提交失败！");
                        }
                    });
            break;
    }

}

function submit_valid(user, email, content){    //验证输入
    if(!user)   //用户名非空
    {
        return 1;
    }
    if(!email)  //email非空
    {
        return 2;
    }
    var re = /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/;
    if(!re.test(email)) //邮箱格式
    {
        return 4;
    }
    if(!content)    //内容非空
    {
        return 3;
    }
    if(content.length<5)    //内容长度
    {
        return 5;
    }
    return 0;   //验证成功
}
