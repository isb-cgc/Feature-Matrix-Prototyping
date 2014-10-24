/*
Copyright 2014 Google Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

$(function() {
    $("#logEntryForm").validate({
        rules: {
            logMessage: "required",
        },
        messages: {
          logMessage: "Please provide a message to log.",
        },
        highlight: function(element) {
            $(element).parent().parent().addClass("has-error");
        },
        unhighlight: function(element) {
            $(element).parent().parent().removeClass("has-error");
        },
        submitHandler: function(form) {
            $('#alertMessage').hide();
            form.submit();
        }
    });
});
