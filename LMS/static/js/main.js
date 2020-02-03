
$(document).ready(function(){
    
  })
    locations = [
        {
        "id":0,
        "text": "Andhra Pradesh",
        },
        {
        "id":1,
        "text": "Arunachal Pradesh",
        },
        {
        "id":2,
        "text": "Bihar",
        },
        {
        "id":3,
        "text": "Chhattisgarh",
        },
        {
        "id":4,
        "text": "Goa",
        },
        {
        "id":5,
        "text": "Gujarat",
        },
        {
        "id":6,
        "text": "Haryana",
        },
        {
        "id":7,
        "text": "Jammu and Kashmir",
        },
        {
        "id":8,
        "text": "Jharkhand",
        },
        {
        "id":9,
        "text": "Karnataka",
        },
        {
        "id":10,
        "text": "Kerala",
        },
        {
        "id":11,
        "text": "Madhya Pradesh",
        },
        {
        "id":12,
        "text": "Maharashtra",
        },
        {
        "id":13,
        "text": "Manipur",
        },
        {
        "id":14,
        "text": "Meghalaya",
        },
        {
        "id":15,
        "text": "Mizoram",
        },
        {
        "id":16,
        "text": "Nagaland",
        },
        {
        "id":17,
        "text": "Odisha",
        },
        {
        "id":18,
        "text": "Punjab",
        },
        {
        "id":19,
        "text": "Rajasthan",
        },
        {
        "id":20,
        "text": "Sikkim",
        },
        {
        "id":21,
        "text": "Tamil Nadu",
        },
        {
        "id":22,
        "text": "Telangana",
        },
        {
        "id":23,
        "text": "Tripura",
        },
        {
        "id":24,
        "text": "Uttarakhand",
        },
        {
        "id":25,
        "text": "Uttar Pradesh",
        },
        {
        "id":26,
        "text": "West Bengal",
        },
        {
        "id":27,
        "text": "Andaman and Nicobar Island",
        },
        {
        "id":28,
        "text": "Chandigarh",
        },
        {
        "id":29,
        "text": "Dadra and Nagar Haveli",
        },
        {
        "id":30,
        "text": "Daman and Diu",
        },
        {
        "id":31,
        "text": "Delhi",
        },
        {
        "id":32,
        "text": "Lakshadweep",
        },
        {
        "id":33,
        "text": "Puducherry",
        }





]
       

      occupation=[
        {
        "id":0,
        "text": "Student",
        },
        {
        "id":1,
        "text": "Employee",
        }]
      

    //   $("section").click(function(e){
    //     a = e.target.closest("section")
    //     a.attr('id')
    // });

      $("a[name='Messages']").click(function (e) {
        $.ajax({
        type: "GET",
        url:"/message",
        success: function(data){
           console.log(data)

        }
    });
});


function checkPassword() { 
    password1 = $('#password1').val()
    password2 = $('#password2').val()    
    console.log(password1)
    console.log(password2)
    if (password1 != password2) { 
        document.getElementById("message").innerHTML= "Passwords did not match" 
        document.getElementById('submitbutton').disabled = true
    }
    else {
        document.getElementById("message").innerHTML= "Passwords matched" 
        document.getElementById('submitbutton').disabled = false
    }
    } 




// grouping display 
   
window.onload = function() { 

    if($('#course_id').val() != null){
    courseid = $('#course_id').val()
    console.log(courseid)
        $.ajax ({
                url: "/groupsDisplay/",
                type: "GET",
                data:{"courseid":courseid},
            success: function(data){
               console.log(data)
               for (var i=0 ;i < data.length; i++){
                var user = data[i]['user__username']
                var  rewards= data[i]['rewards']     
                var user_id= data[i]['user_id']
                var lastActivity  = data[i]["lastActivity"]
                console.log(data[i]['user__username'])
                console.log(data)

                var badge = document.getElementById('mygroup');
                var span = document.createElement("div");
                if (lastActivity =='online')
                {
                    span.innerHTML = "<a style='font-weight: 100;' class='text-dark' target='_blank' href="+'/A2AQuestionUpload/' + courseid + '/' + user_id + '/'+ ">"+user+ "<i class='fas fa-circle online'></i></a>" 
                }
                else{
                    span.innerHTML = "<a style='font-weight: 100;' class='text-dark'  target='_blank' href="+'/A2AQuestionUpload/' + courseid + '/' + user_id + '/'+ ">"+user+ "</a>" 

                }
                badge.appendChild(span);
                   }   
            } 
                });
    }
    else{
        console.log("no group")
    }
    if ($("#timegiven").val() != null){

    var fiveMinutes = $("#timegiven").val()
        display = document.querySelector('#time');

    startTimer(fiveMinutes, display);
    }
    if ($("#editorr").val() !=undefined){
    var editor = ace.edit('editorr');
    editor.setTheme("ace/theme/solarized_lite");
    editor.getSession().setMode("ace/mode/" + $("#mode").val());
    editor.setShowPrintMargin(false);
    editor.setOptions({
    fontFamily: "monospace",
    fontSize: "10pt"
    })
    }
};         
//timer display
function startTimer(duration, display) {
    var timer = duration;
    setInterval(function () {   
        display.textContent = timer + " sec";
        $("#timeTaken").val(timer);
        if (--timer < 0){
            // timer = duration;
            document.getElementById("time").innerHTML = "Time expired";

        }    
        
    }, 1000);
    $("#TimeButton").click(function(){
        $.ajax ({
            url: "/TimeFunctionality/",
            type: "POST",
            data: {"time":timer,"questionid":$("#questionid").val()},
        }).done(function(data) {
            console.log(data)
        }// inner function
        )})
}


// if ($('editorr').val()!= null){

// }
function getCookie(name) {
   var cookieValue = null;
   if (document.cookie && document.cookie !== '') {
       var cookies = document.cookie.split(';');
       for (var i = 0; i < cookies.length; i++) {
           var cookie = cookies[i].trim();
           // Does this cookie string begin with the name we want?
           if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
   return cookieValue;
}

$("#run").click(function(){

    
        $.ajax ({
            url: "/compiler/",
            type: "POST",
            data: {"file":ace.edit('editorr').session.getValue()},
        }).done(function(data) {
            console.log(data)
            if (JSON.parse(data).errors == null){
                var o = JSON.parse(data).output
                console.log(o)
                try{
                    var result=o.join("")
                    document.getElementById("myresult").innerHTML = result;
                }
                catch(TypeError){

                    document.getElementById("myresult").innerHTML = o;
                }
            }
            else{
                var error = JSON.parse(data).errors
                document.getElementById("myresult").innerHTML = error;
            }

        }).fail(function(data, err) {
            alert("fail " + JSON.stringify(data) + " " + JSON.stringify(err));
        });
    
});


function testcase(number,id){
    problemid = $('#idd').val()
    currentuser = $('#currentuser').val()
    $.ajax ({
        url: "/testcase/",
        type: "POST",
        data: {"currentuser":currentuser,"file":ace.edit('editorr').session.getValue(),"number":number,"problemid":problemid, "timeTaken":$("#timeTaken").val()},
    }).done(function(data) {
        console.log(data)
        if (JSON.parse(data.output).errors == null){
            var verified = data.verified;
            console.log(verified)
            var status = JSON.parse(data.status);
            var res = JSON.parse(data.output).output;
            console.log(res)
            try{
                var result=res.join("")
                
                document.getElementById("myresult").innerHTML =  result;
                if (verified == "yes"){
                    alert("Wow!!!!! Its verified....")
                    document.getElementById(status).remove();

                }
                else{
                    alert("offoooo....Not verified.Try again!")
                }
            }
            catch(TypeError){
             
                document.getElementById("myresult").innerHTML = res;
            }
        }
        else{
            var err = JSON.parse(data.output).errors
            document.getElementById("myresult").innerHTML = err;
        }

    }).fail(function(data, err) {
        alert("fail " + JSON.stringify(data) + " " + JSON.stringify(err));
    });
}




function testcase(number,id){
    problemid = $('#idd').val()
    currentuser = $('#currentuser').val()
    $.ajax ({
        url: "/testcase/",
        type: "POST",
        data: {"currentuser":currentuser,"file":ace.edit('editorr').session.getValue(),"number":number,"problemid":problemid, "timeTaken":$("#timeTaken").val()},
    }).done(function(data) {
        console.log(data)
        if (JSON.parse(data.output).errors == null){
            var verified = data.verified;
            console.log(verified)
            var status = JSON.parse(data.status);
            var res = JSON.parse(data.output).output;
            console.log(res)
            try{
                var result=res.join("")
                
                document.getElementById("myresult").innerHTML =  result;
                if (verified == "yes"){
                    alert("Wow!!!!! Its verified....")
                    document.getElementById(status).remove();

                }
                else{
                    alert("offoooo....Not verified.Try again!")
                }
            }
            catch(TypeError){
             
                document.getElementById("myresult").innerHTML = res;
            }
        }
        else{
            var err = JSON.parse(data.output).errors
            document.getElementById("myresult").innerHTML = err;
        }

    }).fail(function(data, err) {
        alert("fail " + JSON.stringify(data) + " " + JSON.stringify(err));
    });
}

function saveProgram(){
    problemid = $('#idd').val()
    currentuser = $('#currentuser').val()
    $.ajax ({
        url: "/saveProblem/",
        type: "POST",
        data: {"currentuser":currentuser, "file":ace.edit('editorr').session.getValue(), "problemid":problemid},
    }).done(function(data) {
        if (JSON.parse(data).errors == null){
            alert("Program saved :)")
            
        }
        else{
            var err = JSON.parse(data.output).errors
            alert(err);
        }

    }).fail(function(data, err) {
        alert("fail " + JSON.stringify(data) + " " + JSON.stringify(err));
    });
}




// function tag(){
//     var a = window.open("https://ibastatic.sfo2.digitaloceanspaces.com/python/taggingPage.html")
//     var target = document.getElementById("405")
//     if( target ) {
//         event.preventDefault();
//         $('html, body').stop().animate({
//             scrollTop: target.offset().top
//         }, 1000);
//     }
// }










