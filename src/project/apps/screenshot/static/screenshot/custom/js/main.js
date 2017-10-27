
(function(){

	$('#screenshot_api_form').on('submit', function(e){
		e.preventDefault();
		var formdata = new FormData($('#screenshot_api_form').get(0));
		if(formdata){
			console.log(formdata.get('browsers'));
			$.ajax({
				url: '/screenshot/api/v.1/generate-screenshot',
				method: 'POST',
				type: 'POST',
				data: formdata,
				processData: false,
				cache: false,
    			contentType: false,
    			enctype: "multipart/form-data",
				success: function(resp){
					console.log("YOLO");
					console.log(JSON.parse(JSON.stringify(resp)));
					data = JSON.parse(JSON.stringify(resp));
					if (data.status == 200) {
						swal({
		                    title: 'Done',
		                    text: data.img_path,
		                    type: 'success'
		                });
					}else{
						swal({
		                    title: 'Failed',
		                    text: data.error_message,
		                    type: 'error'
		                });
					}
					
				},
				error: function(err){
					console.log(err);
				}
			});
		}
	});

})();