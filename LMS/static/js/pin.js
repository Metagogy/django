var module = angular.module('myApp', []);

function Main($scope,$http,$rootScope,$sce,$window){
    module.config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('{[{');
      $interpolateProvider.endSymbol('}]}');
    });


$scope.coursesList = function(){
       
        $http({
            method:"GET",

            url:"/coursesList/"
         }).then( function(response, status) {
                
                $scope.courseslist=angular.fromJson(response.data.courseslist)
                console.log($scope.courseslist)
        });

    }


    $scope.fetchData = function(){
        console.log($("#courseid").val())
		$http({
			method:"GET",

	     	url:"/chapt_topic_ajax/"+$("#courseid").val()+"/"
     	 }).then( function(response, status) {
	     		$rootScope.chapterslist=response.data.chapterslist
	     		$rootScope.topicslist=response.data.topicslist
	     		console.log($rootScope.chapterslist)
    	});

     }
    $scope.topicData = function(){
 		
 		a = $("#chapterselected").val()
	    $scope.alltopics=$rootScope.topicslist
	    $scope.topics = $scope.alltopics[a]
    }
    $scope.courseData = function(){
		$http({
			method:"GET",

	     	url:"/course_chapter_ajax/"+$("#course").val()+"/"
     	 }).then( function(response, status) {
	     		$rootScope.chapterslist=response.data.chapterslist
	     		
    	});

     }
    $scope.projectData = function(){

		$http({
			method:"GET",

	     	url:"/course_project_ajax/"+$("#courseselected").val()+"/"
     	 }).then( function(response, status) {
     	 		
	     		$rootScope.projectslist=response.data.projectslist
	     		
    	});

     }

    $scope.sampleData = function(){
		
		$http({
			method:"GET",

	     	url:"https://ibastatic.sfo2.digitaloceanspaces.com/python/100/101.html"
     	 }).then( function(response, status) {
	     		
	     		$scope.tata=$sce.trustAsHtml(response.data)
	     		console.log($scope.tata)
	     		
    	});

     }


    $scope.testLanding = function(){
    	$scope.first_ques = $("#first_ques").val()
    	$scope.first_answer = JSON.parse($("#first_ans").val())
    	$scope.test = $("#test").val()
    }

    $scope.pretest_validate=function(){

    	$scope.ansid=($("input[name='answer']:checked").val());
        if($scope.ansid != null ){
	    	$http({
				method:"GET",

		     	url:"/pretest_val/",
		     	params:{"submitted_ans":$scope.ansid}
	     	 }).then( function(response, status) {
	     	 	$("#baseQues").remove()
	     	 	if (response.data.next_ques){
					$scope.results=response.data
					console.log($scope.results)
					$scope.next_ques=$scope.results.next_ques
					$scope.answers=$scope.results.next_ans
				}else{
					$("#last").remove()
	     	 		$("#r").remove()
                    $scope.results=response.data
                    console.log($scope.results)
                    $scope.status=response.data.status
                    console.log($scope.status)
                    


				}
	    	});
   		}
   		else{
   			alert("select any answer");
   		}
 }
					
					
					


					
				
					
				

				

				


 	$scope.edit = function(){
        if ($("#result").val()){
 		    $scope.score = $("#result").val()
            $scope.code = $("#code").val()
            $scope.time = $("#time").val()

            console.log($scope.score)
            
        }
	 	$scope.editor = ace.edit("editor");
	    $scope.editor.setTheme("ace/theme/solarized_dark");
	    $scope.editor.session.setMode("ace/mode/" + $("#mode").val());
	    $scope.editor.setShowPrintMargin(false);
	    $scope.editor.setOptions({
	      fontFamily: "monospace",
	      fontSize: "15pt"
	    });
  
 	}

    $scope.testRun=function(){
    	
    	$scope.d=$scope.editor.session.getValue()
    	$http({
            method: "POST",
            url: "/testCode/",
            params: {"editorvalue":$scope.d},
            }).then( function(response, status) {
                $scope.output=response.data.output
                
                
                
               
                });
           
	}
	$scope.testAcrossTestcases=function(){
    	$scope.pblmid = $("#idd").val()
        $scope.compilerid=$("#compilerid").val()
        

        $http({
            method: "POST",
            url: "/pyExec/",
            params: {"compilerid":$scope.compilerid,"editorvalue":$scope.editor.session.getValue(),"pid":$scope.pblmid,"check":"check"},
            }).then( function(response, status) {
                $scope.output=response.data.output
                $scope.score=response.data.score
                $scope.testcases=response.data.testcases
                $scope.try_again=response.data.try_again
	        
	            });

        }


    $scope.submitCode=function(){
    	$scope.pblmid = $("#idd").val()
    	$scope.chapter= $("#chapter").val()
        $scope.compilerid=$("#compilerid").val()

        $http({
            method: "POST",
            url: "/pyExec/",
            params: {"compilerid":$scope.compilerid,"editorvalue":$scope.editor.session.getValue(),"pid":$scope.pblmid,"chapter":$scope.chapter},
            }).then( function(response, status) {
                $scope.output=response.data.output
                $scope.score=response.data.score
                $scope.testcases=response.data.testcases
                if (response.data.next_try){
                	$scope.next_try=response.data.next_try
                }
                else{
                	$scope.success=response.data.success
                }
               
                });       
    }
    $scope.testBegin=function(){
        
        $scope.course=$("#course").val()
        $scope.courseid=$("#courseid").val()
        console.log($scope.courseid)
        $scope.chapter=$("#chapter").val()
        $scope.page=$("#page").val()
        $scope.courseCat=$("#courseCat").val()
        console.log($scope.courseCat)
        $http({
            method: "GET",
            url: "/page/",
            params:{"courseid":$scope.courseid,"chapter": $scope.chapter,"page": $scope.page}
          }).then(function successCallback(response,status) {

                $scope.contentdata=response.data
                console.log($scope.contentdata)
                $scope.details=$scope.contentdata.contents
                console.log($scope.contentdata.questions)
                if ($scope.contentdata.questions == null){
                    $scope.cont=function(event){

                        $scope.link=$sce.trustAsResourceUrl("https://ibastatic.sfo2.digitaloceanspaces.com/"+$scope.courseCat+'/'+$scope.chapter+'/'+$scope.page+'.html')
                        console.log($scope.link)
                        // $http.get("https://ibastatic.sfo2.digitaloceanspaces.com/"+$scope.courseCat+'/'+$scope.chapter+'/'+$scope.page+'.html').then( function(response) {
                        // $scope.htmlcontent = $sce.trustAsHtml(response.data)
                        // console.log($scope.link)
                        // });
                    }();}   
                // $scope.htmlcontent=$scope.contentdata.contents
                $scope.prevchaptno=$scope.contentdata.previous.chaptno        
                $scope.nextchaptno=$scope.contentdata.next.chaptno        
                $scope.prevtopicno=$scope.contentdata.previous.topicno        
                $scope.nexttopicno=$scope.contentdata.next.topicno  
                if ($scope.contentdata.questions){
                    

                    $scope.question=$scope.contentdata.questions.question  
                    $scope.answers=$scope.contentdata.questions.answers
                    $scope.questions=$scope.contentdata.questions
                    $scope.count=$scope.questions.count
                    $scope.key=$scope.questions.key
                    $scope.id=$scope.questions.id
            }
          }, function errorCallback(response) {

          alert("Error. Try Again!");

      });

   }

   $scope.check=function(event){
        $scope.ansid=($("input[name='answer']:checked").val());
        if($scope.ansid != null ){
            
        $http({
            method: 'POST',
            url: '/validate/',
            dataType: 'json',

            params: { 'answer' : $scope.ansid,'count':$scope.count,'question': $scope.id,'key':$scope.key},
            headers: { 'Content-Type': 'application/json; charset=UTF-8' }

            })
        .then(function(response) {
            $("#baseQues").remove()
            $scope.show = true;
            $scope.results=response.data
            console.log($scope.results)
            $scope.count=$scope.results.count
            $scope.key=$scope.results.key
            if ($scope.results.final_result){
                $scope.final_result=$scope.results.final_result

                $scope.percentile= $scope.results.level_percentile
            }
            if ($scope.results.lastTopic){
                $scope.lastTopic=$scope.results.lastTopic
                $scope.chaptername=$scope.results.chaptername   

                

            }
            if ($scope.results.question != null ){ 
                $scope.id=$scope.results.question.id
                $scope.nextanswers=$scope.results.question.ans

            }

        }, 
        function(response) { // optional
                // failed
        });
        } else{
            alert("Please Select any option to submit")
        }


      } 

    $scope.groupDis = function(){
        alert(222222)
        $http({

            method:"GET",

            url:"/groupsDisplay/",
            params:{"courseid":$("#course_id").val()}
         }).then( function(response, status) {
                $scope.Respone_data=response.data
                $scope.courseID=$("#course_id").val()

                console.log($scope.Respone_data)
                
        });

     }
//////////////////////////////////////////////////// project //////////////////////////////////////////////
    $scope.fileEditorLaunch = function(){

       $scope.editor = ace.edit("editor");
       $scope.editor.setTheme("ace/theme/solarized_dark");
       $scope.editor.session.setMode("ace/mode/python");
       $scope.editor.setShowPrintMargin(false);
       $scope.editor.setOptions({
        fontFamily: "monospace",
        fontSize: "15pt"
        });
       

       $scope.editor.session.setValue("");
}
       
$scope.filestructureLaunch=function(){

    $http({
            method: "GET",
            url: "/filestructure/",
            }).then( function(response, status) {
                $scope.dList=response.data.dList
                $scope.code=response.data.code
                console.log($scope.dList)
        })
    }

$scope.getFileData=function(item){
    
    $scope.editor = ace.edit("editor");
    
    
    $rootScope.filepath = item
    console.log($rootScope.filepath)
    $http({
            method: "GET",
            url: "/fileData/",
            params: {"filePath":$scope.filepath},
            }).then( function(response, status) {
                $scope.filedataa=response.data.code
                
                $scope.editor.session.setValue($scope.filedataa);
                
        });

    

    }
      

$scope.submitFileData=function(){
    $scope.editorvalue=$scope.editor.session.getValue()
    console.log($rootScope.filepath)
        $http({
            method: "GET",
            url: "/writetofile/",
            params: {"editorvalue":$scope.editor.session.getValue(),"filePathToBeSaved":$rootScope.filepath},
            }).then( function(response, status) {
                $scope.filesaved="File Saved Successfully"
                alert($scope.filesaved)
                // $scope.editorvalue=$scope.editor.session.setValue()
                
                });
    }


$scope.restartServer=function(){
    alert($('#project').val())
    $http({
            method: "GET",
            url: "/restartServer/",
            params:{"project_id":$('#project').val()}
            }).then( function(response, status) {
                $scope.done=response.data

                console.log($scope.done)
                
        })
    }
//////////////////////////////////////////////////// End of project //////////////////////////////////////////////

  $scope.cartObject = function(){
    
        $http({
            method:"GET",
            url:"/cartObjects/",

         }).then( function(response, status) {
                if(response.data == 0 ){
                    $scope.objects=true
                }
                else{
                    $scope.objects=false
                }
                
                        });

     }             
            


}
            
module.controller("MainCtrl",Main); 
    


    