
/*
	Read and preview image before upload
*/
function previewImage(ele, file) {

    var reader = new FileReader();

    reader.onload = function (e) {
    	var srcData = e.target.result;
    	$(ele).parents('.form-wrapper').find('.img-preview .inner').append('<img src="'+srcData+'">');
    }

    reader.readAsDataURL(file);
    
}

/*
	Search value in array of an objects
*/
function searchArrayObject(value, data){
    for (var i=0; i < data.length; i++) {
        if (data[i].value == value) {
            return data[i];
        }
    }

    return false;
}

/*
	Get concepts of model
*/
function getConceptsByModel(model_id){
	return new Promise(function(resolve, reject){
		$.ajax({
			url: '/clarifai/api/v.1/model/concepts/get',
			method: 'POST',
			data: {
				model_id: model_id,
				csrfmiddlewaretoken: $("meta[name=csrfmiddlewaretoken]").attr('content')
			},
			success: function(resp){
				resolve(resp);
			},
			error: function(err){
				reject(err);
			}
		});
	});
}


/*
	Add concepts to model & train
*/
function handleCreateTrainModelFormSubmit(e ,action){
	e.preventDefault();
	var model = $('#train-model').val();
	var concepts = $('#train-concepts').val();
	switch(action){
		case 'add_concepts_train': 
			var response = addConceptsToModel(model, concepts);
			response.then(function(data){
				console.log(data);
				var status = JSON.parse(JSON.stringify(data));
				if(status.code == 10000){
					swal({
	                    title: 'Done',
	                    text: status.message,
	                    type: 'success'
	                });
				}else{
					swal({
	                    title: 'Failed',
	                    text: status.message,
	                    type: 'error'
	                });
				}
				
			}).catch(function(err){
				console.log(err);
				swal({
                    title: 'Failed',
                    text: 'Oop! something went wrong while trying request to server.',
                    type: 'error'
                });
				
			});
			break;
		case 'create_model_train':
			var response = createModel(model, concepts);
			response.then(function(data){
				console.log(data);
				var status = JSON.parse(JSON.stringify(data));
				if(status.code == 10000){

					$('.submit-create-model').removeClass('active');
                    $('.submit-train-model').addClass('active');
					model_opts.push({text: status.model.name, value: status.model.id});
					var train_model = train_model_selectize[0].selectize;
					var predict_model = predict_model_selectize[0].selectize;

					train_model.addOption({text: status.model.name, value: status.model.id});
					predict_model.addOption({text: status.model.name, value: status.model.id});

					swal({
	                    title: 'Done',
	                    text: status.message,
	                    type: 'success'
	                });
				}else{
					swal({
	                    title: 'Failed',
	                    text: status.message,
	                    type: 'error'
	                });
				}
			}).catch(function(err){
				console.log(err);
				swal({
                    title: 'Failed',
                    text: 'Oop! something went wrong while trying request to server.',
                    type: 'error'
                });
			});
			break;

		default:
			break;
	}
}

/*
	Add concepts to model & train
*/
function addConceptsToModel(model_id, concepts){
	return new Promise(function(resolve, reject){
		$.ajax({
			url: '/clarifai/api/v.1/model/train',
			method: 'POST',
			data: {
				model_id: model_id,
				concepts: concepts,
				csrfmiddlewaretoken: $("meta[name=csrfmiddlewaretoken]").attr('content')
			},
			success: function(resp){
				resolve(resp);
			},
			error: function(err){
				reject(err);
			}
		});
	});
}


/*
	Create model and train
*/
function createModel(model_id, concepts){
	return new Promise(function(resolve, reject){
		$.ajax({
			url: '/clarifai/api/v.1/model/create',
			method: 'POST',
			data: {
				model_id: model_id,
				concepts: concepts,
				csrfmiddlewaretoken: $("meta[name=csrfmiddlewaretoken]").attr('content')
			},
			success: function(resp){
				resolve(resp);
			},
			error: function(err){
				reject(err);
			}
		});
	});
}


/*
	Make prediction request
*/
function makePrediction(e){
	e.preventDefault();
	var formdata = new FormData($('#predict-from').get(0));
	if(formdata){
		// var predict_model = $('#predict-model').val(),
		// 	predict_concepts = $('#predict-concepts').val(),
		// 	min_predict_value = $('#min-predict-value').val();

		var image_files = $('#predict_images')[0].files;
		if(image_files && image_files.length > 0){

			// formdata.append('predict_images', image_files);
			// formdata.append('predict_model', predict_model);
			// formdata.append('predict_concepts', predict_concepts);
			// formdata.append('min_predict_value', min_predict_value);
			// formdata.append('csrfmiddlewaretoken', $("meta[name=csrfmiddlewaretoken]").attr('content'));
			console.log(image_files);
			$.ajax({
				url: '/clarifai/api/v.1/prediction',
				method: 'POST',
				type: 'POST',
				data: formdata,
				processData: false,
				cache: false,
    			contentType: false,
    			enctype: "multipart/form-data",
				success: function(resp){
					console.log("HHHHHH");
					console.log(JSON.parse(JSON.stringify(resp)));
				},
				error: function(err){
					console.log(err);
				}
			});
		}
		
	}
	
}



/*
	Display chosen files name
*/

(function(){
	$('.uploadfile').each(function(i){
		$(this).on('change', function(e){
			var $previewDiv = $(this).parents('.form-wrapper').find('.img-preview .inner');
			var $previewDivOutter = $(this).parents('.form-wrapper').find('.img-preview-outter');
			var files = this.files;
			var self = this;
				// $previewDivHtml = $previewDiv.html();
			$previewDiv.html('');
			if(files && files.length > 0){
				for(var i = 0; i < files.length; i++){
					previewImage(self, files[i]);
				};

				$($previewDivOutter).fadeIn();	
			}else{
				// $previewDivHtml == '' ? $('.img-preview-outter').fadeOut() : $previewDiv.html($previewDivHtml);
				$($previewDivOutter).fadeOut();
			}
		});
	});

	$('#predict-from').on('submit', function(e){
		e.preventDefault();
		var formdata = new FormData($('#predict-from').get(0));
		if(formdata){
			// var predict_model = $('#predict-model').val(),
			// 	predict_concepts = $('#predict-concepts').val(),
			// 	min_predict_value = $('#min-predict-value').val();

			var image_files = $('#predict_images')[0].files;
			if(image_files && image_files.length > 0){

				// formdata.append('predict_images', image_files);
				// formdata.append('predict_model', predict_model);
				// formdata.append('predict_concepts', predict_concepts);
				// formdata.append('min_predict_value', min_predict_value);
				// formdata.append('csrfmiddlewaretoken', $("meta[name=csrfmiddlewaretoken]").attr('content'));
				console.log(image_files);
				$.ajax({
					url: '/clarifai/api/v.1/prediction',
					method: 'POST',
					type: 'POST',
					data: formdata,
					processData: false,
					cache: false,
	    			contentType: false,
	    			enctype: "multipart/form-data",
					success: function(resp){
						console.log("GGGGGG");
						console.log(JSON.parse(JSON.stringify(resp)));
					},
					error: function(err){
						console.log(err);
					}
				});
			}
			
		}
	});
})();