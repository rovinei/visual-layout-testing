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
});
