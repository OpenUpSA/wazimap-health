$(document).ready(function(){
	 function getCookie(name) {
	     var cookieValue = null;
	     if (document.cookie && document.cookie !== '') {
		 var cookies = document.cookie.split(';');
		 for (var i = 0; i < cookies.length; i++) {
		     var cookie = jQuery.trim(cookies[i]);
		     // Does this cookie string begin with the name we want?
				  if (cookie.substring(0, name.length + 1) === (name + '=')) {
				      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				      break;
				  }
		 }
	     }
	     return cookieValue;
	 }
	 var csrftoken = getCookie('csrftoken');
	 $('#partner_import_form').on('submit',function(event){
	     event.preventDefault();
	     var partnerForm = document.getElementById('partner_import_form');
	     var partnerDataForm = new FormData(this);
	     $.ajax({
		 url: partnerForm.getAttribute('action'),
		 type: partnerForm.getAttribute('method'),
		 data: partnerDataForm,
		 processData: false,
		 contentType: false,
		 beforeSend: function(xhr, settings){
		     xhr.setRequestHeader("X-CSRFToken", csrftoken);
		     $(".loader").css("display", "block");
		 },
		 success: function(data){
		     if (data['status'] == 'ok'){
			 console.log("Partner Sheet has been imported");
			 $("#successMessage").css("display", 'block');
		     }
		     else{
			 console.log("Error Uploading Partner Sheet");
			 $("#errorMessage").css("display", 'block');
			 $('#errorDetail').css("display", 'block');
			 $('#errorDetail').html(data['form']);
		     }
		 },
		 complete: function(data){
		     $(".loader").css("display", "none");
		 },
		 error: function(xhr,message, error){
		     console.log(xhr.status +  " : "+ xhr.responseText);
		     $('#errorDetail').css("display", 'block');
		     $('#errorDetail').html(xhr.status +  " : "+ xhr.responseText);
		 },

	     }); 
	 });
     });
