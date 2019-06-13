'use strict';

;(function (document, window, index)
{
    // File listing

    var file_list = document.getElementById('file_list');

    function deleteFile(file)
    {
        var ajax = new XMLHttpRequest();
        ajax.open("DELETE", file, true);

        ajax.addEventListener('load', function(e) {
            e.preventDefault();
            e.stopPropagation();

            if (ajax.status >= 200 && ajax.status < 400)
            {
                requestList();
            }
            else
                alert('Error. Please contact Nanome');
        });

        ajax.send();
    }

    function requestList()
    {
        var ajax = new XMLHttpRequest();
        ajax.open("GET", "/list", true);

        ajax.addEventListener('load', function(e) {
            e.preventDefault();
            e.stopPropagation();

            if (ajax.status >= 200 && ajax.status < 400)
            {
                var data = JSON.parse(ajax.responseText);
                file_list.innerHTML = "";
                if (data.success) {
                    data.file_list.forEach(file => {
                        var node = document.createElement("li");
                        var textnode = document.createTextNode(file + " - ");
                        var btn = document.createElement("Button");
                        btn.innerHTML = "DELETE";
                        btn.addEventListener('click', function(e) {
                            e.preventDefault();
                            deleteFile(file);
                        });
                        node.appendChild(textnode);
                        node.appendChild(btn);
                        file_list.appendChild(node);
                    });
                }
            }
            else
                alert('Error. Please contact Nanome');
        });

        ajax.send();
    }

    // File Upload

    var form = document.getElementById('file_uploader');
    var input		 = form.querySelector('input[type="file"]'),
        label		 = form.querySelector('label'),
        errorMsg	 = form.querySelector('.box__error span'),
        restart		 = form.querySelectorAll('.box__restart'),
        droppedFiles = false,
        submitForm = function()
        {
            // preventing the duplicate submissions if the current one is in progress
            if (form.classList.contains('is-uploading'))
                return false;

            form.classList.add('is-uploading');
            form.classList.remove('is-error');
            form.classList.remove('is-success');

            // gathering the form data
            var ajaxData = new FormData(form);
            if (droppedFiles)
            {
                Array.prototype.forEach.call(droppedFiles, function(file)
                {
                    ajaxData.append(input.getAttribute('name'), file);
                });
            }

            // ajax request
            var ajax = new XMLHttpRequest();
            ajax.open(form.getAttribute('method'), form.getAttribute('action'), true);

            ajax.addEventListener('load', function(e) {
                e.preventDefault();
                e.stopPropagation();

                form.classList.remove('is-uploading');
                if (ajax.status >= 200 && ajax.status < 400)
                {
                    var data = JSON.parse(ajax.responseText);
                    form.classList.add(data.success == true ? 'is-success' : 'is-error');
                    if (!data.success)
                        errorMsg.textContent = data.error;
                    requestList()
                }
                else
                    alert('Error. Please contact Nanome');
            });

            ajax.addEventListener('error', function(e) {
                e.preventDefault();
                e.stopPropagation();

                form.classList.remove('is-uploading');
                alert('Error. Please, try again!');
            });

            ajax.send(ajaxData);

            return false;
        };

    // automatically submit the form on file select
    input.addEventListener('change', function(e)
    {
        droppedFiles = false;
        submitForm()
    });

    [ 'drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop' ].forEach(function(event)
    {
        form.addEventListener(event, function(e)
        {
            // preventing the unwanted behaviours
            e.preventDefault();
            e.stopPropagation();
        });
    });
    [ 'dragover', 'dragenter' ].forEach(function(event)
    {
        form.addEventListener(event, function()
        {
            form.classList.add('is-dragover');
        });
    });
    [ 'dragleave', 'dragend', 'drop' ].forEach(function(event)
    {
        form.addEventListener(event, function()
        {
            form.classList.remove('is-dragover');
        });
    });
    form.addEventListener('drop', function(e)
    {
        droppedFiles = e.dataTransfer.files;
        submitForm();
    });

    form.onsubmit = submitForm;

    Array.prototype.forEach.call(restart, function(entry)
    {
        entry.addEventListener('click', function(e)
        {
            e.preventDefault();
            form.classList.remove('is-error', 'is-success');
            input.click();
        });
    });

    input.addEventListener('focus', function() { input.classList.add('has-focus'); });
    input.addEventListener('blur', function() { input.classList.remove('has-focus'); });

    requestList();
}(document, window, 0));