!function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a="function"==typeof require&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}for(var i="function"==typeof require&&require,o=0;o<r.length;o++)s(r[o]);return s}({1:[function(require,module,exports){"use strict";function load(location,callback){var xhr;xhr=window.XMLHttpRequest?new XMLHttpRequest:new ActiveXObject("Microsoft.XMLHTTP"),xhr.open("GET",location,!0),xhr.onreadystatechange=function(){if(200===xhr.status&&4===xhr.readyState)try{callback(null,JSON.parse(xhr.responseText))}catch(err){callback(err,null)}},xhr.send()}module.exports={load:load}},{}],2:[function(require,module,exports){"use strict";module.exports=function OptionsValidator(params){function validateParams(params){return params?void 0!==params.required&&params.required instanceof Array:!1}if(!validateParams(params))throw new Error("-- OptionsValidator: required options missing");if(!(this instanceof OptionsValidator))return new OptionsValidator(params);var requiredOptions=params.required;this.getRequiredOptions=function(){return requiredOptions},this.validate=function(parameters){var errors=[];return requiredOptions.forEach(function(requiredOptionName){void 0===parameters[requiredOptionName]&&errors.push(requiredOptionName)}),errors}}},{}],3:[function(require,module,exports){"use strict";function put(data){return isObject(data)?addObject(data):isArray(data)?addArray(data):void 0}function clear(){return data.length=0,data}function get(){return data}function isObject(obj){return!!obj&&"[object Object]"===Object.prototype.toString.call(obj)}function isArray(obj){return!!obj&&"[object Array]"===Object.prototype.toString.call(obj)}function addObject(_data){return data.push(_data),data}function addArray(_data){for(var added=[],i=0;i<_data.length;i++)isObject(_data[i])&&added.push(addObject(_data[i]));return added}function search(crit){return crit?findMatches(data,crit,opt.searchStrategy,opt):[]}function setOptions(_opt){opt=_opt||{},opt.fuzzy=_opt.fuzzy||!1,opt.limit=_opt.limit||10,opt.searchStrategy=_opt.fuzzy?FuzzySearchStrategy:LiteralSearchStrategy}function findMatches(data,crit,strategy,opt){for(var matches=[],i=0;i<data.length&&matches.length<opt.limit;i++){var match=findMatchesInObject(data[i],crit,strategy,opt);match&&matches.push(match)}return matches}function findMatchesInObject(obj,crit,strategy,opt){for(var key in obj)if(!isExcluded(obj[key],opt.exclude)&&strategy.matches(obj[key],crit))return obj}function isExcluded(term,excludedTerms){var excluded=!1;excludedTerms=excludedTerms||[];for(var i=0;i<excludedTerms.length;i++){var excludedTerm=excludedTerms[i];!excluded&&new RegExp(term).test(excludedTerm)&&(excluded=!0)}return excluded}module.exports={put:put,clear:clear,get:get,search:search,setOptions:setOptions};var FuzzySearchStrategy=require("./SearchStrategies/FuzzySearchStrategy"),LiteralSearchStrategy=require("./SearchStrategies/LiteralSearchStrategy"),data=[],opt={};opt.fuzzy=!1,opt.limit=10,opt.searchStrategy=opt.fuzzy?FuzzySearchStrategy:LiteralSearchStrategy},{"./SearchStrategies/FuzzySearchStrategy":4,"./SearchStrategies/LiteralSearchStrategy":5}],4:[function(require,module,exports){"use strict";function FuzzySearchStrategy(){function fuzzyRegexFromString(string){return new RegExp(string.split("").join(".*?"),"gi")}this.matches=function(string,crit){return"string"!=typeof string?!1:(string=string.trim(),!!fuzzyRegexFromString(crit).test(string))}}module.exports=new FuzzySearchStrategy},{}],5:[function(require,module,exports){"use strict";function LiteralSearchStrategy(){function matchesString(string,crit){return string.toLowerCase().indexOf(crit.toLowerCase())>=0}this.matches=function(string,crit){return"string"!=typeof string?!1:(string=string.trim(),matchesString(string,crit))}}module.exports=new LiteralSearchStrategy},{}],6:[function(require,module,exports){"use strict";function setOptions(_options){options.pattern=_options.pattern||options.pattern,options.template=_options.template||options.template,"function"==typeof _options.middleware&&(options.middleware=_options.middleware)}function compile(data){return options.template.replace(options.pattern,function(match,prop){var value=options.middleware(prop,data[prop],options.template);return void 0!==value?value:data[prop]||match})}module.exports={compile:compile,setOptions:setOptions};var options={};options.pattern=/\{(.*?)\}/g,options.template="",options.middleware=function(){}},{}],7:[function(require,module,exports){!function(window,document,undefined){"use strict";function initWithJSON(json){repository.put(json),registerInput()}function initWithURL(url){jsonLoader.load(url,function(err,json){err&&throwError("failed to get JSON ("+url+")"),initWithJSON(json)})}function emptyResultsContainer(){options.resultsContainer.innerHTML=""}function appendToResultsContainer(text){options.resultsContainer.innerHTML+=text}function registerInput(){options.searchInput.addEventListener("keyup",function(e){emptyResultsContainer(),e.target.value.length>0&&render(repository.search(e.target.value))})}function render(results){if(0===results.length)return appendToResultsContainer(options.noResultsText);for(var i=0;i<results.length;i++)appendToResultsContainer(templater.compile(results[i]))}function throwError(message){throw new Error("SimpleJekyllSearch --- "+message)}var options={searchInput:null,resultsContainer:null,json:[],searchResultTemplate:'<li><a href="{url}" title="{desc}">{title}</a></li>',templateMiddleware:function(){},noResultsText:"No results found",limit:10,fuzzy:!1,exclude:[]},requiredOptions=["searchInput","resultsContainer","json"],templater=require("./Templater"),repository=require("./Repository"),jsonLoader=require("./JSONLoader"),optionsValidator=require("./OptionsValidator")({required:requiredOptions}),utils=require("./utils");window.SimpleJekyllSearch=function(_options){var errors=optionsValidator.validate(_options);errors.length>0&&throwError("You must specify the following required options: "+requiredOptions),options=utils.merge(options,_options),templater.setOptions({template:options.searchResultTemplate,middleware:options.templateMiddleware}),repository.setOptions({fuzzy:options.fuzzy,limit:options.limit}),utils.isJSON(options.json)?initWithJSON(options.json):initWithURL(options.json)},window.SimpleJekyllSearch.init=window.SimpleJekyllSearch}(window,document)},{"./JSONLoader":1,"./OptionsValidator":2,"./Repository":3,"./Templater":6,"./utils":8}],8:[function(require,module,exports){"use strict";function merge(defaultParams,mergeParams){var mergedOptions={};for(var option in defaultParams)mergedOptions[option]=defaultParams[option],void 0!==mergeParams[option]&&(mergedOptions[option]=mergeParams[option]);return mergedOptions}function isJSON(json){try{return json instanceof Object&&JSON.parse(JSON.stringify(json))?!0:!1}catch(e){return!1}}module.exports={merge:merge,isJSON:isJSON}},{}]},{},[7]);

 //============================================================================
//  Custom functionality

// var search_modal_current_selection = null;
// var search_modal_wraparound = true;

// // $('#search-input').focus();

// function get_next() {
//     if (search_modal_current_selection == null) {
//         search_modal_current_selection = $('.focusable').first();
//     } else {
//         if (!search_modal_current_selection.is($('.focusable').last())) {
//             search_modal_current_selection = search_modal_current_selection.next('.focusable');
//         } else {
//             search_modal_current_selection = search_modal_wraparound ? $('.focusable').first() : search_modal_current_selection;
//         }
//     }
//     return search_modal_current_selection;
// }

// function get_prev() {
//     if (search_modal_current_selection == null) {
//         search_modal_current_selection = $('.focusable').last();
//     } else {
//         if (!search_modal_current_selection.is($('.focusable').first())) {
//             search_modal_current_selection = search_modal_current_selection.prev('.focusable');
//         } else {
//             search_modal_current_selection = search_modal_wraparound ? $('.focusable').last() : search_modal_current_selection;   
//         }
//     }
//     return search_modal_current_selection;
// }

// function invalidate_selection() {
//     if (search_modal_current_selection != null) {
//         search_modal_current_selection.removeClass('active');
//         search_modal_current_selection = null;
//     }
// }

// function select_next() {
//     if (search_modal_current_selection != null) {
//         search_modal_current_selection.removeClass('active');
//     }
//     search_modal_current_selection = get_next().addClass('active');
// }

// function select_prev() {
//     if (search_modal_current_selection != null) {
//         search_modal_current_selection.removeClass('active');
//     }
//     search_modal_current_selection = get_prev().addClass('active');
// }

// function goto_search_modal_current_selection_link() {
//     window.open(search_modal_current_selection.attr('href'),'_self');
// }

// $(window).keyup(function (e) {
//     if (e.which === 40) { // down
//         select_next();
//     } else if (e.which === 38) { // up
//         select_prev();
//     } else if (e.which === 27) { // esc
//         finishSearch();
//         invalidate_selection();
//     } else if (e.which === 13) { // enter
//         goto_search_modal_current_selection_link();
//     } else {
//         invalidate_selection();
//     }
// });

// function finishSearch() {
//     $('#results-container').html('');
//     $('#search-input').val('');
//     $('#search-input').blur();
// }

SimpleJekyllSearch({
    searchInput: document.getElementById("search-modal-input"),
    resultsContainer: document.getElementById("search-results-container"),
    json: "/extras/search.json",
    searchResultTemplate: '<a href="{url}" class="list-group-item focusable search-result-item"><h4 class="list-group-item-heading">{title}<small style="margin-left: 4px">{tags}</small></h4><p class="list-group-item-text">{summary}</p></a>',
    noResultsText: '<div class="panel panel-danger"><div class="panel-heading"><i class="fa fa-exclamation-triangle"></i> No results were found..</div><div class="panel-body">The search algorithm tries to match your input to the following post parameters: <ul><li>title</li><li>category</li><li>tags</li><li>url</li><li>date</li><li>summary</li></ul>Make sure you pass the right keyword according to your needs.<br />You can search for a date as well. The accepted format is: <i>yyyy-mm-dd</i>.</div></div>',
    limit: 40,
    fuzzy: false
});

$('#search-modal').on('shown.bs.modal', function () {
    $('#search-modal-input').focus();
})

$('#search-modal').on('hidden.bs.modal', function () {
    $('#search-modal-input').val('');
    $('#search-results-container').html('');
})

$(document).ready(function() {
  $('#search-modal-form input').keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});
