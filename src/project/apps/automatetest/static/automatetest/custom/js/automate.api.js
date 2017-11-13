/* -------------------------------------------------------------------------

	PUNITED.automateAPI

	Automate Browser API integrating with BrowserStack Automate API:
	    + Automate API
	    + Screenshot API
	    + Live Automate

------------------------------------------------------------------------- */

var PUNITED;
if (!PUNITED) PUNITED = {};
if (!PUNITED.automateAPI) PUNITED.automateAPI = {};

(function(){
    var func = PUNITED.automateAPI;

    /*
        * Get available browsers list
        * Ajax function request
        * HTTP METHOD : GET
        * REQUEST URL : /api/v.1/automate/get_browsers
    */
    func.getAvailableBrowsers = function(){
        $.ajax({
            url: '/api/v.1/automate/get_browsers',
            method: 'GET',
            type: 'GET',
            dataType: 'application/json',
            success: function(response){
                console.log(JSON.parse(JSON.stringify(response)));
            },
            error: function(error){
                console.log(JSON.parse(JSON.stringify(error)));
            }
        });
    }

    /*
        * Automate cross browser platform testing
        * Ajax function request
        * HTTP METHOD : GET
        * REQUEST URL :
    */
    func.automateBrowserTest = function(){

    }

    /*
        * Get project list
        * Ajax function request
        * HTTP METHOD : GET
        * REQUEST URL :
    */
    func.getProjectsList = function(){
        $.ajax({
            url: '/automate/project_view',
            method: 'GET',
            type: 'GET',
            dataType: 'application/json',
            success: function(response){
                console.log(JSON.parse(JSON.stringify(response)));
            },
            error: function(error){
                console.log(JSON.parse(JSON.stringify(error)));
            }
        });
    }

    /*
        * Create new project
        * Ajax function request
        * HTTP METHOD : GET
        * REQUEST URL :
    */
    func.createNewProject = function(){
        swal({
            title: 'Create New Project',
            html:
                '<div class="uk-margin">' +
                '<div class="uk-form-controls">'+
                '<input placeholder="Enter project name" type="text" id="create-project-name" class="uk-input custom-text-input">' +
                '</div>' +
                '</div>' +
                '<div class="uk-margin">' +
                '<div class="uk-form-controls">' +
                '<textarea placeholder="Description" id="create-project-desc" class="uk-textarea custom-textarea"></textarea>' +
                '</div>' +
                '</div>',
            showCancelButton: true,
            confirmButtonText: 'Create',
            showLoaderOnConfirm: true,
            focusConfirm: false,
            preConfirm: function () {
                var $project_name = $('#create-project-name').val(),
                    $project_desc = $('#create-project-desc').val(),
                    $csrftoken = $("meta[name=csrfmiddlewaretoken]").attr('content');
                return new Promise(function (resolve, reject) {
                    $.ajax({
                        url: '/automate/ajax/project_view',
                        method: 'POST',
                        type: 'POST',
                        data: {
                            csrfmiddlewaretoken: $csrftoken,
                            action: 'create',
                            project_name: $project_name,
                            project_desc: $project_desc
                        },
                        dataType: 'json',
                        success: function(response){
                            resolve(response);
                        },
                        error: function(error){
                            swal({
                                title: "Failed",
                                type: 'error',
                                text: error.responseText,
                                timer: 5000,
                            });
                            reject();
                        }
                    });
                });
            },
            allowOutsideClick: false
        }).then(function (result) {
            var res = JSON.parse(JSON.stringify(result));
            if(res.status == 200){
                swal({
                    title: "Done",
                    type: 'success',
                    text: res.message,
                    timer: 5000,
                });
            }else{
                swal({
                    title: "Failed",
                    type: 'error',
                    text: res.message,
                    timer: 5000,
                });
            }

        });
    }

    /*
        * Create new project
        * Ajax function request
        * HTTP METHOD : GET
        * REQUEST URL :
    */
    func.deleteProject = function(){
        $('.project_item .key-icon-delete').on('click', function(e){
            var self = $(this);
            e.preventDefault();
            swal({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#E71D36',
                cancelButtonColor: '#aaa',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'cancel',
                showLoaderOnConfirm: true,
                focusConfirm: true,
                preConfirm: function () {
                    var $project_uuid = $(self).parents('.project_item').attr('data-uuid'),
                        $csrftoken = $("meta[name=csrfmiddlewaretoken]").attr('content');
                        console.log($project_uuid);
                    return new Promise(function (resolve, reject) {
                        $.ajax({
                            url: '/automate/ajax/project_view',
                            method: 'POST',
                            type: 'POST',
                            data: {
                                csrfmiddlewaretoken: $csrftoken,
                                action: 'delete',
                                project_uuid: $project_uuid,
                            },
                            dataType: 'json',
                            success: function(response){
                                resolve(response);
                            },
                            error: function(error){
                                swal({
                                    title: "Failed",
                                    type: 'error',
                                    text: error.responseText,

                                });
                                reject();
                            }
                        });
                    });
                },
                allowOutsideClick: false
            }).then(function (result) {
                var res = JSON.parse(JSON.stringify(result));
                if(res.status == 200){
                    swal({
                        title: "Done",
                        type: 'success',
                        text: res.message,
                        timer: 5000,
                    });
                    $(self).parents('.project_item').remove();
                }else{
                    swal({
                        title: "Failed",
                        type: 'error',
                        text: res.message,

                    });
                }

            });
        });
    }

    /*
        * Edit project function
        * Ajax function request
        * HTTP METHOD : GET
        * REQUEST URL : /api/v.1/automate/get_browsers
    */
    func.editProject = function(){
        $('.project_item .key-icon-edit').on('click', function(e){
            e.preventDefault();
            var self = $(this),
                $project_uuid = $(self).parents('.project_item').attr('data-uuid'),
                $project_div = $(self).parents('.project_item');

            function showEditDialog(data){
                var res = JSON.parse(JSON.stringify(data));
                var project = JSON.parse(res.project);
                swal({
                    title: 'Edit Project',
                    html:
                        '<div class="uk-margin">' +
                        '<div class="uk-form-controls">'+
                        '<input placeholder="Enter project name" type="text" id="edit-project-name" class="uk-input custom-text-input" value="'+ project[0].fields.project_name +'">' +
                        '</div>' +
                        '</div>' +
                        '<div class="uk-margin">' +
                        '<div class="uk-form-controls">' +
                        '<textarea placeholder="Description" id="edit-project-desc" class="uk-textarea custom-textarea">'+ project[0].fields.description +'</textarea>' +
                        '</div>' +
                        '</div>',
                    showCancelButton: true,
                    confirmButtonText: 'Update',
                    showLoaderOnConfirm: true,
                    focusConfirm: false,
                    preConfirm: function () {
                        var $project_name = $('#edit-project-name').val(),
                            $project_desc = $('#edit-project-desc').val(),
                            $csrftoken = $("meta[name=csrfmiddlewaretoken]").attr('content');
                        return new Promise(function (resolve, reject) {
                            $.ajax({
                                url: '/automate/ajax/project_view',
                                method: 'POST',
                                type: 'POST',
                                data: {
                                    csrfmiddlewaretoken: $csrftoken,
                                    action: 'update',
                                    project_uuid: project[0].fields.project_uuid,
                                    project_name: $project_name,
                                    project_desc: $project_desc
                                },
                                dataType: 'json',
                                success: function(response){
                                    resolve(response);
                                },
                                error: function(error){
                                    swal({
                                        title: "Failed",
                                        type: 'error',
                                        text: error.responseText,
                                        timer: 5000,
                                    });
                                    reject();
                                }
                            });
                        });
                    },
                    allowOutsideClick: false
                }).then(function (result) {
                    var res = JSON.parse(JSON.stringify(result));
                    var project = JSON.parse(res.project);
                    if(res.status == 200){
                        $(self).parents('.project_item').attr('data-uuid', project[0].fields.project_uuid);
                        $(self).parents('.project_item').find('.project_name').text(project[0].fields.project_name);
                        swal({
                            title: "Done",
                            type: 'success',
                            text: res.message,
                            timer: 5000,
                        });
                    }else{
                        swal({
                            title: "Failed",
                            type: 'error',
                            text: res.message,
                            timer: 5000,
                        });
                    }

                });
            }

            (function(){
                $('#loading-spinner').addClass('active');
                $.ajax({
                    url: '/automate/ajax/project_view',
                    method: 'GET',
                    type: 'GET',
                    data: {
                        action: 'single_project',
                        project_uuid: $project_uuid,
                    },
                    contentType: 'application/x-www-form-urlencoded',
                    dataType: 'json',
                    success: function(response){
                        $('#loading-spinner').removeClass('active');
                        showEditDialog(response);
                    },
                    error: function(error){
                        $('#loading-spinner').removeClass('active');
                        swal({
                            title: "Failed",
                            type: 'error',
                            text: error.responseText,

                        });
                    }
                });

            })();
        });
    }

    /*
        * Automate Cross Browser Function
        * Ajax function request
        * HTTP METHOD : GET
        * REQUEST URL : /api/v.1/automate/get_browsers
    */
    func.crossBrowserTest = function(){
        $('#cross_browser_form').on('submit', function(e){
            e.preventDefault();
            var self = $(this);
            $('#loading-spinner').addClass('active');
            var formData = new FormData($('#cross_browser_form').get(0));
            console.log($(self).attr('action'));
            console.log(formData.get('browsers'));
            if(formData){
                $.ajax({
                    url: $(self).attr('action'),
                    method: 'POST',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    cache: false,
                    contentType: false,
                    enctype: "multipart/form-data",
                    success: function(resp){
                        $('#loading-spinner').removeClass('active');
                        console.log(JSON.parse(JSON.stringify(resp)));
                        var response = JSON.parse(JSON.stringify(resp));
                        var browsers = response.data;
                        var reports_html = "<h3 class='md-title'>Summarized Report</h3>";

                        if (response.status == 200) {
                            for(var i=0; i<browsers.length; i++){
                                var browser = browsers[i],
                                    status = browser.status;
                                if(status == 200){
                                    var report = JSON.parse(browser.report),
                                        report_url = "/automate/report/" + report[0].fields.report_dir + "report.html";

                                    reports_html += "<div class='uk-margin uk-width-1-1'>" +
                                                        "<div class='alert-report-title'>" +
                                                            "<h4 class='uk-title'>"+ report[0].fields.title +"</h4>" +
                                                        "</div>" +
                                                        "<div class='alert-report-url'>" +
                                                            "<a href='"+ report_url +"'> See detail </a>" +
                                                        "</div>" +
                                                    "</div>";

                                }else{
                                    reports_html += "<div class='uk-margin uk-width-1-1'>" +
                                                        "<div class='alert-report-title'>" +
                                                            "<h4 class='uk-title uk-text-danger'>" +
                                                                browser.title +
                                                            "</h4>" +
                                                        "</div>" +
                                                        "<div class='alert-report-msg'>" +
                                                            browser.message +
                                                        "</div>" +
                                                     "</div>";
                                }

                            }

                            swal({
                                title: 'Done',
                                html: reports_html,
                                type: 'success',
                                allowOutsideClick: false,
                            });

                        }else{
                            swal({
                                title: 'Failed',
                                text: data.message,
                                type: 'error'
                            });
                        }

                    },
                    error: function(error){
                        $('#loading-spinner').removeClass('active');
                        swal({
                            title: 'Failed',
                            text: error.responseText,
                            type: 'error'
                        });
                    }
                });
            }
        });
    }

    /*
        * Init function
        * Ajax function request
        * HTTP METHOD : GET
        * REQUEST URL : /api/v.1/automate/get_browsers
    */
    func.init = (function(){
        func.deleteProject();
        func.editProject();
        func.crossBrowserTest();
    })();

})();
